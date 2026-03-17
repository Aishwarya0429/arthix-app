"""
utils/auth.py — JWT Authentication for Arthix
══════════════════════════════════════════════════════════════
REPLACES: Old session-state only auth (check_auth / basic login)

JWT Flow:
  1. User submits email + password
  2. Password verified against SHA-256 hash in DB
  3. JWT access token  generated → 8 hour  expiry  (HS256)
  4. JWT refresh token generated → 7 day   expiry  (HS256)
  5. Both tokens stored in st.session_state
  6. Every page load → verify_session() validates token
  7. Expired access token → auto-refresh via refresh token
  8. Both expired → force logout

Token Payload:
  {
    "sub":      user_id,
    "name":     user_name,
    "email":    user_email,
    "role":     "Owner" | "Accountant" | "Staff",
    "biz_id":   business_id,
    "biz_name": business_name,
    "iat":      issued_at  (UTC),
    "exp":      expiry     (UTC),
    "type":     "access" | "refresh"
  }
══════════════════════════════════════════════════════════════
"""

import jwt
import streamlit as st
from datetime import datetime, timezone, timedelta
from utils.database import authenticate, get_businesses, register_user, create_business

# ── JWT Config ────────────────────────────────────────────────
# In production load from: os.environ["JWT_SECRET"]
JWT_SECRET              = "arthix_jwt_secret_key_infosys_2026"
JWT_ALGORITHM           = "HS256"
ACCESS_TOKEN_EXPIRY_HOURS  = 8   # 8 hours
REFRESH_TOKEN_EXPIRY_DAYS  = 7   # 7 days


# ══════════════════════════════════════════════════════════════
# TOKEN GENERATION
# ══════════════════════════════════════════════════════════════

def _generate_access_token(user: dict, biz_id, biz_name: str) -> str:
    """Generate signed JWT access token — expires in 8 hours."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub":     str(user["id"]),
        "name":     user["name"],
        "email":    user["email"],
        "role":     user["role"],
        "biz_id":   biz_id,
        "biz_name": biz_name,
        "iat":      now,
        "exp":      now + timedelta(hours=ACCESS_TOKEN_EXPIRY_HOURS),
        "type":     "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def _generate_refresh_token(user_id: int, email: str) -> str:
    """Generate signed JWT refresh token — expires in 7 days."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub":   str(user_id),
        "email": email,
        "iat":   now,
        "exp":   now + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
        "type":  "refresh",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# ══════════════════════════════════════════════════════════════
# TOKEN VERIFICATION
# ══════════════════════════════════════════════════════════════

def _verify_token(token: str, expected_type: str):
    """
    Decode and verify JWT token.
    Returns payload dict on success, None on failure.
    Checks: valid signature, not expired, correct type.
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "iat", "sub", "type"]},
        )
        if payload.get("type") != expected_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None   # Expired — caller handles refresh
    except jwt.InvalidTokenError:
        return None   # Tampered or malformed


def _decode_expired_token(token: str):
    """Decode token WITHOUT checking expiry — used during refresh flow."""
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.InvalidTokenError:
        return None


# ══════════════════════════════════════════════════════════════
# SESSION MANAGEMENT
# ══════════════════════════════════════════════════════════════

def _store_session(access_token: str, refresh_token: str, payload: dict):
    """Write JWT tokens and user info into Streamlit session state."""
    if payload is None:
        raise ValueError("JWT payload is None — token decode failed.")
    st.session_state.logged_in     = True
    st.session_state.access_token  = access_token
    st.session_state.refresh_token = refresh_token
    st.session_state.user_id       = int(payload["sub"])
    st.session_state.username      = payload["name"]
    st.session_state.email         = payload["email"]
    st.session_state.role          = payload["role"]
    st.session_state.business_id   = payload["biz_id"]
    st.session_state.business_name = payload["biz_name"]
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"


def _clear_session():
    """Wipe all session state — used on logout or token expiry."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def _token_expiry_info() -> str:
    """Return human-readable session time remaining for sidebar display."""
    token = st.session_state.get("access_token")
    if not token:
        return ""
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        exp  = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        diff = exp - datetime.now(timezone.utc)
        if diff.total_seconds() <= 0:
            return "Session expired"
        hours, rem = divmod(int(diff.total_seconds()), 3600)
        mins = rem // 60
        return f"Session valid {hours}h {mins}m" if hours > 0 else f"Session valid {mins}m"
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════

