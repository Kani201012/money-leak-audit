import json
import os
import pandas as pd

DB_FILE = "leads_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_lead(lead_data):
    db = load_db()
    # Check for duplicates
    if any(l['place_id'] == lead_data['place_id'] for l in db):
        return False
    
    # Add CRM fields
    lead_data['status'] = "New Lead"
    lead_data['notes'] = ""
    lead_data['win_probability'] = "High" if lead_data['rating'] < 4.0 else "Medium"
    lead_data['estimated_value'] = 2000 # Default retainer value
    
    db.append(lead_data)
    save_db(db)
    return True

def update_lead_status(place_id, new_status):
    db = load_db()
    for lead in db:
        if lead['place_id'] == place_id:
            lead['status'] = new_status
    save_db(db)

def delete_lead(place_id):
    db = load_db()
    db = [l for l in db if l['place_id'] != place_id]
    save_db(db)

def get_metrics():
    db = load_db()
    df = pd.DataFrame(db)
    if df.empty:
        return 0, 0, 0
    
    pipeline_value = df['estimated_value'].sum()
    active_leads = len(df)
    return pipeline_value, active_leads
