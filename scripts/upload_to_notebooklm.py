import os
import glob
import time
from playwright.sync_api import sync_playwright

def run():
    print("DEBUG: Starting simplified script execution...")
    # Configuration
    notebook_url = "https://notebooklm.google.com/notebook/0e65a56f-f5d9-4915-8d13-a81fbe114d9c"
    base_dir = os.path.abspath("01_News")
    # Using a NEW clean context for debugging
    user_data_dir = os.path.abspath(".auth/notebooklm_context_debug")
    
    md_files = []
    print(f"DEBUG: Scanning files in {base_dir}")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    print(f"DEBUG: Found {len(md_files)} md files.")

    with sync_playwright() as p:
        print(f"DEBUG: Launching browser with NEW context: {user_data_dir}")
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                # channel="chrome", # REMOVED: Use bundled chromium to avoid issues
                args=["--start-maximized", "--no-sandbox"],
                no_viewport=True
            )
            print("DEBUG: Browser launched successfully.")
        except Exception as e:
            print(f"DEBUG: Failed to launch browser: {e}")
            return
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print(f"DEBUG: Navigating to Notebook URL: {notebook_url}")
        try:
            page.goto(notebook_url, timeout=60000)
            print("DEBUG: Navigation initiated.")
        except Exception as e:
            print(f"DEBUG: Navigation error (ignored): {e}")

        print("DEBUG: Waiting for manual login or page load...")
        # Simple loop to keep browser open and show progress
        start_time = time.time()
        while time.time() - start_time < 300: # 5 mins
            if "signin" in page.url or "ServiceLogin" in page.url:
                print("DEBUG: Login page detected. Please log in.", end="\r")
            else:
                print(f"DEBUG: Current URL: {page.url[:50]}...", end="\r")
            time.sleep(1)
            
        browser.close()

if __name__ == "__main__":
    run()
