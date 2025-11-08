"""
Demo Data Transformer - Permanently replaces sensitive data with fake data
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Fake names pool (5 names)
FAKE_NAMES = [
    "Addison",
    "Mark",
    "Peter",
    "Emily",
    "Sarah"
]

# Fake tasks pool (60 tasks organized by 5 projects - 12 tasks per project)
FAKE_TASKS = [
    # INVESTOR PREP (12 tasks)
    "Prepare investor deck presentation",
    "Review financial projections and models",
    "Schedule investor pitch meetings",
    "Draft executive summary for investors",
    "Compile competitive market analysis",
    "Create valuation documentation",
    "Prepare board meeting materials",
    "Update cap table and ownership structure",
    "Review partnership agreements",
    "Develop investor FAQ document",
    "Prepare quarterly investor report",
    "Research potential investor leads",

    # WEBSITE REDESIGN (12 tasks)
    "Design new landing page mockups",
    "Audit current SEO performance",
    "Analyze website analytics and metrics",
    "Create wireframes for homepage",
    "Conduct user testing sessions",
    "Update brand guidelines for web",
    "Optimize mobile responsiveness",
    "Design email newsletter templates",
    "Create help center article templates",
    "Update site navigation structure",
    "Review accessibility compliance",
    "Develop content style guide",

    # INTERNAL SYSTEMS (12 tasks)
    "Update CRM database configuration",
    "Review security protocols and access",
    "Audit internal tool licenses",
    "Update employee handbook policies",
    "Review legal compliance checklist",
    "Configure automated reporting systems",
    "Update project management workflows",
    "Implement new communication tools",
    "Review data backup procedures",
    "Update IT infrastructure documentation",
    "Configure team collaboration spaces",
    "Streamline approval processes",

    # MARKETING (12 tasks)
    "Create social media content calendar",
    "Review Q1 marketing campaign results",
    "Optimize email marketing workflows",
    "Develop sales enablement materials",
    "Draft press release announcements",
    "Plan virtual conference presence",
    "Create case study content",
    "Plan webinar series schedule",
    "Analyze conversion funnel performance",
    "Design referral program structure",
    "Develop retention campaign strategy",
    "Conduct competitor pricing analysis",

    # PRODUCT LAUNCH 2025 (12 tasks)
    "Develop product roadmap Q2-Q3",
    "Update product documentation",
    "Create product launch timeline",
    "Plan product launch event details",
    "Update customer onboarding flow",
    "Conduct stakeholder interviews",
    "Analyze customer feedback data",
    "Create video tutorial scripts",
    "Update API documentation",
    "Design customer survey questions",
    "Prepare product demo materials",
    "Update pricing strategy for launch"
]

# Fake project names pool (5 projects)
FAKE_PROJECTS = [
    "Investor Prep",
    "Website Redesign",
    "Internal Systems",
    "Marketing",
    "Product Launch 2025"
]

# Status options with weights for realistic distribution
STATUS_OPTIONS = [
    "Open",
    "Working",
    "Done",
    "Archived"
]

def generate_demo_transcript_id(index):
    """Generate random transcript number (5-6 digits)"""
    return str(random.randint(10000, 999999))

def get_random_name():
    """Get a random fake name from the pool"""
    return random.choice(FAKE_NAMES)

def get_random_task():
    """Get a random fake task from the pool"""
    return random.choice(FAKE_TASKS)

def get_random_project():
    """Get a random fake project from the pool"""
    return random.choice(FAKE_PROJECTS)

def get_random_status():
    """Get a random status for realistic distribution"""
    return random.choice(STATUS_OPTIONS)

def get_random_date_2025():
    """Generate a random date in 2025 (Jan-Dec)"""
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

def transform_to_demo_data(df):
    """
    Transform sensitive data to demo data permanently.

    Args:
        df: DataFrame with real data

    Returns:
        DataFrame with demo data
    """
    if df is None or df.empty:
        return df

    # Create a copy to avoid modifying the original
    demo_df = df.copy()

    # Transform Transcript ID
    if 'Transcript ID' in demo_df.columns:
        demo_df['Transcript ID'] = [generate_demo_transcript_id(i) for i in range(len(demo_df))]

    # Transform Person column
    if 'Person' in demo_df.columns:
        demo_df['Person'] = [get_random_name() for _ in range(len(demo_df))]

    # Transform Task column - ensure unique tasks (no duplicates)
    if 'Task' in demo_df.columns:
        num_rows = len(demo_df)
        # Shuffle tasks for randomness
        shuffled_tasks = FAKE_TASKS.copy()
        random.shuffle(shuffled_tasks)
        # If we need more tasks than available, cycle through with reshuffling
        if num_rows <= len(FAKE_TASKS):
            demo_df['Task'] = shuffled_tasks[:num_rows]
        else:
            # Need to repeat tasks, but shuffle each cycle
            all_tasks = []
            while len(all_tasks) < num_rows:
                random.shuffle(shuffled_tasks)
                all_tasks.extend(shuffled_tasks)
            demo_df['Task'] = all_tasks[:num_rows]

    # Transform Project column
    if 'Project' in demo_df.columns:
        demo_df['Project'] = [get_random_project() for _ in range(len(demo_df))]

    # Transform Status column
    if 'Status' in demo_df.columns:
        demo_df['Status'] = [get_random_status() for _ in range(len(demo_df))]

    # Transform Date Assigned column
    if 'Date Assigned' in demo_df.columns:
        demo_df['Date Assigned'] = [get_random_date_2025() for _ in range(len(demo_df))]

    return demo_df


def write_demo_data_to_sheet_permanently(secrets):
    """
    ONE-TIME SCRIPT: Load real data, transform to demo, write back to Google Sheet

    WARNING: This will PERMANENTLY replace all data in your Google Sheet with demo data!

    Args:
        secrets: Streamlit secrets dictionary
    """
    import gspread
    from google.oauth2.service_account import Credentials

    print("⚠️  WARNING: This will PERMANENTLY replace all data in your Google Sheet!")
    print("Starting in 3 seconds...")
    import time
    time.sleep(3)

    try:
        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Load credentials
        creds_dict = secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

        # Authorize and open the sheet
        client = gspread.authorize(creds)
        sheet_id = secrets.get("google_sheet_id", "1xENgMtZL5DSEHKFvYr34UZsJIDCxlTw-BbS3giYrHvw")

        print(f"📊 Opening Google Sheet: {sheet_id}")

        # Open the Otter_Tasks worksheet
        try:
            sheet = client.open_by_key(sheet_id).worksheet("Otter_Tasks")
        except:
            sheet = client.open_by_key(sheet_id).sheet1

        print("📥 Loading current data...")
        # Get all values
        all_values = sheet.get_all_values()

        if not all_values or len(all_values) < 2:
            print("❌ Sheet is empty or has no data rows.")
            return False

        # First row is headers, rest is data
        headers = all_values[0]
        data_rows = all_values[1:]

        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers)

        print(f"✅ Loaded {len(df)} rows")
        print(f"📝 Columns: {', '.join(headers)}")

        # Transform to demo data
        print("🔄 Transforming to demo data...")
        demo_df = transform_to_demo_data(df)

        print(f"✅ Transformed {len(demo_df)} rows")

        # Convert DataFrame to list of lists (including headers)
        data = [demo_df.columns.tolist()] + demo_df.values.tolist()

        # Write back to sheet
        print("📤 Writing demo data back to Google Sheet...")
        sheet.clear()
        sheet.update(data, 'A1')

        print("✅ SUCCESS! Demo data written to Google Sheet permanently!")
        print(f"   - {len(demo_df)} rows transformed")
        print(f"   - Names: {', '.join(FAKE_NAMES)}")
        print(f"   - Projects: {', '.join(FAKE_PROJECTS[:5])}...")

        return True

    except Exception as e:
        print(f"❌ Error writing demo data to sheet: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
