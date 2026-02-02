import datetime
import os
import sys

def get_weekly_target():
    today = datetime.date.today()
    # Python's weekday: Mon=0, Sun=6.
    # We want Sunday to be the start of the week (or the identifier).
    # If today is Sunday (6), we use today.
    # If today is Mon-Sat (0-5), we want the *previous* Sunday?
    # User said: "Next Sunday (Feb 8) -> 2026-02-08".
    # So if today is Feb 1 (Sun), folder is Feb 1.
    # If today is Feb 2 (Mon), folder is Feb 1? Or does the new week start on Monday?
    # Usually "Weekly" implies a ISO week or a specific start day.
    # User said: "Next Sunday... create 2026-02-08".
    # This implies the folder date is the *Sunday* date.
    # Let's assume the folder covers Sunday to Saturday.
    
    # Calculate days to subtract to get back to Sunday
    # (weekday+1)%7 gives days since Sunday?
    # Sun(6): (6+1)%7 = 0. Correct.
    # Mon(0): (0+1)%7 = 1. Subtract 1 day -> Sunday.
    # Sat(5): (5+1)%7 = 6. Subtract 6 days -> Sunday.
    
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(days=idx)
    
    folder_name = f"{sun.strftime('%Y-%m-%d')}--ST-news"
    year = sun.strftime('%Y')
    
    # Updated path to match the standalone repo structure
    # Repo root is 10_Projects/ST_channnel
    base_path = "01_News"
    target_path = os.path.join(base_path, year, folder_name)
    summary_file = os.path.join(target_path, f"{folder_name}.md")
    
    print(f"TARGET_DIR={target_path}")
    print(f"SUMMARY_FILE={summary_file}")
    
    # Check if exists
    if os.path.exists(target_path):
        print("STATUS=EXISTS")
    else:
        print("STATUS=NEW")

if __name__ == "__main__":
    get_weekly_target()
