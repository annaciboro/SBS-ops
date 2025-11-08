#!/usr/bin/env python3
"""
ONE-TIME SCRIPT: Write demo data to Google Sheet permanently

WARNING: This will PERMANENTLY replace all real data in your Google Sheet with demo data!

Usage:
    python write_demo_data_to_sheet.py
"""

import streamlit as st
from demo_data_transformer import write_demo_data_to_sheet_permanently

# Load secrets from Streamlit
# This works because we're in the same directory as .streamlit/secrets.toml
import toml
import os

# Load secrets manually
secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

print("=" * 60)
print("WRITE DEMO DATA TO GOOGLE SHEET - ONE-TIME SCRIPT")
print("=" * 60)
print()
sheet_id = secrets.get('google_sheet_id', '1xENgMtZL5DSEHKFvYr34UZsJIDCxlTw-BbS3giYrHvw')
print("⚠️  WARNING: This will PERMANENTLY replace all data in:")
print(f"   Google Sheet ID: {sheet_id}")
print(f"   Worksheet: Otter_Tasks")
print()
print("The following transformations will be applied:")
print("   - Transcript ID → Random 5-6 digit numbers")
print("   - Person → Addison, Mark, Peter, Emily, Sarah")
print("   - Task → 60 unique business tasks (12 per project)")
print("   - Project → Investor Prep, Website Redesign, Internal Systems, Marketing, Product Launch 2025")
print("   - Status → Random mix of Open, Working, Done, Archived")
print("   - Date Assigned → Random dates in 2025")
print()

# Ask for confirmation
response = input("Are you ABSOLUTELY SURE you want to proceed? (type 'YES' to continue): ")

if response == "YES":
    print()
    success = write_demo_data_to_sheet_permanently(secrets)
    if success:
        print()
        print("=" * 60)
        print("✅ COMPLETE! Your Google Sheet now contains demo data only.")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("❌ Failed to write demo data. Check errors above.")
        print("=" * 60)
else:
    print()
    print("❌ Aborted. No changes made to Google Sheet.")
