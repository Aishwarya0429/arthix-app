import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    /* ═══════════════════════════════════════════════════════════════
       BIZPULSE — GLOBAL STYLESHEET
       Sections:
         1.  Google Fonts & CSS Variables
         2.  Global Reset & Base
         3.  Streamlit Chrome Overrides
         4.  Layout — Main & Sidebar
         5.  Sidebar — Brand, Nav, Role Badge
         6.  Typography — Page Title, Subtitle, Section Headers
         7.  Cards — Base Card, Card Title
         8.  Metric Cards
         9.  Alert / Status Banners
         10. Badges
         11. Data Tables
         12. Form Inputs — Text, Number, Select, Textarea
         13. Buttons — Primary, Secondary, Danger
         14. Tabs
         15. Progress Bars
         16. Info Boxes
         17. Auth Page
         18. Forecast Tag
         19. File Upload Zone
         20. CSV Preview Panel
         21. Dividers
         22. Scrollbar
    ═══════════════════════════════════════════════════════════════ */


    /* ─────────────────────────────────────────────────────────────
       1. GOOGLE FONTS & CSS VARIABLES
    ───────────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

    :root {
        /* Backgrounds */
        --bg-primary:       #050D1A;
        --bg-secondary:     #071220;
        --bg-card:          #0B1A2E;
        --bg-card-hover:    #0E2038;
        --bg-card2:         #102440;
        --bg-input:         #0E2038;

        /* Brand Colors */
        --accent:           #0EA5E9;
        --accent-light:     #38BDF8;
        --accent-dark:      #0284C7;
        --accent2:          #06B6D4;
        --accent2-light:    #22D3EE;
        --accent3:          #F43F5E;
        --accent3-light:    #FB7185;
        --accent4:          #F59E0B;

        /* Semantic Colors */
        --success:          #06B6D4;
        --success-bg:       rgba(6, 182, 212, 0.10);
        --success-border:   rgba(6, 182, 212, 0.30);
        --danger:           #F43F5E;
        --danger-bg:        rgba(244, 63, 94, 0.10);
        --danger-border:    rgba(244, 63, 94, 0.30);
        --warning:          #F59E0B;
        --warning-bg:       rgba(245, 158, 11, 0.10);
        --warning-border:   rgba(245, 158, 11, 0.30);
        --info:             #0EA5E9;
        --info-bg:          rgba(14, 165, 233, 0.10);
        --info-border:      rgba(14, 165, 233, 0.30);

        /* Text */
        --text-primary:     #E0F2FE;
        --text-secondary:   #7AA2C0;
        --text-muted:       #3A5570;

        /* Borders & Effects */
        --border:           rgba(14, 165, 233, 0.20);
        --border-hover:     rgba(14, 165, 233, 0.50);
        --glow:             rgba(14, 165, 233, 0.15);
        --glow-strong:      rgba(14, 165, 233, 0.35);
        --shadow:           0 4px 20px rgba(0, 0, 0, 0.40);
        --shadow-lg:        0 12px 40px rgba(0, 0, 0, 0.60);

        /* Shape */
        --radius-xs:        4px;
        --radius-sm:        8px;
        --radius:           14px;
        --radius-lg:        20px;
        --radius-xl:        28px;

        /* Typography */
        --font-head:        'Syne', sans-serif;
        --font-body:        'DM Sans', sans-serif;

        /* Spacing scale */
        --space-xs:         0.25rem;
        --space-sm:         0.5rem;
        --space-md:         1rem;
        --space-lg:         1.5rem;
        --space-xl:         2rem;
        --space-2xl:        3rem;

        /* Transitions */
        --transition-fast:  0.15s ease;
        --transition-base:  0.25s ease;
        --transition-slow:  0.40s ease;
    }


    /* ─────────────────────────────────────────────────────────────
       2. GLOBAL RESET & BASE
    ───────────────────────────────────────────────────────────── */
    *, *::before, *::after {
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family:      var(--font-body) !important;
        background-color: var(--bg-primary) !important;
        color:            var(--text-primary) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    p, li, span {
        line-height: 1.65;
    }


    /* ─────────────────────────────────────────────────────────────
       3. STREAMLIT CHROME OVERRIDES
    ───────────────────────────────────────────────────────────── */
    #MainMenu      { visibility: hidden; }
    footer         { visibility: hidden; }
    header         { visibility: hidden; }
    .stDeployButton { display: none !important; }

    /* Remove default streamlit top padding */
    .stApp > header { height: 0 !important; }


    /* ─────────────────────────────────────────────────────────────
       4. LAYOUT — MAIN CONTENT & SIDEBAR
    ───────────────────────────────────────────────────────────── */
    .main .block-container {
        background:  linear-gradient(160deg, #050D1A 0%, #071828 60%, #050F1E 100%);
        padding:     2rem 2.5rem 3rem;
        max-width:   1400px;
        margin:      0 auto;
    }

    [data-testid="stSidebar"] {
        background:   var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
        min-width:    220px !important;
        max-width:    260px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background:  var(--bg-secondary) !important;
        padding-top: 1.5rem;
    }


    /* ─────────────────────────────────────────────────────────────
       5. SIDEBAR — BRAND, NAV, ROLE BADGE
    ───────────────────────────────────────────────────────────── */

    /* Brand row */
    .sidebar-brand {
        display:     flex;
        align-items: center;
        gap:         10px;
        padding:     0 1rem 0.4rem;
    }

    .brand-icon {
        font-size: 1.8rem;
        flex-shrink: 0;
    }

    .brand-text {
        font-family: var(--font-head) !important;
        font-size:   1.45rem;
        font-weight: 800;
        background:  linear-gradient(135deg, var(--accent-light), var(--accent2-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip:         text;
        letter-spacing:         -0.02em;
    }

    /* Business name below brand */
    .sidebar-biz {
        font-size:      0.78rem;
        color:          var(--text-secondary);
        padding:        0 1rem 0.4rem;
        letter-spacing: 0.02em;
        white-space:    nowrap;
        overflow:       hidden;
        text-overflow:  ellipsis;
    }

    /* Role pill */
    .role-badge {
        display:        inline-block;
        margin:         0 1rem 0.5rem;
        padding:        3px 12px;
        background:     var(--info-bg);
        border:         1px solid var(--info-border);
        border-radius:  20px;
        font-size:      0.68rem;
        color:          var(--accent);
        font-weight:    600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    /* Nav buttons */
    [data-testid="stSidebar"] .stButton > button {
        background:    transparent !important;
        border:        none !important;
        border-left:   3px solid transparent !important;
        color:         var(--text-secondary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.875rem !important;
        font-weight:   400 !important;
        text-align:    left !important;
        padding:       0.6rem 1rem 0.6rem 0.9rem !important;
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
        transition:    all var(--transition-fast) !important;
        width:         100% !important;
        margin-bottom: 2px !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background:   var(--glow) !important;
        border-left:  3px solid var(--accent) !important;
        color:        var(--text-primary) !important;
        padding-left: 1.2rem !important;
    }


    /* ─────────────────────────────────────────────────────────────
       6. TYPOGRAPHY — PAGE TITLE, SUBTITLE, SECTION HEADERS
    ───────────────────────────────────────────────────────────── */

    .page-title {
        font-family:  var(--font-head) !important;
        font-size:    2.1rem;
        font-weight:  800;
        background:   linear-gradient(130deg, #E0F2FE 30%, var(--accent) 70%, var(--accent2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip:         text;
        line-height:   1.1;
        margin-bottom: var(--space-xs);
        letter-spacing: -0.02em;
    }

    .page-subtitle {
        color:         var(--text-secondary);
        font-size:     0.875rem;
        font-weight:   300;
        margin-bottom: var(--space-lg);
        letter-spacing: 0.01em;
    }

    .section-title {
        font-family:   var(--font-head) !important;
        font-size:     1.05rem;
        font-weight:   700;
        color:         var(--text-primary);
        margin-bottom: var(--space-md);
        display:       flex;
        align-items:   center;
        gap:           8px;
    }

    .section-title::before {
        content:       '';
        display:       inline-block;
        width:         4px;
        height:        1em;
        background:    linear-gradient(180deg, var(--accent-light), var(--accent2));
        border-radius: 4px;
        flex-shrink:   0;
    }

    /* Legacy card-title alias (for existing page code) */
    .card-title {
        font-family:   var(--font-head) !important;
        font-size:     0.95rem;
        font-weight:   600;
        color:         var(--text-primary);
        margin-bottom: var(--space-sm);
        letter-spacing: 0.01em;
    }


    /* ─────────────────────────────────────────────────────────────
       7. CARDS — BASE CARD
    ───────────────────────────────────────────────────────────── */
    .card {
        background:    var(--bg-card);
        border:        1px solid var(--border);
        border-radius: var(--radius);
        padding:       1.3rem 1.5rem;
        margin-bottom: var(--space-md);
        transition:    border-color var(--transition-fast),
                       box-shadow   var(--transition-fast);
    }

    .card:hover {
        border-color: var(--border-hover);
        box-shadow:   var(--shadow);
    }

    /* Accent top-border variant */
    .card-accent {
        border-top: 3px solid var(--accent);
    }


    /* ─────────────────────────────────────────────────────────────
       8. METRIC CARDS
    ───────────────────────────────────────────────────────────── */
    .metric-card {
        background:    var(--bg-card);
        border:        1px solid var(--border);
        border-radius: var(--radius);
        padding:       1.3rem 1.5rem;
        position:      relative;
        overflow:      hidden;
        transition:    transform     var(--transition-base),
                       box-shadow    var(--transition-base),
                       border-color  var(--transition-fast);
    }

    /* Gradient top strip */
    .metric-card::before {
        content:          '';
        position:         absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background:       linear-gradient(90deg, var(--accent), var(--accent2), var(--accent-light));
        border-radius:    var(--radius) var(--radius) 0 0;
    }

    /* Subtle ambient glow behind card */
    .metric-card::after {
        content:          '';
        position:         absolute;
        inset:            0;
        background:       radial-gradient(ellipse at top left, var(--glow) 0%, transparent 70%);
        pointer-events:   none;
        opacity:          0;
        transition:       opacity var(--transition-base);
    }

    .metric-card:hover {
        transform:    translateY(-4px);
        box-shadow:   0 12px 35px var(--glow);
        border-color: var(--border-hover);
    }

    .metric-card:hover::after {
        opacity: 1;
    }

    .metric-icon {
        font-size:     1.8rem;
        margin-bottom: var(--space-sm);
        display:       block;
    }

    .metric-label {
        font-size:      0.72rem;
        color:          var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight:    600;
        margin-bottom:  var(--space-xs);
    }

    .metric-value {
        font-family:  var(--font-head) !important;
        font-size:    1.85rem;
        font-weight:  700;
        color:        var(--text-primary);
        line-height:  1;
        margin-bottom: var(--space-xs);
        letter-spacing: -0.02em;
    }

    .metric-delta-pos {
        color:       var(--success);
        font-size:   0.78rem;
        font-weight: 500;
    }

    .metric-delta-neg {
        color:       var(--danger);
        font-size:   0.78rem;
        font-weight: 500;
    }


    /* ─────────────────────────────────────────────────────────────
       9. ALERT / STATUS BANNERS
    ───────────────────────────────────────────────────────────── */
    .alert {
        display:       flex;
        align-items:   center;
        gap:           0.6rem;
        padding:       0.7rem 1rem;
        border-radius: var(--radius-sm);
        font-size:     0.84rem;
        font-weight:   400;
        margin-bottom: var(--space-sm);
        border:        1px solid transparent;
        line-height:   1.4;
    }

    .alert-success {
        background: var(--success-bg);
        border-color: var(--success-border);
        color: var(--success);
    }

    .alert-danger {
        background: var(--danger-bg);
        border-color: var(--danger-border);
        color: var(--danger);
    }

    .alert-warning {
        background: var(--warning-bg);
        border-color: var(--warning-border);
        color: var(--warning);
    }

    .alert-info {
        background: var(--info-bg);
        border-color: var(--info-border);
        color: var(--info);
    }


    /* ─────────────────────────────────────────────────────────────
       10. BADGES
    ───────────────────────────────────────────────────────────── */
    .badge {
        display:        inline-block;
        padding:        3px 10px;
        border-radius:  20px;
        font-size:      0.70rem;
        font-weight:    600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border:         1px solid transparent;
    }

    .badge-income  { background: var(--success-bg);  color: var(--success); border-color: var(--success-border); }
    .badge-expense { background: var(--danger-bg);   color: var(--danger);  border-color: var(--danger-border);  }
    .badge-profit  { background: var(--info-bg);     color: var(--accent);  border-color: var(--info-border);    }
    .badge-warning { background: var(--warning-bg);  color: var(--warning); border-color: var(--warning-border); }
    .badge-low     { background: var(--warning-bg);  color: var(--warning); border-color: var(--warning-border); }
    .badge-out     { background: var(--danger-bg);   color: var(--danger);  border-color: var(--danger-border);  }
    .badge-ok      { background: var(--success-bg);  color: var(--success); border-color: var(--success-border); }
    .badge-neutral { background: var(--bg-card2);    color: var(--text-secondary); border-color: var(--border); }


    /* ─────────────────────────────────────────────────────────────
       11. DATA TABLES
    ───────────────────────────────────────────────────────────── */
    .stDataFrame,
    [data-testid="stDataFrame"] {
        border-radius: var(--radius) !important;
        border:        1px solid var(--border) !important;
        overflow:      hidden !important;
        background:    var(--bg-card) !important;
    }

    thead tr th {
        background:     var(--bg-card2) !important;
        color:          var(--text-secondary) !important;
        font-size:      0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        font-weight:    600 !important;
        padding:        0.6rem 0.8rem !important;
        border-bottom:  1px solid var(--border) !important;
    }

    tbody tr td {
        font-size:  0.84rem !important;
        color:      var(--text-primary) !important;
        padding:    0.5rem 0.8rem !important;
        border-bottom: 1px solid rgba(108,99,255,0.06) !important;
    }

    tbody tr:hover td {
        background: var(--glow) !important;
    }


    /* ─────────────────────────────────────────────────────────────
       12. FORM INPUTS — TEXT, NUMBER, SELECT, TEXTAREA
    ───────────────────────────────────────────────────────────── */

    /* Text inputs */
    .stTextInput input,
    .stNumberInput input {
        background:    var(--bg-input) !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color:         var(--text-primary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.88rem !important;
        padding:       0.55rem 0.8rem !important;
        transition:    border-color var(--transition-fast),
                       box-shadow   var(--transition-fast) !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: var(--accent) !important;
        box-shadow:   0 0 0 3px var(--glow) !important;
        outline:      none !important;
    }

    /* Textarea */
    .stTextArea textarea {
        background:    var(--bg-input) !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color:         var(--text-primary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.88rem !important;
        resize:        vertical;
        transition:    border-color var(--transition-fast) !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow:   0 0 0 3px var(--glow) !important;
    }

    /* Selectbox / dropdown */
    [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div {
        background:    var(--bg-input) !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color:         var(--text-primary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.88rem !important;
    }

    [data-baseweb="select"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow:   0 0 0 3px var(--glow) !important;
    }

    /* Dropdown list */
    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background:    var(--bg-card2) !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* Date input */
    .stDateInput input {
        background:    var(--bg-input) !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color:         var(--text-primary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.88rem !important;
    }

    /* Input labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label,
    .stDateInput label,
    .stRadio label {
        color:          var(--text-secondary) !important;
        font-size:      0.80rem !important;
        font-weight:    500 !important;
        letter-spacing: 0.02em !important;
        margin-bottom:  var(--space-xs) !important;
    }

    /* Radio buttons */
    .stRadio [data-baseweb="radio"] {
        gap: 0.5rem;
    }

    .stRadio [data-baseweb="radio"] span {
        color: var(--text-primary) !important;
        font-size: 0.875rem !important;
    }


    /* ─────────────────────────────────────────────────────────────
       13. BUTTONS — PRIMARY, SECONDARY, DANGER
    ───────────────────────────────────────────────────────────── */

    /* Primary action button */
    button[kind="primary"],
    .stButton > button[kind="primary"] {
        background:    linear-gradient(135deg, var(--accent-dark), var(--accent), var(--accent2)) !important;
        border:        none !important;
        border-radius: var(--radius-sm) !important;
        color:         #ffffff !important;
        font-family:   var(--font-body) !important;
        font-size:     0.875rem !important;
        font-weight:   600 !important;
        padding:       0.6rem 1.4rem !important;
        box-shadow:    0 4px 15px rgba(108,99,255,0.35) !important;
        transition:    transform    var(--transition-fast),
                       box-shadow   var(--transition-fast) !important;
        letter-spacing: 0.02em !important;
    }

    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        transform:  translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(108,99,255,0.55) !important;
    }

    button[kind="primary"]:active,
    .stButton > button[kind="primary"]:active {
        transform:  translateY(0) !important;
        box-shadow: 0 2px 8px rgba(108,99,255,0.30) !important;
    }

    /* Secondary / default buttons */
    .stButton > button {
        background:    transparent !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color:         var(--text-secondary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.875rem !important;
        font-weight:   400 !important;
        transition:    all var(--transition-fast) !important;
    }

    .stButton > button:hover {
        border-color: var(--accent) !important;
        color:        var(--text-primary) !important;
        background:   var(--glow) !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background:    var(--success-bg) !important;
        border:        1px solid var(--success-border) !important;
        border-radius: var(--radius-sm) !important;
        color:         var(--success) !important;
        font-weight:   600 !important;
        font-size:     0.84rem !important;
        transition:    all var(--transition-fast) !important;
    }

    .stDownloadButton > button:hover {
        background: rgba(0,212,170,0.20) !important;
        box-shadow: 0 4px 14px rgba(0,212,170,0.25) !important;
    }


    /* ─────────────────────────────────────────────────────────────
       14. TABS
    ───────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background:    var(--bg-card) !important;
        border:        1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding:       4px !important;
        gap:           4px !important;
        margin-bottom: var(--space-md) !important;
    }

    .stTabs [data-baseweb="tab"] {
        background:    transparent !important;
        border-radius: var(--radius-xs) !important;
        color:         var(--text-secondary) !important;
        font-family:   var(--font-body) !important;
        font-size:     0.84rem !important;
        font-weight:   500 !important;
        padding:       0.45rem 1rem !important;
        transition:    all var(--transition-fast) !important;
        border:        none !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color:      var(--text-primary) !important;
        background: var(--glow) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-dark), var(--accent), var(--accent2)) !important;
        color:      #ffffff !important;
        box-shadow: 0 2px 10px rgba(108,99,255,0.35) !important;
    }


    /* ─────────────────────────────────────────────────────────────
       15. PROGRESS BARS
    ───────────────────────────────────────────────────────────── */
    .stProgress > div {
        background:    var(--bg-card2) !important;
        border-radius: 10px !important;
        height:        8px !important;
    }

    .stProgress > div > div {
        background:    linear-gradient(90deg, var(--accent), var(--accent2-light)) !important;
        border-radius: 10px !important;
        transition:    width 0.5s ease !important;
    }


    /* ─────────────────────────────────────────────────────────────
       16. INFO BOXES
    ───────────────────────────────────────────────────────────── */
    .info-box {
        background:    linear-gradient(135deg,
                           rgba(14,165,233,0.07),
                           rgba(6,182,212,0.04));
        border:        1px solid var(--border);
        border-left:   3px solid var(--accent2);
        border-radius: var(--radius-sm);
        padding:       0.75rem 1rem;
        font-size:     0.84rem;
        color:         var(--text-secondary);
        line-height:   1.55;
        margin-bottom: var(--space-md);
    }

    .info-box strong, .info-box b {
        color: var(--text-primary);
    }

    .info-box code {
        background:    var(--bg-card2);
        padding:       1px 6px;
        border-radius: var(--radius-xs);
        font-size:     0.82rem;
        color:         var(--accent2);
    }


    /* ─────────────────────────────────────────────────────────────
       17. AUTH PAGE
    ───────────────────────────────────────────────────────────── */
    .auth-logo {
        text-align:     center;
        font-family:    var(--font-head) !important;
        font-size:      2.2rem;
        font-weight:    800;
        background:     linear-gradient(135deg, var(--accent-light), var(--accent2-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip:         text;
        letter-spacing: -0.02em;
        margin-bottom:  var(--space-xs);
    }

    .auth-tagline {
        text-align:    center;
        font-size:     0.82rem;
        color:         var(--text-secondary);
        margin-bottom: var(--space-xl);
        font-weight:   300;
    }


    /* ─────────────────────────────────────────────────────────────
       18. FORECAST TAG
    ───────────────────────────────────────────────────────────── */
    .forecast-tag {
        display:        inline-flex;
        align-items:    center;
        gap:            8px;
        background:     linear-gradient(135deg,
                            rgba(14,165,233,0.15),
                            rgba(6,182,212,0.12));
        border:         1px solid rgba(14,165,233,0.35);
        border-radius:  var(--radius-sm);
        padding:        6px 14px;
        font-size:      0.82rem;
        color:          var(--accent-light);
        font-weight:    500;
        margin-bottom:  var(--space-md);
        letter-spacing: 0.01em;
    }


    /* ─────────────────────────────────────────────────────────────
       19. FILE UPLOAD ZONE
    ───────────────────────────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        background:    var(--bg-card) !important;
        border:        2px dashed var(--border) !important;
        border-radius: var(--radius) !important;
        padding:       var(--space-lg) !important;
        transition:    border-color var(--transition-base),
                       background   var(--transition-base) !important;
        text-align:    center;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent) !important;
        background:   var(--info-bg) !important;
    }

    [data-testid="stFileUploader"] section {
        border: none !important;
        background: transparent !important;
    }

    [data-testid="stFileUploader"] button {
        background:    var(--accent) !important;
        border:        none !important;
        color:         #fff !important;
        border-radius: var(--radius-sm) !important;
        font-weight:   600 !important;
        font-size:     0.84rem !important;
        padding:       0.4rem 1rem !important;
        transition:    opacity var(--transition-fast) !important;
    }

    [data-testid="stFileUploader"] button:hover {
        opacity: 0.85 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color:     var(--text-secondary) !important;
        font-size: 0.875rem !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
        border:     none !important;
    }

    /* Upload box wrapper used in CSV tab */
    .upload-zone {
        background:    var(--bg-card);
        border:        2px dashed var(--border);
        border-radius: var(--radius);
        padding:       2rem;
        text-align:    center;
        transition:    all var(--transition-base);
        margin-bottom: var(--space-md);
    }

    .upload-zone:hover {
        border-color: var(--accent);
        background:   var(--info-bg);
    }

    .upload-zone-icon {
        font-size:     3rem;
        margin-bottom: var(--space-sm);
        display:       block;
    }

    .upload-zone-title {
        font-family:   var(--font-head);
        font-size:     1.1rem;
        font-weight:   700;
        color:         var(--text-primary);
        margin-bottom: var(--space-xs);
    }

    .upload-zone-sub {
        font-size:  0.82rem;
        color:      var(--text-secondary);
        margin-bottom: var(--space-md);
    }


    /* ─────────────────────────────────────────────────────────────
       20. CSV PREVIEW PANEL
    ───────────────────────────────────────────────────────────── */
    .csv-preview-header {
        display:       flex;
        align-items:   center;
        gap:           10px;
        margin-bottom: var(--space-sm);
    }

    .csv-preview-badge {
        background:    var(--success-bg);
        border:        1px solid var(--success-border);
        border-radius: 20px;
        color:         var(--success);
        font-size:     0.72rem;
        font-weight:   600;
        padding:       2px 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .csv-stats-row {
        display:         flex;
        gap:             var(--space-md);
        margin-bottom:   var(--space-md);
        flex-wrap:       wrap;
    }

    .csv-stat-pill {
        background:    var(--bg-card2);
        border:        1px solid var(--border);
        border-radius: var(--radius-sm);
        padding:       0.4rem 0.9rem;
        font-size:     0.82rem;
        color:         var(--text-secondary);
        display:       flex;
        align-items:   center;
        gap:           6px;
    }

    .csv-stat-pill strong {
        color:       var(--text-primary);
        font-weight: 600;
    }

    /* Column mapping panel */
    .col-map-panel {
        background:    var(--bg-card2);
        border:        1px solid var(--border);
        border-radius: var(--radius-sm);
        padding:       var(--space-md) var(--space-md) var(--space-sm);
        margin-bottom: var(--space-md);
    }

    .col-map-label {
        font-size:      0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color:          var(--text-secondary);
        font-weight:    600;
        margin-bottom:  var(--space-sm);
    }


    /* ─────────────────────────────────────────────────────────────
       21. DIVIDERS
    ───────────────────────────────────────────────────────────── */
    hr {
        border:        none !important;
        border-top:    1px solid var(--border) !important;
        margin:        var(--space-lg) 0 !important;
        opacity:       1 !important;
    }


    /* ─────────────────────────────────────────────────────────────
       22. SCROLLBAR
    ───────────────────────────────────────────────────────────── */
    ::-webkit-scrollbar {
        width:  6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background:    var(--bg-secondary);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background:    var(--border);
        border-radius: 10px;
        transition:    background var(--transition-fast);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent);
    }

    </style>
    """, unsafe_allow_html=True)
