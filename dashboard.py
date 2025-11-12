import os
import streamlit as st
import streamlit.components.v1 as components
import pages as pg
import time
import base64
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="SBS Ops",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# HANDLE LOGOUT - MUST BE BEFORE AUTHENTICATOR.LOGIN()
# ============================================
# Check if logout was requested - handle it BEFORE authenticator.login() restores session
if st.session_state.get('_logout_requested', False):
    # Clear ALL session state (including authentication) except the logout flag
    for key in list(st.session_state.keys()):
        if key not in ['_is_running_with_streamlit', '_logout_requested']:
            try:
                del st.session_state[key]
            except:
                pass
    # Now remove the logout flag
    del st.session_state['_logout_requested']
    # Force a rerun to properly reset everything
    st.rerun()

# ============================================
# AUTHENTICATION
# ============================================
# Load credentials from config.yaml
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
with open(config_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# SBS styled login page
if st.session_state.get("authentication_status") is None:
    # Import Google Fonts
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Questrial&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # SBS OPERATIONS header at top
    st.markdown("""
        <div style="text-align: center; padding-top: 3rem; margin-bottom: 3rem;">
            <div style="
                font-size: 64px;
                font-weight: 400;
                font-family: 'Marcellus', serif;
                letter-spacing: -0.01em;
                color: #2B2B2B;
                line-height: 1;
            ">SBS OPERATIONS</div>
            <div style="
                font-size: 16px;
                font-weight: 400;
                font-family: 'Questrial', sans-serif;
                color: #918C86;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                margin-top: 12px;
            ">Strategic Business Solutions</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* Login page background - Soft white */
        .main, section.main, [data-testid="stAppViewContainer"] {
            background: #FFFDFD !important;
            position: relative !important;
            min-height: 100vh !important;
        }

        /* Center everything with ULTRA massive side space */
        .main .block-container {
            max-width: 100% !important;
            padding-top: 8rem !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin: 0 auto !important;
            position: relative !important;
            z-index: 1 !important;
        }

        /* Center the form container */
        .main .block-container > div:first-child {
            display: flex !important;
            justify-content: center !important;
            align-items: flex-start !important;
            width: 100% !important;
        }

        /* Login box with minimalist border - CENTERED */
        section[data-testid="stForm"] {
            background: #F4F4F4 !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 16px !important;
            padding: 48px 40px !important;
            box-shadow:
                0 4px 16px rgba(43, 43, 43, 0.08),
                0 2px 8px rgba(0, 0, 0, 0.04) !important;
            border: 2px solid #E5E4E2 !important;
            position: relative !important;
            margin: 0 auto !important;
            width: 100% !important;
            max-width: 600px !important;
        }

        /* Force the form's parent containers to be narrow */
        section[data-testid="stForm"] > div,
        section[data-testid="stForm"] form {
            max-width: 100% !important;
        }

        /* Input fields - Override all Streamlit defaults */
        input,
        input[type="text"],
        input[type="password"],
        section[data-testid="stForm"] input,
        input[aria-invalid="false"],
        input[aria-invalid="true"],
        .st-ba.st-bb.st-bc.st-bd.st-be.st-bf.st-bg.st-bh.st-bi.st-bj input,
        div[data-baseweb="base-input"] input {
            border-radius: 14px !important;
            border: 2px solid #2B2B2B !important;
            border-color: #2B2B2B !important;
            border-style: solid !important;
            padding: 18px 24px !important;
            font-size: 15px !important;
            background: #ffffff !important;
            caret-color: #2B2B2B !important;
            outline: none !important;
            box-shadow: none !important;
        }

        input:focus,
        input[type="text"]:focus,
        input[type="password"]:focus,
        section[data-testid="stForm"] input:focus,
        input:focus-visible,
        input[type="text"]:focus-visible,
        input[type="password"]:focus-visible,
        input[aria-invalid="false"]:focus,
        input[aria-invalid="true"]:focus,
        .st-ba.st-bb.st-bc.st-bd.st-be.st-bf.st-bg.st-bh.st-bi.st-bj input:focus,
        div[data-baseweb="base-input"] input:focus {
            border: 2px solid #E5E4E2 !important;
            border-color: #E5E4E2 !important;
            border-style: solid !important;
            box-shadow: 0 0 0 4px rgba(229, 228, 226, 0.3) !important;
            outline: none !important;
            caret-color: #2B2B2B !important;
        }

        /* Remove any red error styling from Streamlit */
        input[aria-invalid="true"],
        input[aria-invalid="false"] {
            border: 2px solid #2B2B2B !important;
            border-color: #2B2B2B !important;
        }

        input[aria-invalid="true"]:focus,
        input[aria-invalid="false"]:focus {
            border: 2px solid #E5E4E2 !important;
            border-color: #E5E4E2 !important;
            box-shadow: 0 0 0 4px rgba(229, 228, 226, 0.3) !important;
        }

        /* Target Streamlit's baseweb input wrapper */
        div[data-baseweb="base-input"],
        div[data-baseweb="input"] {
            border: none !important;
            box-shadow: none !important;
        }

        /* Override any Streamlit emotion cache classes */
        [class*="st-emotion-cache"] input,
        [class*="st-ba"] input {
            border: 2px solid #2B2B2B !important;
            border-color: #2B2B2B !important;
        }

        [class*="st-emotion-cache"] input:focus,
        [class*="st-ba"] input:focus {
            border: 2px solid #E5E4E2 !important;
            border-color: #E5E4E2 !important;
            box-shadow: 0 0 0 4px rgba(229, 228, 226, 0.3) !important;
        }

        /* Center the submit button container - ULTRA AGGRESSIVE */
        section[data-testid="stForm"] [data-testid="stFormSubmitButton"],
        section[data-testid="stForm"] div[data-testid="stFormSubmitButton"],
        [data-testid="stFormSubmitButton"],
        div[data-testid="stFormSubmitButton"],
        .stFormSubmitButton,
        section[data-testid="stForm"] > div:last-child {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            text-align: center !important;
        }

        /* Login button - minimalist black with white text */
        button[kind="primary"],
        section[data-testid="stForm"] button[type="submit"],
        section[data-testid="stForm"] button,
        form button,
        form button[type="submit"],
        [data-testid="stForm"] button,
        [data-testid="stFormSubmitButton"] button,
        div[data-testid="stFormSubmitButton"] > button,
        [class*="stFormSubmitButton"] button {
            background: #474747 !important;
            background-color: #474747 !important;
            background-image: none !important;
            color: #FFFDFD !important;
            border: none !important;
            border-color: transparent !important;
            border-width: 0 !important;
            border-style: none !important;
            border-radius: 8px !important;
            padding: 16px 32px !important;
            font-family: 'Questrial', sans-serif !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            width: auto !important;
            min-width: 200px !important;
            max-width: 300px !important;
            display: inline-block !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(43, 43, 43, 0.2) !important;
            outline: none !important;
        }

        /* Force cream text on button and all nested elements */
        section[data-testid="stForm"] button,
        section[data-testid="stForm"] button *,
        section[data-testid="stForm"] button p,
        section[data-testid="stForm"] button div,
        section[data-testid="stForm"] button span,
        [data-testid="stFormSubmitButton"] button,
        [data-testid="stFormSubmitButton"] button *,
        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stFormSubmitButton"] button div,
        [data-testid="stFormSubmitButton"] button span,
        form button,
        form button *,
        form button p,
        form button div,
        form button span {
            color: #FFFDFD !important;
            text-transform: uppercase !important;
            font-size: 13px !important;
            letter-spacing: 0.1em !important;
            font-weight: 600 !important;
            font-family: 'Questrial', sans-serif !important;
        }

        /* Hover state - slightly lighter */
        button[kind="primary"]:hover,
        section[data-testid="stForm"] button:hover,
        form button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            background: #474747 !important;
            background-image: none !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(10, 75, 75, 0.4) !important;
            border: none !important;
            color: #FFFDFD !important;
        }

        /* Hover state text color */
        button[kind="primary"]:hover *,
        section[data-testid="stForm"] button:hover *,
        form button:hover *,
        [data-testid="stFormSubmitButton"] button:hover * {
            color: #FFFDFD !important;
        }

        /* Active/Clicked state - neon green with dark green text */
        button[kind="primary"]:active,
        section[data-testid="stForm"] button:active,
        section[data-testid="stForm"] button[type="submit"]:active,
        form button:active,
        [data-testid="stFormSubmitButton"] button:active {
            background: linear-gradient(135deg, #d4ff00 0%, #c8ff00 100%) !important;
            background-image: linear-gradient(135deg, #d4ff00 0%, #c8ff00 100%) !important;
            color: #474747 !important;
            transform: translateY(0) !important;
            box-shadow: 0 0 0 4px rgba(212, 255, 0, 0.3) !important;
            border: none !important;
        }

        /* Force dark green text when active */
        section[data-testid="stForm"] button:active,
        section[data-testid="stForm"] button:active *,
        [data-testid="stFormSubmitButton"] button:active,
        [data-testid="stFormSubmitButton"] button:active * {
            color: #474747 !important;
        }

        /* Password field container - needs relative positioning */
        div[data-baseweb="input"],
        div[data-baseweb="base-input"] {
            position: relative !important;
        }

        /* Password visibility toggle button - make it smaller and styled */
        button[kind="icon"],
        button[kind="iconButton"],
        div[data-baseweb="input"] button,
        section[data-testid="stForm"] button[kind="icon"],
        [data-testid="stForm"] button[kind="icon"] {
            background: transparent !important;
            background-color: transparent !important;
            background-image: none !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 6px !important;
            width: 36px !important;
            min-width: 36px !important;
            max-width: 36px !important;
            height: 36px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 !important;
            box-shadow: none !important;
            color: #E5E4E2 !important;
            position: absolute !important;
            right: 8px !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            z-index: 10 !important;
        }

        button[kind="icon"]:hover,
        button[kind="iconButton"]:hover,
        section[data-testid="stForm"] button[kind="icon"]:hover {
            background: rgba(77, 122, 64, 0.1) !important;
            color: #474747 !important;
            transform: translateY(-50%) scale(1.1) !important;
        }

        /* Ensure password input has padding for the button */
        input[type="password"] {
            padding-right: 50px !important;
        }

        /* Labels - Dark green */
        label,
        section[data-testid="stForm"] label,
        .stTextInput label,
        div[class*="stText"] label {
            color: #474747 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 8px !important;
        }

        /* Form title "Login" - Dark green - centered - multiple selectors */
        section[data-testid="stForm"] h1,
        section[data-testid="stForm"] h2,
        .stForm h1,
        form h1 {
            color: #474747 !important;
            font-weight: 700 !important;
            font-size: 32px !important;
            text-align: center !important;
            width: 100% !important;
        }

        /* Copyright footer at bottom */
        .copyright-footer {
            position: fixed;
            bottom: 16px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 11px;
            color: #6b7878;
            font-weight: 500;
            z-index: 999;
        }
        </style>
    """, unsafe_allow_html=True)

    # Copyright footer
    st.markdown("""
        <div class="copyright-footer">
            © 2025 SBS ARCHITECTED
        </div>
    """, unsafe_allow_html=True)

    # Render login form INSIDE the styling block
    authenticator.login(location="main", fields={"Form name": "Login"})

    # Check authentication status
    if st.session_state.get("authentication_status") is False:
        st.error("❌ Username or password is incorrect")

    # Stop execution - don't show the app
    st.stop()

# If authenticated, continue with the app
# ============================================
# GLOBAL STYLE STANDARDIZATION
# ============================================
st.markdown("""
    <style>
    /* COMPREHENSIVE FONT & SIZE STANDARDIZATION - Soft Minimalist Design */

    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Questrial&display=swap');

    /* Base font size for entire app */
    html, body, [class*="st-"] {
        font-family: 'Questrial', sans-serif !important;
        font-size: 16px !important;
    }

    /* Page headers (H1) - Welcome back, Téa */
    h1, .stMarkdown h1 {
        font-family: 'Marcellus', serif !important;
        font-size: 2rem !important;
        font-weight: 400 !important;
        line-height: 1.2 !important;
        color: #2B2B2B !important;
    }

    /* Section headers (H2) - Executive Overview - Left aligned */
    h2, .stMarkdown h2 {
        font-family: 'Marcellus', serif !important;
        font-size: 1.75rem !important;
        font-weight: 400 !important;
        line-height: 1.2 !important;
        color: #2B2B2B !important;
        text-align: left !important;
        margin: 24px 0 16px 0 !important;
    }

    /* Subsection headers (H3) */
    h3, .stMarkdown h3 {
        font-family: 'Marcellus', serif !important;
        font-size: 1.2rem !important;
        font-weight: 400 !important;
        line-height: 1.4 !important;
        color: #474747 !important;
    }

    /* Body text, paragraphs - BUT NOT BUTTONS */
    p:not(button p):not(button *),
    .stMarkdown p:not(button p):not(button *),
    div:not(button):not(button div):not(button *),
    span:not(button span):not(button *) {
        font-family: 'Questrial', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        color: #474747 !important;
    }

    /* ALL BUTTONS - Consistent sizing */
    button, .stButton button {
        font-family: 'Questrial', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }

    /* ALL PRIMARY BUTTONS - Minimalist Dark Grey */
    button[kind="primary"],
    button[data-testid="baseButton-primary"],
    .stButton > button[kind="primary"],
    div[data-testid="stButton"] > button[type="submit"] {
        background: #474747 !important;
        background-color: #474747 !important;
        border: none !important;
        color: #FFFDFD !important;
        font-weight: 500 !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(10, 75, 75, 0.15) !important;
        transition: all 0.3s ease !important;
    }

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    .stButton > button[kind="primary"]:hover,
    div[data-testid="stButton"] > button[type="submit"]:hover {
        background: #918C86 !important;
        color: #FFFDFD !important;
        box-shadow: 0 2px 6px rgba(10, 75, 75, 0.2) !important;
        transform: translateY(-1px) !important;
    }

    /* Fix hamburger menu - remove baby blue, make it teal */
    button[data-testid*="baseButton-header"] {
        background: white !important;
        border: 1.5px solid #474747 !important;
        color: #474747 !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
    }

    button[data-testid*="baseButton-header"]:hover {
        background: #f0f9f9 !important;
        border-color: #474747 !important;
    }

    /* Navigation buttons inside popover - FORCE consistent styling */
    div[data-testid="stPopover"] button,
    .stPopover button {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 10px 16px !important;
        margin: 4px 0 !important;
    }

    /* Remove ALL baby blue/light blue colors */
    [data-baseweb="popover"] {
        background: white !important;
    }

    /* Metric labels */
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Dataframe/table text */
    .dataframe, table {
        font-size: 0.85rem !important;
    }

    /* Input fields */
    input, textarea, select {
        font-size: 0.9rem !important;
    }

    /* Zen Minimal Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #e8eaed;
        border-radius: 3px;
        transition: background 0.3s ease;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #cbd5e0;
    }

    /* Firefox scrollbar styling */
    * {
        scrollbar-width: thin;
        scrollbar-color: #e8eaed transparent;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZE SESSION STATE
# ============================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Executive Summary"

# ============================================
# NAVIGATION BAR
# ============================================

# Get the logged-in user's name
user_name = st.session_state.get("name", "")
user_email = st.session_state.get("username", "")
is_anna = "anna" in user_name.lower() or user_email.lower() == "sbs.anna.ciboro@gmail.com"
is_jess = user_email.lower() == "jess@sbsglove.com"

# Different navigation based on user type
if is_anna:
    # Anna (admin) sees all pages
    pages_list = ["Overview", "Executive Summary", "My Tasks", "All Tasks", "Archive", "Sales Portal", "Investor Portal", "Logout"]
elif is_jess:
    # Jess sees team-related pages but not Sales/Investor portals
    pages_list = ["Overview", "Executive Summary", "My Tasks", "All Tasks", "Archive", "Logout"]
else:
    # Regular users only see Overview, My Tasks, Archive, and Logout
    pages_list = ["Overview", "Executive Summary", "My Tasks", "Archive", "Logout"]

nav_container = st.container()

with nav_container:
    # Navigation: Logo + Welcome message on left, hamburger menu on right
    cols = st.columns([6, 1])

    # Get first name for greeting
    first_name = user_name.split()[0] if user_name else "User"

    # Welcome message - minimalist
    with cols[0]:
        st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
            ">
                <h2 style="
                    font-size: 1.1rem;
                    font-weight: 600;
                    font-family: 'Marcellus', serif;
                    color: #2B2B2B;
                    margin: 0;
                    padding: 0;
                    line-height: 1.2;
                ">Welcome back, {first_name}</h2>
            </div>
        """, unsafe_allow_html=True)

    # Hamburger menu on the right
    with cols[1]:
        # Hamburger menu button styling - completely remove all borders and outlines
        st.markdown(f"""
            <style>
            /* Hamburger menu button - clean text only, no outline ever */
            button[data-testid*="baseButton-header"],
            button[data-testid*="baseButton-header"]:focus,
            button[data-testid*="baseButton-header"]:active,
            button[data-testid*="baseButton-header"]:focus-visible {{
                background: transparent !important;
                border: 2px solid #474747 !important;
                border-radius: 8px !important;
                outline: none !important;
                outline-width: 0 !important;
                outline-style: none !important;
                outline-color: transparent !important;
                padding: 10px 16px !important;
                width: 56px !important;
                height: 56px !important;
                box-shadow: none !important;
                transition: all 0.3s ease !important;
                cursor: pointer !important;
                font-size: 1.75rem !important;
                color: #918C86 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }}

            button[data-testid*="baseButton-header"]:hover {{
                background: rgba(122, 153, 0, 0.08) !important;
                color: #a8d900 !important;
                border: 2px solid #918C86 !important;
                outline: none !important;
                box-shadow: 0 2px 8px rgba(122, 153, 0, 0.25) !important;
                transform: translateY(-2px) !important;
            }}

            /* Also target the div container - position to left edge */
            div[data-testid="stPopover"],
            div[data-testid="stPopover"] > button {{
                outline: none !important;
                border: 2px solid #474747 !important;
                border-radius: 8px !important;
                width: 56px !important;
                min-width: 56px !important;
                max-width: 56px !important;
                height: 56px !important;
                min-height: 56px !important;
                max-height: 56px !important;
                padding: 0 !important;
                margin: 0 !important;
                margin-right: auto !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                overflow: hidden !important;
                flex-shrink: 0 !important;
            }}

            div[data-testid="stPopover"] > button:focus {{
                outline: none !important;
                border: 2px solid #474747 !important;
                box-shadow: none !important;
            }}

            div[data-testid="stPopover"] > button:hover {{
                border: 2px solid #918C86 !important;
                box-shadow: 0 2px 8px rgba(10, 75, 75, 0.2) !important;
                transform: translateY(-2px) !important;
            }}

            /* Make popover larger */
            div[data-testid="stPopover"] > div {{
                min-width: 300px !important;
            }}

            /* Standardize navigation button styling - ULTRA AGGRESSIVE override */
            /* Primary button (current page) - teal with white text */
            div[data-testid="stPopover"] button[kind="primary"],
            div[data-testid="stPopover"] button[type="submit"],
            .stPopover button[kind="primary"],
            .stPopover button[type="submit"] {{
                background: linear-gradient(135deg, #474747 0%, #918C86 100%) !important;
                background-color: #474747 !important;
                background-image: linear-gradient(135deg, #474747 0%, #918C86 100%) !important;
                color: white !important;
                border: none !important;
                border-color: transparent !important;
                font-weight: 600 !important;
                padding: 12px 20px !important;
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }}

            div[data-testid="stPopover"] button[kind="primary"]:hover,
            div[data-testid="stPopover"] button[type="submit"]:hover,
            .stPopover button[kind="primary"]:hover,
            .stPopover button[type="submit"]:hover {{
                background: linear-gradient(135deg, #918C86 0%, #106a6a 100%) !important;
                background-color: #918C86 !important;
                background-image: linear-gradient(135deg, #918C86 0%, #106a6a 100%) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 2px 8px rgba(10, 75, 75, 0.2) !important;
            }}

            /* Secondary button (other pages) - soft grey with dark teal border and text */
            div[data-testid="stPopover"] button[kind="secondary"],
            .stPopover button[kind="secondary"],
            div[data-testid="stPopover"] button:not([kind="primary"]):not([type="submit"]),
            .stPopover button:not([kind="primary"]):not([type="submit"]) {{
                background: #f5f7f8 !important;
                background-color: #f5f7f8 !important;
                background-image: none !important;
                color: #474747 !important;
                border: 1.5px solid #474747 !important;
                border-color: #474747 !important;
                font-weight: 500 !important;
                padding: 12px 20px !important;
                border-radius: 10px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 1px 3px rgba(10, 75, 75, 0.08) !important;
            }}

            div[data-testid="stPopover"] button[kind="secondary"]:hover,
            .stPopover button[kind="secondary"]:hover,
            div[data-testid="stPopover"] button:not([kind="primary"]):not([type="submit"]):hover,
            .stPopover button:not([kind="primary"]):not([type="submit"]):hover {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-color: #474747 !important;
                border-width: 1.5px !important;
                color: #474747 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 3px 10px rgba(10, 75, 75, 0.15) !important;
            }}
            </style>
        """, unsafe_allow_html=True)

        # Hamburger menu popover
        with st.popover("☰"):
                for page_name in pages_list:
                    if page_name == "Logout":
                        st.markdown("---")  # Separator before logout
                        if st.button("Logout", key="nav_logout", use_container_width=True):
                            # Set a flag to trigger logout
                            st.session_state['_logout_requested'] = True
                            st.rerun()
                    else:
                        # Navigation button
                        is_current = st.session_state.current_page == page_name
                        button_label = f"{'✓ ' if is_current else ''}{page_name}"

                        if st.button(button_label, key=f"nav_{page_name}", use_container_width=True, type="primary" if is_current else "secondary"):
                            st.session_state.current_page = page_name
                            st.rerun()

# Subtle minimalist accent bar under navigation - platinum gradient
st.markdown("""
    <div style='
        width: 100%;
        max-width: 100vw;
        margin: 0;
        padding: 0;
        height: 2px;
        background: linear-gradient(90deg,
            #E5E4E2 0%,
            #918C86 50%,
            #E5E4E2 100%);
        box-shadow: none;
    '></div>
""", unsafe_allow_html=True)

# Logo styling for navigation bar
st.markdown("""
<style>
.st-emotion-cache-iun7dp {
    padding: 0rem 0px 0.0rem 0.0rem !important;
    position: absolute !important;
    top: -3rem !important;
    right: 0px !important;
    transition: none !important;
    opacity: 0 !important;
}

.st-emotion-cache-7czcpc > img {
    border-radius: 0.0rem !important;
    width: 300% !important;
    max-width: 300% !important;
}

img, svg {
    border-radius: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# JavaScript to forcefully fix logo height, make nav sticky, AND force button styling
st.markdown("""
<script>
function forceLogoHeight() {
    const logo = document.querySelector('[data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] img');
    if (logo) {
        logo.removeAttribute('style');
        logo.style.cssText = 'width: auto !important; height: 140px !important; max-width: none !important; border-radius: 0px !important;';
    }
}

function makeNavSticky() {
    const nav = document.querySelector('[data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child');
    if (nav) {
        nav.style.position = 'fixed';
        nav.style.top = '0';
        nav.style.left = '0';
        nav.style.right = '0';
        nav.style.zIndex = '99999';
    }
}

function forceButtonStyling() {
    console.log('🔍 Starting forceButtonStyling()...');

    // Try multiple selectors and log each attempt
    const selector1 = document.querySelectorAll('[data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"]:first-child button');
    console.log('Selector 1 (stVerticalBlock): ' + selector1.length + ' buttons');

    const selector2 = document.querySelectorAll('.st-emotion-cache-5qfegl.e8vg11g2');
    console.log('Selector 2 (.st-emotion-cache-5qfegl.e8vg11g2): ' + selector2.length + ' buttons');

    const selector3 = document.querySelectorAll('button[kind="secondary"]');
    console.log('Selector 3 (kind="secondary"): ' + selector3.length + ' buttons');

    const selector4 = document.querySelectorAll('button[data-testid="stBaseButton-secondary"]');
    console.log('Selector 4 (stBaseButton-secondary): ' + selector4.length + ' buttons');

    // Get ALL navigation buttons using multiple selectors
    const navButtons = document.querySelectorAll(
        '[data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"]:first-child button, ' +
        '[class*="st-emotion-cache"] button[kind="secondary"], ' +
        '.st-emotion-cache-5qfegl.e8vg11g2, ' +
        '.st-emotion-cache-5qfegl, ' +
        '.e8vg11g2, ' +
        'button[data-testid="stBaseButton-secondary"]'
    );

    console.log('📊 TOTAL Found ' + navButtons.length + ' navigation buttons to style');

    navButtons.forEach((button) => {
        // Check if button is in navigation (not logout or other buttons)
        const isNavButton = button.closest('[data-testid="stVerticalBlock"]');
        if (!isNavButton) return;

        // Force transparent background and remove all borders except bottom
        button.style.setProperty('background', 'transparent', 'important');
        button.style.setProperty('background-color', 'transparent', 'important');
        button.style.setProperty('background-image', 'none', 'important');
        button.style.setProperty('border', 'none', 'important');
        button.style.setProperty('border-top', 'none', 'important');
        button.style.setProperty('border-left', 'none', 'important');
        button.style.setProperty('border-right', 'none', 'important');
        button.style.setProperty('border-bottom', '3px solid transparent', 'important');
        button.style.setProperty('box-shadow', 'none', 'important');
        button.style.setProperty('outline', 'none', 'important');
        button.style.setProperty('border-radius', '0px', 'important');
        button.style.setProperty('padding', '12px 24px 9px 24px', 'important');
        button.style.setProperty('font-size', '12px', 'important');
        button.style.setProperty('font-weight', '600', 'important');
        button.style.setProperty('text-transform', 'uppercase', 'important');
        button.style.setProperty('letter-spacing', '0.05em', 'important');
        button.style.setProperty('color', '#e8f5e9', 'important');
        button.style.setProperty('font-family', "'Inter', -apple-system, BlinkMacSystemFont, sans-serif", 'important');
        button.style.setProperty('transition', 'all 0.2s ease', 'important');
        button.style.setProperty('transform', 'translateY(0)', 'important');

        // Force uppercase on text content - target ALL nested elements INCLUDING EXACT STREAMLIT CLASSES
        const textElements = button.querySelectorAll(
            'p, div, span, ' +
            '[data-testid="stMarkdownContainer"], ' +
            '.st-emotion-cache-12j140x, ' +
            '.st-emotion-cache-12j140x.et2rgd20, ' +
            '.et2rgd20'
        );
        textElements.forEach(el => {
            el.style.setProperty('text-transform', 'uppercase', 'important');
            el.style.setProperty('color', '#e8f5e9', 'important');
            el.style.setProperty('font-variant-caps', 'normal', 'important');
            el.style.setProperty('font-size', '12px', 'important');
            el.style.setProperty('font-weight', '600', 'important');
        });

        // Also force on button itself
        button.style.setProperty('text-transform', 'uppercase', 'important');
        button.style.setProperty('font-variant-caps', 'normal', 'important');
    });

    console.log('Button styling applied!');
}

function applyAll() {
    forceLogoHeight();
    makeNavSticky();
    forceButtonStyling();
}

// Run multiple times to catch Streamlit re-renders with MORE aggressive timing
console.log('Starting button styling timers...');
setTimeout(applyAll, 10);
setTimeout(applyAll, 50);
setTimeout(applyAll, 100);
setTimeout(applyAll, 200);
setTimeout(applyAll, 500);
setTimeout(applyAll, 1000);
setTimeout(applyAll, 2000);
setTimeout(applyAll, 3000);
setTimeout(applyAll, 5000);

// Re-run on any Streamlit update
const observer = new MutationObserver(() => {
    console.log('DOM mutation detected, reapplying styles...');
    applyAll();
});
observer.observe(document.body, { childList: true, subtree: true });

console.log('Button styling observer initialized!');

// Expose applyAll globally for manual debugging
window.applyStrategic Business SolutionsStyling = applyAll;
console.log('✅ Run window.applyStrategic Business SolutionsStyling() in console to manually apply styling');
</script>
""", unsafe_allow_html=True)

# Remove spacing - Strategic Business Solutions Operations sits right against gradient bar
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ULTRA AGGRESSIVE NAVIGATION BUTTON OVERRIDE - LOAD LAST
st.markdown("""
<style>
/* PREMIUM LIGHT THEME NAVIGATION CONTAINER - Clean white with subtle gradient accent - STICKY */
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child {
    background: #ffffff !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06) !important;
    border-bottom: 3px solid #474747 !important;
    padding: 16px 48px !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 999 !important;
}

html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child::after {
    content: '' !important;
    position: absolute !important;
    bottom: -3px !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #474747 0%, #E5E4E2 50%, #918C86 100%) !important;
}

/* FINAL NUCLEAR OVERRIDE FOR NAVIGATION BUTTONS */
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button,
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button[kind="secondary"],
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button[kind="primary"],
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child [class*="st-emotion"] button,
html body div[data-testid="column"] button {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    border: none !important;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-bottom: 3px solid transparent !important;
    box-shadow: none !important;
    outline: none !important;
    border-radius: 0px !important;
    padding: 12px 24px 9px 24px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #e8f5e9 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    transition: all 0.2s ease !important;
    transform: translateY(0) !important;
    opacity: 0.8;
}

/* Force uppercase on all text inside buttons */
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button *,
html body div[data-testid="column"] button * {
    text-transform: uppercase !important;
    color: #e8f5e9 !important;
}

/* Hover - DARK THEME */
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button:hover,
html body div[data-testid="column"] button:hover {
    background: rgba(212, 255, 0, 0.1) !important;
    transform: translateY(-2px) !important;
    border-bottom: 3px solid transparent !important;
    color: #d4ff00 !important;
    opacity: 1 !important;
}

/* Active button - DARK THEME */
html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button[kind="primary"] {
    background: linear-gradient(135deg, #2d5016, #3a6520) !important;
    color: #d4ff00 !important;
    border-bottom: 3px solid #d4ff00 !important;
    opacity: 1 !important;
}

html body [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-child button[kind="primary"] * {
    color: #d4ff00 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# GET CURRENT DIRECTORY
# ============================================
current_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================
# LOAD SBS BRAND DNA (CSS + JS)
# ============================================

def inject_css(path):
    """Embed CSS into Streamlit app with aggressive cache busting."""
    if os.path.exists(path):
        with open(path) as f:
            css = f.read()
            # Add timestamp for cache busting
            cache_buster = int(time.time() * 1000)  # Millisecond precision
            st.markdown(f'<style id="sbs-css-{cache_buster}">{css}</style>', unsafe_allow_html=True)
            # VISIBLE indicator that CSS loaded
            st.markdown(f'<div style="position: fixed; bottom: 10px; right: 10px; background: #d4ff00; color: #000; padding: 5px 10px; border-radius: 5px; font-size: 10px; z-index: 999999;">CSS v{cache_buster}</div>', unsafe_allow_html=True)
            print(f"✅ Strategic Business Solutions CSS loaded with cache buster v{cache_buster}")
    else:
        st.error(f"⚠️ CSS file not found: {path}")

def inject_js(path):
    """Embed JS safely inside Streamlit iframe."""
    if os.path.exists(path):
        with open(path) as f:
            js = f.read()
            st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)
            print(f"✅ Strategic Business Solutions JS injected")
    else:
        st.warning(f"⚠️ JS file not found: {path}")

# --- Apply brand files ---
css_path = os.path.join(current_dir, "style.css")
js_path = os.path.join(current_dir, "static", "sbs.js")

inject_css(css_path)
inject_js(js_path)

# Force CSS variable override with MAXIMUM specificity to fix cached green colors
st.markdown("""
<style>
/* Maximum specificity CSS variable override */
html, html:root, :root, * {
    /* FORCE OVERRIDE - Soft Minimalist Color Palette */
    --sbs-cream: #FFFDFD !important;
    --sbs-light-grey: #F4F4F4 !important;
    --sbs-black: #2B2B2B !important;
    --sbs-dark-grey: #474747 !important;
    --sbs-tan-grey: #918C86 !important;
    --sbs-platinum: #E5E4E2 !important;

    /* FORCE OVERRIDE - Remove old colors */
    --sbs-lime: #2B2B2B !important;
    --sbs-lime-soft: #918C86 !important;
    --sbs-lime-dark: #474747 !important;
    --sbs-teal: #474747 !important;
    --sbs-teal-light: #918C86 !important;
    --sbs-teal-lighter: #E5E4E2 !important;

    /* Semantic Colors */
    --color-primary: #2B2B2B !important;
    --color-secondary: #474747 !important;
    --color-text: #2B2B2B !important;
    --color-text-muted: #918C86 !important;
    --color-bg: #FFFDFD !important;
    --color-card: #FFFDFD !important;
}

/* Direct color replacement for any hardcoded teal/lime colors */
[style*="#d4ff00"], [style*="#c8e66f"], [style*="#b8e600"],
[style*="#0a4b4b"], [style*="#5f8c8c"] {
    background: #FFFDFD !important;
    border-color: #E5E4E2 !important;
}

/* Force KPI card styles to use soft minimalist colors */
div[data-testid="stMetricValue"],
div[data-testid="stMetric"],
.kpi-card {
    background: linear-gradient(135deg, #FFFDFD 0%, #F4F4F4 100%) !important;
    border-left: 4px solid #E5E4E2 !important;
    border: 2px solid #E5E4E2 !important;
}
</style>
""", unsafe_allow_html=True)





# ============================================
# MAIN CONTENT AREA
# ============================================
content_container = st.container()

with content_container:
    functions = {
        "Overview": pg.show_dashboard,
        "Executive Summary": pg.render_executive_summary_page,
        "My Tasks": pg.show_tasks,
        "All Tasks": pg.show_analytics,
        "Archive": pg.show_archive,
        "Sales Portal": pg.show_sales_portal,
        "Investor Portal": pg.show_investor_portal,
    }

    go_to = functions.get(st.session_state.current_page)
    if go_to:
        go_to()
    else:
        st.error(f"⚠️ Page '{st.session_state.current_page}' is not yet implemented")
        st.info(f"Available pages: {', '.join(functions.keys())}")
