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

    # Import Google Fonts
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Questrial&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

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

    # === 3 KPI CARDS ===
    st.markdown("""
        <style>
        .exec-kpi-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 24px 0 32px 0;
        }

        .exec-kpi-card {
            background: linear-gradient(135deg, #FFFDFD 0%, #F4F4F4 100%);
            border: 2px solid #E5E4E2;
            border-radius: 16px;
            padding: 32px 24px;
            box-shadow: 0 4px 12px rgba(43, 43, 43, 0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .exec-kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(43, 43, 43, 0.12);
        }

        .exec-kpi-emoji {
            font-size: 2.5rem;
            margin-bottom: 12px;
            display: block;
        }

        .exec-kpi-value {
            font-family: 'Marcellus', serif;
            font-size: 3rem;
            font-weight: 400;
            color: #2B2B2B;
            margin: 8px 0;
            line-height: 1;
        }

        .exec-kpi-label {
            font-family: 'Questrial', sans-serif;
            font-size: 0.85rem;
            color: #918C86;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="exec-kpi-container">
            <div class="exec-kpi-card">
                <span class="exec-kpi-emoji">🟢</span>
                <div class="exec-kpi-value">{metrics['active_tasks']}</div>
                <div class="exec-kpi-label">Active</div>
            </div>
            <div class="exec-kpi-card">
                <span class="exec-kpi-emoji">🟡</span>
                <div class="exec-kpi-value">{metrics['in_progress_tasks']}</div>
                <div class="exec-kpi-label">In Progress</div>
            </div>
            <div class="exec-kpi-card">
                <span class="exec-kpi-emoji">🔴</span>
                <div class="exec-kpi-value">{metrics['overdue_tasks']}</div>
                <div class="exec-kpi-label">Overdue</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # === COMPLETION RATE BANNER ===
    completion_percentage = metrics['completion_rate']
    completed_count = metrics['done_tasks'] + metrics['archived_tasks']
    total_count = metrics['total_tasks']

    st.markdown(f"""
        <style>
        .completion-banner {{
            background: linear-gradient(135deg, #2B2B2B 0%, #474747 100%);
            border-radius: 16px;
            padding: 40px 48px;
            margin: 32px 0;
            box-shadow: 0 8px 24px rgba(43, 43, 43, 0.15);
            border: 3px solid #E5E4E2;
        }}

        .completion-percentage {{
            font-family: 'Marcellus', serif;
            font-size: 4rem;
            font-weight: 400;
            color: #FFFDFD;
            margin: 0;
            line-height: 1;
        }}

        .completion-label {{
            font-family: 'Questrial', sans-serif;
            font-size: 1.1rem;
            color: #E5E4E2;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin: 16px 0 8px 0;
            font-weight: 500;
        }}

        .completion-context {{
            font-family: 'Questrial', sans-serif;
            font-size: 0.95rem;
            color: #918C86;
            margin: 8px 0 0 0;
        }}
        </style>

        <div class="completion-banner">
            <div class="completion-percentage">{completion_percentage}%</div>
            <div class="completion-label">Completion Rate</div>
            <div class="completion-context">{completed_count} of {total_count} tasks completed or archived</div>
        </div>
    """, unsafe_allow_html=True)

    # === TASK STATUS DONUT CHART ===
    st.markdown("""
        <h2 style='
            font-family: "Marcellus", serif;
            font-size: 1.5rem;
            font-weight: 400;
            color: #2B2B2B;
            margin: 48px 0 24px 0;
            letter-spacing: -0.01em;
        '>Task Status Distribution</h2>
    """, unsafe_allow_html=True)

    # Create donut chart with archived tasks
    donut_fig = create_team_completion_donut(
        metrics['open_tasks'],
        metrics['working_tasks'],
        metrics['done_tasks'],
        metrics['archived_tasks']
    )

    if donut_fig:
        st.plotly_chart(donut_fig, use_container_width=True, config={
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
        })
