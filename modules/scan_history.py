import json
import os
from datetime import datetime

HISTORY_FILE = "scan_history.json"

def save_scan(keyword, location, leads):
    """Saves a search result to the history file."""
    # Create entry
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keyword": keyword,
        "location": location,
        "count": len(leads),
        "leads": leads
    }
    
    # Load existing
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []
            
    # Prepend new scan (newest first)
    history.insert(0, entry)
    
    # Save
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_history():
    """Loads all past scans."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []
