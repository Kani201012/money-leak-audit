import requests
import streamlit as st
import random
import urllib.parse
import time

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (DEEP TRAWL EDITION)
    Scans up to 10 Pages (200 listings) to find the rare Low-Rated gems.
    Strictly filters out anything > 4.2 Stars.
    """
    
    api_key = st.secrets.get("SERPAPI_KEY")
    
    # CONFIGURATION: GO DEEP
    TARGET_LEAD_COUNT = 50  # Aim for 50 bad businesses
    MAX_PAGES = 10          # Scan up to 200 businesses (Deep Trawl)
    
    cleaned_leads = []
    seen_place_ids = set()
    
    if not api_key: return _simulate_data(keyword, location)

    for page in range(MAX_PAGES):
        
        # Stop if we have enough
        if len(cleaned_leads) >= TARGET_LEAD_COUNT: break
            
        st.toast(f"Deep Trawl: Scanning Page {page + 1}...", icon="🦈")
        
        params = {
            "engine": "google_maps",
            "q": f"{keyword} in {location}",
            "type": "search",
            "ll": "@40.7455096,-74.0083012,14z",
            "start": page * 20, 
            "api_key": api_key
        }

        try:
            search = requests.get("https://serpapi.com/search", params=params)
            results = search.json()
            local_results = results.get("local_results", [])
            
            if not local_results: break
            
            for result in local_results:
                
                # Deduping
                pid = result.get("place_id")
                if not pid: pid = str(random.randint(10000,99999))
                if pid in seen_place_ids: continue
                seen_place_ids.add(pid)

                # Rating Extraction
                try: rating = float(result.get("rating", 0))
                except: rating = 0.0
                
                reviews = int(result.get("reviews", 0))

                # --- THE STRICT FILTER (The Wall) ---
                # If rating is > 4.2, THROW IT AWAY.
                # We only want 4.2, 4.1, 3.8, etc.
                if rating > 4.2:
                    continue 

                # --- DATA EXTRACTION ---
                photo_data = result.get("photos_link")
                photos_count = 0
                if isinstance(photo_data, dict):
                    photos_count = photo_data.get("count", 0)
                
                if photos_count == 0 and result.get("thumbnail"): photos_count = 1
                if photos_count == 0 and result.get("images"): photos_count = len(result.get("images"))

                website = result.get("website")
                if not website: website = result.get("links", {}).get("website")
                if not website: website = result.get("reservations_link")

                phone = result.get("phone")
                if not phone: phone = result.get("phone_number")
                if not phone: phone = "N/A"

                maps_url = result.get("gps_coordinates", {}).get("link")
                if not maps_url:
                    query = urllib.parse.quote(f"{result.get('title')} {result.get('address')}")
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

                # WEAKNESS SCORE
                weakness_score = 0
                if not website: weakness_score += 1000 
                if rating < 3.5: weakness_score += 500
                if reviews < 10: weakness_score += 200
                if photos_count < 5: weakness_score += 100

                cleaned_leads.append({
                    "business_name": result.get("title", "Unknown"),
                    "place_id": pid,
                    "rating": rating,
                    "reviews": reviews,
                    "categories": [result.get("type", "Business")],
                    "phone": phone,
                    "address": result.get("address", "Unknown"),
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
            
        time.sleep(0.5)
    
    cleaned_leads.sort(key=lambda x: x['weakness_score'], reverse=True)
    return cleaned_leads

def _simulate_data(keyword, location):
    import time
    time.sleep(1)
    return [
        {
            "business_name": f"{keyword} Struggler",
            "place_id": "SIM_001",
            "rating": 3.2,
            "reviews": 8,
            "categories": [keyword],
            "phone": "555-0101",
            "address": f"101 Main St, {location}",
            "website": None,
            "photos_count": 1,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 1500
        }
    ]