def login(email: str, password: str) -> tuple:
    """
    Authenticate user and issue JWT tokens.

    Steps:
      1. Verify credentials against DB (SHA-256 hash comparison)
      2. Fetch user's business profile
      3. Generate access token  (8h, HS256)
      4. Generate refresh token (7d, HS256)
      5. Store both in session state

    Returns: (success: bool, message: str)
    """
    # Step 1 — verify credentials
    user = authenticate(email, password)
    if not user:
        return False, "❌ Invalid email or password."

    # Step 2 — get business
    businesses = get_businesses(user["id"])
    biz_id     = businesses[0]["id"]   if businesses else None
    biz_name   = businesses[0]["name"] if businesses else "No Business"

    # Step 3 & 4 — generate tokens
    access_token  = _generate_access_token(user, biz_id, biz_name)
    refresh_token = _generate_refresh_token(user["id"], user["email"])

    # Step 5 — decode token directly (we just created it, guaranteed valid)
    payload = jwt.decode(
        access_token, JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        options={"verify_exp": False},
    )
    _store_session(access_token, refresh_token, payload)

    return True, f"✅ Welcome back, {user['name']}!"


def logout():
    """Clear all JWT tokens and session data."""
    _clear_session()


def verify_session() -> bool:
    """
    Called on EVERY page load to validate current JWT session.

    Logic:
      • No token          → return False (show login)
      • Valid access token → return True  (render app)
      • Expired access + valid refresh → auto-issue new access token
      • Both expired      → clear session, return False
    """
    access_token  = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")

    # No token at all
    if not access_token:
        return False

    # Valid access token
    payload = _verify_token(access_token, "access")
    if payload:
        return True

    # Access expired — try refresh token
    if not refresh_token:
        _clear_session()
        return False

    refresh_payload = _verify_token(refresh_token, "refresh")
    if not refresh_payload:
        # Refresh also expired → force re-login
        _clear_session()
        return False

    # Re-issue new access token using expired token's data
    expired_payload = _decode_expired_token(access_token)
    if not expired_payload:
        _clear_session()
        return False

    user = {
        "id":    expired_payload["sub"],
        "name":  expired_payload["name"],
        "email": expired_payload["email"],
        "role":  expired_payload["role"],
    }
    new_access  = _generate_access_token(
        user, expired_payload["biz_id"], expired_payload["biz_name"]
    )
    new_payload = jwt.decode(
        new_access, JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        options={"verify_exp": False},
    )
    _store_session(new_access, refresh_token, new_payload)
    st.toast("🔄 Session refreshed automatically.", icon="🔒")
    return True


def require_role(*allowed_roles: str) -> bool:
    """
    Check if current user has one of the required roles.
    Usage: require_role("Owner", "Accountant")
    Returns True if allowed, shows error and returns False if not.
    """
    role = st.session_state.get("role", "")
    if role in allowed_roles:
        return True
    st.error(
        f"⛔ Access Denied — Requires: {' or '.join(allowed_roles)}. "
        f"Your role: **{role}**"
    )
    return False


def register(name: str, email: str, password: str,
             role: str, biz_name: str, biz_category: str) -> tuple:
    """
    Register new user + business, then auto-login with JWT.

    Steps:
      1. Create user in DB (password SHA-256 hashed in database.py)
      2. Create business profile linked to user
      3. Auto-login → generates JWT access + refresh tokens
      4. Populate session state

    Returns: (success: bool, message: str)
    """
    uid = register_user(name, email, password, role)
    if uid is None:
        return False, "❌ Email already registered. Please sign in."

    create_business(uid, biz_name, biz_category)

    success, msg = login(email, password)
    if success:
        return True, f"✅ Account created! Welcome to Arthix, {name}."
    return False, msg


def get_token_info() -> dict:
    """
    Return decoded JWT metadata for display on the Profile page.
    Shows: issued_at, expires_at, time_remaining, algorithm, role.
    """
    token = st.session_state.get("access_token", "")
    if not token:
        return {}
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        iat = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        return {
            "issued_at":      iat.strftime("%d %b %Y, %H:%M UTC"),
            "expires_at":     exp.strftime("%d %b %Y, %H:%M UTC"),
            "time_remaining": _token_expiry_info(),
            "algorithm":      JWT_ALGORITHM,
            "token_type":     payload.get("type", "access"),
            "user_id":        payload.get("sub"),
            "role":           payload.get("role"),
            "is_expired":     now > exp,
        }
    except Exception:
        return {}


# ── Backward compatibility alias (replaces old check_auth) ────
def check_auth() -> bool:
    """Alias kept for any page still calling check_auth()."""
    return verify_session()
