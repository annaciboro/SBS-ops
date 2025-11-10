"""
UI Helper Functions for SBS Dashboard
Provides reusable UI components and formatting utilities
"""

def get_status_badge(status):
    """
    Generate HTML for a colored status badge

    Args:
        status (str): Task status (Open, Working, Done, Archived, etc.)

    Returns:
        str: HTML for the status badge
    """
    if not status or status.strip() == "":
        return ""

    status_lower = status.strip().lower()

    # Define status colors matching soft minimalist palette
    if status_lower in ['done', 'complete', 'completed', '🟢']:
        bg_color = '#918C86'  # Tan grey for completed
        text_color = '#FFFDFD'  # Cream text
        display_text = '✓ Done'
    elif status_lower in ['working', 'in progress', 'in-progress', 'progress']:
        bg_color = '#E5E4E2'  # Platinum for in progress
        text_color = '#2B2B2B'  # Black text
        display_text = '→ In Progress'
    elif status_lower in ['open', 'not started', 'todo', 'to do']:
        bg_color = '#F4F4F4'  # Light grey for open
        text_color = '#474747'  # Dark grey text
        display_text = '○ Open'
    elif status_lower in ['archived', 'archive']:
        bg_color = '#474747'  # Dark grey for archived
        text_color = '#FFFDFD'  # Cream text
        display_text = '✕ Archived'
    else:
        # Default for unknown statuses
        bg_color = '#F4F4F4'
        text_color = '#2B2B2B'
        display_text = status.title()

    badge_html = f"""
    <span style='
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        background-color: {bg_color};
        color: {text_color};
        font-family: "Questrial", sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        white-space: nowrap;
    '>{display_text}</span>
    """

    return badge_html


def format_relative_date(date_str):
    """
    Convert date string to relative format (e.g., '2 days ago', 'Tomorrow')

    Args:
        date_str (str): Date string in format YYYY-MM-DD

    Returns:
        str: Formatted relative date string
    """
    from datetime import datetime, timedelta

    if not date_str or date_str.strip() == "":
        return ""

    try:
        # Parse the date
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        else:
            date_obj = date_str

        # Get current date (no time component)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        target_date = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)

        # Calculate difference
        diff = (target_date - today).days

        # Format based on difference
        if diff == 0:
            return "Today"
        elif diff == 1:
            return "Tomorrow"
        elif diff == -1:
            return "Yesterday"
        elif diff > 1 and diff <= 7:
            return f"In {diff} days"
        elif diff < -1 and diff >= -7:
            return f"{abs(diff)} days ago"
        elif diff > 7 and diff <= 30:
            weeks = diff // 7
            return f"In {weeks} week{'s' if weeks > 1 else ''}"
        elif diff < -7 and diff >= -30:
            weeks = abs(diff) // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif diff > 30:
            return date_obj.strftime("%b %d, %Y")
        else:
            return date_obj.strftime("%b %d, %Y")
    except:
        # If parsing fails, return original string
        return date_str


def create_global_search():
    """
    Create a global search bar component

    Returns:
        str: HTML/CSS for the search bar
    """
    search_html = """
    <style>
    .global-search-container {
        margin: 24px 0 32px 0;
    }

    .search-input-wrapper {
        position: relative;
        max-width: 600px;
    }

    .search-icon {
        position: absolute;
        left: 16px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        fill: #918C86;
        pointer-events: none;
    }

    .global-search-input {
        width: 100%;
        padding: 14px 16px 14px 48px;
        font-family: 'Questrial', sans-serif;
        font-size: 0.95rem;
        color: #2B2B2B;
        background: #FFFDFD;
        border: 2px solid #E5E4E2;
        border-radius: 12px;
        outline: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(43, 43, 43, 0.03);
    }

    .global-search-input:focus {
        border-color: #918C86;
        box-shadow: 0 4px 16px rgba(145, 140, 134, 0.15);
    }

    .global-search-input::placeholder {
        color: #918C86;
    }
    </style>

    <div class="global-search-container">
        <div class="search-input-wrapper">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
            <input
                type="text"
                class="global-search-input"
                placeholder="Search tasks, projects, or assignees..."
                id="global-task-search"
            />
        </div>
    </div>
    """

    return search_html


def create_fab_button():
    """
    Create a floating action button (FAB) with quick actions menu

    Returns:
        str: HTML/CSS for the FAB
    """
    fab_html = """
    <style>
    /* Floating Action Button */
    .fab-container {
        position: fixed;
        bottom: 32px;
        right: 32px;
        z-index: 9999;
    }

    .fab-button {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2B2B2B 0%, #474747 100%);
        box-shadow: 0 4px 16px rgba(43, 43, 43, 0.3), 0 2px 8px rgba(43, 43, 43, 0.2);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fab-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 24px rgba(43, 43, 43, 0.4), 0 4px 12px rgba(43, 43, 43, 0.3);
        background: linear-gradient(135deg, #474747 0%, #2B2B2B 100%);
    }

    .fab-button svg {
        width: 24px;
        height: 24px;
        fill: #FFFDFD;
    }

    /* Quick actions menu */
    .fab-menu {
        position: absolute;
        bottom: 72px;
        right: 0;
        background: #FFFDFD;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(43, 43, 43, 0.15);
        padding: 8px;
        min-width: 200px;
        display: none;
        border: 2px solid #E5E4E2;
    }

    .fab-container:hover .fab-menu {
        display: block;
    }

    .fab-menu-item {
        padding: 12px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s;
        font-family: 'Questrial', sans-serif;
        font-size: 0.9rem;
        color: #2B2B2B;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .fab-menu-item:hover {
        background: #F4F4F4;
    }

    .fab-menu-item svg {
        width: 18px;
        height: 18px;
        fill: #474747;
    }
    </style>

    <div class="fab-container">
        <div class="fab-menu">
            <div class="fab-menu-item" onclick="window.location.reload();">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
                Refresh Data
            </div>
            <div class="fab-menu-item">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                Add Task
            </div>
            <div class="fab-menu-item">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2z"/></svg>
                Export CSV
            </div>
        </div>
        <button class="fab-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
            </svg>
        </button>
    </div>
    """

    return fab_html
