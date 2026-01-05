import requests
import streamlit as st
import random
import urllib.parse

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (STRICT UNDERDOG EDITION)
    Logic:
    1. STRICT FILTER: Discards any business with Rating > 4.2.
    2. DEEP PHONE: Checks 3 different API fields to find the number.
    """
    
    api_key = st.secrets.get("SERPAPI_KEY")
    
    params = {
        "engine": "google_maps",
        "q": f"{keyword} in {location}",
        "type": "search",
        "ll": "@40.7455096,-74.0083012,14z" 
    }
    
    if api_key: params["api_key"] = api_key

    try:
        # 3. CALL API
        if not api_key: return _simulate_data(keyword, location)

        search = requests.get("https://serpapi.com/search", params=params)
        results = search.json()
        local_results = results.get("local_results", [])
        
        cleaned_leads = []
        
        for result in local_results:
            # --- 1. RATING FILTER (THE WALL) ---
            try: rating = float(result.get("rating", 0))
            except: rating = 0.0
            
            reviews = int(result.get("reviews", 0))

            # STRICT RULE: If Rating is > 4.2, SKIP IT.
            # We only want the strugglers.
            if rating > 4.2:
                continue 

            # --- 2. DEEP PHONE EXTRACTION ---
            phone = result.get("phone")
            if not phone: phone = result.get("phone_number")
            if not phone: phone = result.get("local_phone")
            if not phone: phone = "N/A"

            # --- 3. DATA EXTRACTION ---
            photo_data = result.get("photos_link")
            photos_count = 0
            if isinstance(photo_data, dict):
                photos_count = photo_data.get("count", 0)
            
            website = result.get("website")
            if not website: website = result.get("links", {}).get("website")
            
            # --- 4. MAP LINK ---
            maps_url = result.get("gps_coordinates", {}).get("link")
            if not maps_url:
                query = urllib.parse.quote(f"{result.get('title')} {result.get('address')}")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

            # --- 5. WEAKNESS SCORE ---
            # Prioritize: No Website > Low Rating > Low Reviews
            weakness_score = 0
            if not website: weakness_score += 1000 
            if rating < 3.5: weakness_score += 500
            if reviews < 10: weakness_score += 200
            if phone == "N/A": weakness_score += 100

            cleaned_leads.append({
                "business_name": result.get("title", "Unknown Business"),
                "place_id": result.get("place_id", str(random.randint(1000,9999))),
                "rating": rating,
                "reviews": reviews,
                "categories": [result.get("type", "Business")],
                "phone": phone,
                "address": result.get("address", "Unknown Address"),
                "website": website,
                "photos_count": photos_count,
                "maps_url": maps_url,
                "posts_active": False,
                "owner_response_rate": 0.5,
                "weakness_score": weakness_score
            })
        
        # Sort: Worst profiles first
        cleaned_leads.sort(key=lambda x: x['weakness_score'], reverse=True)
            
        return cleaned_leads

    except Exception as e:
        st.error(f"Scraping Error: {str(e)}")
        return []

def _simulate_data(keyword, location):
    """Simulation"""
    import time
    time.sleep(1)
    return [
        {
            "business_name": f"{keyword} Struggler",
            "place_id": "SIM_001",
            "rating": 3.2,
            "reviews": 8,
            "categories": [keyword],
            "phone": "+1 555-0101",
            "address": f"101 Main St, {location}",
            "website": None,
            "photos_count": 1,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 1500
        }
    ]
