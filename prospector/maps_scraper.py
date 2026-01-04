import requests
import streamlit as st
import random
import urllib.parse
import time

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (DEEP DIVE EDITION)
    Scrapes Page 1 -> Page 2 -> Page 3 until it finds 'Weak' targets.
    """
    
    api_key = st.secrets.get("SERPAPI_KEY")
    
    # Configuration
    TARGET_LEAD_COUNT = 15  # Stop once we have this many leads
    MAX_PAGES = 3           # Don't burn more than 3 API credits per run
    
    cleaned_leads = []
    
    # If no key, return simulation
    if not api_key: return _simulate_data(keyword, location)

    # --- PAGINATION LOOP ---
    for page in range(MAX_PAGES):
        
        # Stop if we have enough leads
        if len(cleaned_leads) >= TARGET_LEAD_COUNT:
            break
            
        # Update Status on UI
        st.toast(f"Scanning Page {page + 1} for underdogs...", icon="🕵️")
        
        params = {
            "engine": "google_maps",
            "q": f"{keyword} in {location}",
            "type": "search",
            "ll": "@40.7455096,-74.0083012,14z",
            "start": page * 20, # Pagination Offset (0, 20, 40)
            "api_key": api_key
        }

        try:
            search = requests.get("https://serpapi.com/search", params=params)
            results = search.json()
            local_results = results.get("local_results", [])
            
            # If Google has no more results, stop.
            if not local_results:
                break
            
            for result in local_results:
                # --- DATA EXTRACTION ---
                photo_data = result.get("photos_link")
                photos_count = 0
                if isinstance(photo_data, dict):
                    photos_count = photo_data.get("count", 0)
                
                # Deep Website Check
                website = result.get("website")
                if not website: website = result.get("links", {}).get("website")
                
                try: rating = float(result.get("rating", 0))
                except: rating = 0.0
                
                reviews = int(result.get("reviews", 0))

                # --- THE FILTER (Skip the Winners) ---
                # If they are established (Website + >4.5 Stars + >50 Reviews), skip them.
                # We want the ones struggling on Page 2 and 3.
                if website and rating > 4.5 and reviews > 50:
                    continue 

                # --- MAP LINK ---
                maps_url = result.get("gps_coordinates", {}).get("link")
                if not maps_url:
                    query = urllib.parse.quote(f"{result.get('title')} {result.get('address')}")
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

                # --- WEAKNESS SCORE ---
                weakness_score = 0
                if not website: weakness_score += 1000  # Gold Mine
                if rating < 4.0: weakness_score += 500  # Reputation Fix
                if reviews < 10: weakness_score += 200  # New Biz
                if photos_count < 5: weakness_score += 50

                cleaned_leads.append({
                    "business_name": result.get("title", "Unknown Business"),
                    "place_id": result.get("place_id", str(random.randint(1000,9999))),
                    "rating": rating,
                    "reviews": reviews,
                    "categories": [result.get("type", "Business")],
                    "phone": result.get("phone", "N/A"),
                    "address": result.get("address", "Unknown Address"),
                    "website": website,
                    "photos_count": photos_count,
                    "maps_url": maps_url,
                    "posts_active": False,
                    "owner_response_rate": 0.5,
                    "weakness_score": weakness_score
                })
                
        except Exception as e:
            st.error(f"Error on Page {page+1}: {str(e)}")
            break
            
        # Be polite to the API (Optional)
        time.sleep(0.5)
    
    # Sort final list: Worst Profiles First
    cleaned_leads.sort(key=lambda x: x['weakness_score'], reverse=True)
    
    return cleaned_leads

def _simulate_data(keyword, location):
    """Simulation"""
    import time
    time.sleep(1)
    return [
        {
            "business_name": f"{keyword} No-Site",
            "place_id": "SIM_001",
            "rating": 3.0,
            "reviews": 5,
            "categories": [keyword],
            "phone": "+1 555-0101",
            "address": f"2nd Page St, {location}",
            "website": None,
            "photos_count": 1,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 1500
        },
        {
            "business_name": f"{location} {keyword} Low Rated",
            "place_id": "SIM_002",
            "rating": 2.8,
            "reviews": 40,
            "categories": [keyword],
            "phone": "+1 555-0202",
            "address": f"Back Alley, {location}",
            "website": "https://badsite.com",
            "photos_count": 3,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 500
        }
    ]
