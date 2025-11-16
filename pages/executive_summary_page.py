import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from charts import create_team_completion_donut

def get_column(df, col_name):
    """
    Helper function to get a column by its original name, even if it has a unique suffix.
    Returns the column name with the suffix that exists in the DataFrame.
    """
    if col_name in df.columns:
        return col_name

    matching_cols = [col for col in df.columns if col.startswith(f"{col_name}___")]
    if matching_cols:
        return matching_cols[0]

    return col_name

def has_column(df, col_name):
    """Check if a column exists by original name"""
    if col_name in df.columns:
        return True
    return any(col.startswith(f"{col_name}___") for col in df.columns)

@st.cache_data(ttl=300)
def load_google_sheet():
    """Load data from Google Sheet with caching"""
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)

        sheet_id = st.secrets.get("google_sheet_id", "1xENgMtZL5DSEHKFvYr34UZsJIDCxlTw-BbS3giYrHvw")

        try:
            sheet = client.open_by_key(sheet_id).worksheet("Otter_Tasks")
        except:
            sheet = client.open_by_key(sheet_id).sheet1

        data = sheet.get_all_values()

        if not data or len(data) < 2:
            return pd.DataFrame()

        headers = data[0]
        rows = data[1:]

        df = pd.DataFrame(rows, columns=headers)

        return df

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def calculate_executive_metrics(df):
    """Calculate executive-level metrics"""
    if df.empty or not has_column(df, "Status"):
        return {
            "active_tasks": 0,
            "in_progress_tasks": 0,
            "overdue_tasks": 0,
            "completion_rate": 0,
            "total_tasks": 0,
            "open_tasks": 0,
            "working_tasks": 0,
            "done_tasks": 0,
            "archived_tasks": 0
        }

    df_copy = df.copy()
    status_col = get_column(df_copy, "Status")
    df_copy[status_col] = df_copy[status_col].str.strip().str.lower()

    # Active tasks = Open + Working
    open_tasks = len(df_copy[df_copy[status_col].str.contains("open|not started|🔴", case=False, na=False)])
    working_tasks = len(df_copy[df_copy[status_col].str.contains("working|in progress|🟡", case=False, na=False)])
    done_tasks = len(df_copy[df_copy[status_col].str.contains("done|complete|🟢", case=False, na=False)])
    archived_tasks = len(df_copy[df_copy[status_col].str.contains("archived|archive", case=False, na=False)])

    active_tasks = open_tasks
    in_progress_tasks = working_tasks

    # Overdue tasks - tasks with Date Assigned > 30 days ago and still open/working
    overdue_tasks = 0
    if has_column(df_copy, "Date Assigned"):
        date_col = get_column(df_copy, "Date Assigned")
        today = datetime.now()

        for idx, row in df_copy.iterrows():
            status = row[status_col].lower()
            date_str = str(row[date_col]).strip()

            if status in ['open', 'working', 'in progress', 'not started'] and date_str:
                try:
                    assigned_date = datetime.strptime(date_str, "%Y-%m-%d")
                    days_old = (today - assigned_date).days
                    if days_old > 30:
                        overdue_tasks += 1
                except:
                    pass

    total_tasks = len(df_copy)
    completed_tasks = done_tasks + archived_tasks
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return {
        "active_tasks": active_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks,
        "completion_rate": round(completion_rate, 1),
        "total_tasks": total_tasks,
        "open_tasks": open_tasks,
        "working_tasks": working_tasks,
        "done_tasks": done_tasks,
        "archived_tasks": archived_tasks
    }

