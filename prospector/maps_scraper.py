import requests
import streamlit as st
import random
import urllib.parse

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (RUTHLESS FILTER EDITION)
    Logic:
    1. Skips 'Perfect' businesses (High Rating + Website + Reviews).
    2. Sorts results to show the 'Worst' profiles first.
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
            # --- DATA EXTRACTION ---
            
            # Photos
            photo_data = result.get("photos_link")
            photos_count = 0
            if isinstance(photo_data, dict):
                photos_count = photo_data.get("count", 0)
            
            # Website (Deep Check)
            website = result.get("website")
            if not website: website = result.get("links", {}).get("website")
            
            # Rating
            try: rating = float(result.get("rating", 0))
            except: rating = 0.0
            
            # Reviews
            reviews = int(result.get("reviews", 0))

            # --- THE RUTHLESS FILTER (SKIP THE WINNERS) ---
            # If a business has a Website AND Good Rating (>4.0) AND Established (>20 reviews)
            # We SKIP them. They are not good prospects.
            if website and rating > 4.0 and reviews > 20:
                continue 

            # --- MAP LINK ---
            maps_url = result.get("gps_coordinates", {}).get("link")
            if not maps_url:
                query = urllib.parse.quote(f"{result.get('title')} {result.get('address')}")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

            # --- WEAKNESS SORTING SCORE ---
            # We calculate a score to push the WORST businesses to the top of the UI
            weakness_score = 0
            
            if not website: weakness_score += 1000  # No Website = #1 Priority
            if rating < 4.0: weakness_score += 500  # Bad Rating = #2 Priority
            if reviews < 10: weakness_score += 200  # New/Empty = #3 Priority
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
        
        # Sort by Weakness Score (Highest weakness first)
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
            "business_name": f"{keyword} Neglected",
            "place_id": "SIM_001",
            "rating": 2.5,
            "reviews": 4,
            "categories": [keyword],
            "phone": "+1 555-0101",
            "address": f"101 Main St, {location}",
            "website": None, # NO WEBSITE
            "photos_count": 1,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 1500
        },
        {
            "business_name": f"{location} Low Rated",
            "place_id": "SIM_002",
            "rating": 3.2,
            "reviews": 50,
            "categories": [keyword],
            "phone": "+1 555-0202",
            "address": f"200 Side St, {location}",
            "website": "https://exist.com",
            "photos_count": 5,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 500
        }
    ]