def render_executive_summary_page():
    """Render the Executive Summary page"""

    # Import Google Fonts and inject CSS using components.html for better rendering
    import streamlit.components.v1 as components

    components.html("""
        <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Questrial&display=swap" rel="stylesheet">
        <style>
        [data-testid="stMetricValue"]{font-family:'Marcellus',serif;font-size:2.5rem;color:#2B2B2B;}
        [data-testid="stMetricLabel"]{font-family:'Questrial',sans-serif;font-size:0.9rem;color:#474747;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;}
        [data-testid="metric-container"]{background:transparent;border:none;padding:0;}
        .stProgress>div>div>div{background:#6BCF7F!important;height:12px;border-radius:6px;}
        .stProgress>div>div{background:#6BCF7F!important;border-radius:6px;}
        .exec-metric-card{border-radius:16px;padding:32px 24px;text-align:center;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);cursor:pointer;}
        .exec-metric-card:hover{transform:translateY(-6px);box-shadow:0 12px 32px rgba(43,43,43,0.15)!important;}
        .exec-metric-label{font-family:"Questrial",sans-serif;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 12px 0;font-weight:600;}
        .exec-metric-value{font-family:"Marcellus",serif;font-size:3.5rem;margin:0;font-weight:400;line-height:1;}
        </style>
    """, height=0)

    # Page header
    st.markdown("""
        <h1 style='
            font-family: "Marcellus", serif;
            font-size: 2.5rem;
            font-weight: 400;
            color: #2B2B2B;
            margin: 0 0 8px 0;
            letter-spacing: -0.02em;
        '>Executive Summary</h1>
        <p style='
            font-family: "Questrial", sans-serif;
            font-size: 0.95rem;
            color: #918C86;
            margin: 0 0 32px 0;
            letter-spacing: 0.02em;
        '>High-level overview of task performance and completion metrics</p>
    """, unsafe_allow_html=True)

    # Load data
    df = load_google_sheet()

    if df.empty:
        st.warning("No data available to display.")
        return

    # Calculate metrics
    metrics = calculate_executive_metrics(df)

    # === COMPLETION METRICS - Luxury minimal KPI cards ===
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Questrial&display=swap" rel="stylesheet">
        <style>
        .kpi-card {
            background: linear-gradient(135deg, #FFFDFD 0%, #F4F4F4 100%);
            padding: 56px 40px;
            border-radius: 16px;
            border: 2px solid #E5E4E2;
            box-shadow: 0 8px 24px rgba(43, 43, 43, 0.06), 0 2px 6px rgba(43, 43, 43, 0.04);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
            position: relative;
            overflow: hidden;
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #2B2B2B 0%, #918C86 50%, #E5E4E2 100%);
            opacity: 0;
            transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .kpi-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 16px 48px rgba(43, 43, 43, 0.12), 0 4px 12px rgba(43, 43, 43, 0.08);
            border-color: #918C86;
        }
        .kpi-card:hover::before {
            opacity: 1;
        }
        </style>
        <h2 style='
            margin: 0 0 56px 0;
            font-size: 2rem;
            font-weight: 400;
            font-family: "Marcellus", serif;
            color: #2B2B2B;
            letter-spacing: -0.01em;
            text-align: center;
        '>Executive Overview</h2>
    """, unsafe_allow_html=True)

    # Top row: 4 key metrics - Luxury minimal style with ample spacing
    col1, sp1, col2, sp2, col3, sp3, col4 = st.columns([1, 0.15, 1, 0.15, 1, 0.15, 1])

    with col1:
        st.markdown(f"""
            <div class='kpi-card'>
                <p style='margin: 0 0 24px 0; font-size: 0.75rem; font-weight: 400; font-family: "Questrial", sans-serif; text-transform: uppercase; letter-spacing: 0.15em; color: #918C86;'>Open Tasks</p>
                <h2 style='margin: 0; font-size: 3.5rem; font-weight: 400; font-family: "Marcellus", serif; color: #2B2B2B; line-height: 1; letter-spacing: -0.01em;'>{metrics["open_tasks"]}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='kpi-card'>
                <p style='margin: 0 0 24px 0; font-size: 0.75rem; font-weight: 400; font-family: "Questrial", sans-serif; text-transform: uppercase; letter-spacing: 0.15em; color: #918C86;'>In Progress</p>
                <h2 style='margin: 0; font-size: 3.5rem; font-weight: 400; font-family: "Marcellus", serif; color: #2B2B2B; line-height: 1; letter-spacing: -0.01em;'>{metrics["working_tasks"]}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='kpi-card'>
                <p style='margin: 0 0 24px 0; font-size: 0.75rem; font-weight: 400; font-family: "Questrial", sans-serif; text-transform: uppercase; letter-spacing: 0.15em; color: #918C86;'>Complete</p>
                <h2 style='margin: 0; font-size: 3.5rem; font-weight: 400; font-family: "Marcellus", serif; color: #2B2B2B; line-height: 1; letter-spacing: -0.01em;'>{metrics["done_tasks"] + metrics["archived_tasks"]}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='kpi-card'>
                <p style='margin: 0 0 24px 0; font-size: 0.75rem; font-weight: 400; font-family: "Questrial", sans-serif; text-transform: uppercase; letter-spacing: 0.15em; color: #918C86;'>Completion Rate</p>
                <h2 style='margin: 0; font-size: 3.5rem; font-weight: 400; font-family: "Marcellus", serif; color: #2B2B2B; line-height: 1; letter-spacing: -0.01em;'>{metrics["completion_rate"]}%</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 80px 0;'></div>", unsafe_allow_html=True)

    # === TASK STATUS DISTRIBUTION ===
    st.markdown("""
        <h2 style='
            font-family: "Marcellus", serif;
            font-size: 1.8rem;
            font-weight: 400;
            color: #2B2B2B;
            margin: 48px 0 24px 0;
            letter-spacing: -0.01em;
        '>Task Status Distribution</h2>
    """, unsafe_allow_html=True)

    # Create donut chart with archived tasks - make it bigger
    donut_fig = create_team_completion_donut(
        metrics['open_tasks'],
        metrics['working_tasks'],
        metrics['done_tasks'],
        metrics['archived_tasks']
    )

    if donut_fig:
        # Update chart height to make it bigger
        donut_fig.update_layout(height=600)

        st.plotly_chart(
            donut_fig,
            use_container_width=True,
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'executive_task_status',
                    'height': 800,
                    'width': 1200,
                    'scale': 2
                }
            }
        )
