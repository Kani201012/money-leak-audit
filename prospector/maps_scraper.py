import requests
import streamlit as st
import random
import urllib.parse

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (HUNTER EDITION)
    FILTERS: Removes "Perfect" businesses.
    SORTS: Shows "Weakest" prospects first.
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
            # --- EXTRACT DATA ---
            photo_data = result.get("photos_link")
            photos_count = 0
            if isinstance(photo_data, dict):
                photos_count = photo_data.get("count", 0)
            
            website = result.get("website")
            if not website: website = result.get("links", {}).get("website")
            
            try: rating = float(result.get("rating", 0))
            except: rating = 0.0
            
            reviews = int(result.get("reviews", 0))

            # --- HUNTER FILTER (THE NEW LOGIC) ---
            # If they are "Too Good", SKIP them.
            # Definition of "Too Good": Has Website AND > 4.5 Rating AND > 100 Reviews
            if website and rating >= 4.5 and reviews > 100:
                continue 

            # --- MAP LINK ---
            maps_url = result.get("gps_coordinates", {}).get("link")
            if not maps_url:
                query = urllib.parse.quote(f"{result.get('title')} {result.get('address')}")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

            # Calculate "Weakness Score" for Sorting (Higher = Better Prospect)
            # No Website = +50 pts
            # < 20 Reviews = +30 pts
            # Rating < 4.0 = +20 pts
            weakness_score = 0
            if not website: weakness_score += 50
            if reviews < 20: weakness_score += 30
            if rating < 4.0: weakness_score += 20
            if photos_count < 5: weakness_score += 10

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
                "weakness_score": weakness_score # Internal metric for sorting
            })
        
        # --- SORT LOGIC ---
        # Sort list so the "Weakest" (Highest Score) appear first
        cleaned_leads.sort(key=lambda x: x['weakness_score'], reverse=True)
            
        return cleaned_leads

    except Exception as e:
        st.error(f"Scraping Error: {str(e)}")
        return []

def _simulate_data(keyword, location):
    """Simulation: returns mostly weak leads for demo"""
    import time
    time.sleep(1)
    return [
        {
            "business_name": f"{keyword} Broken Profile",
            "place_id": "SIM_001",
            "rating": 3.2,
            "reviews": 8,
            "categories": [keyword],
            "phone": "+1 555-0101",
            "address": f"101 Main St, {location}",
            "website": None, # TARGET!
            "photos_count": 2,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 90
        },
        {
            "business_name": f"{location} {keyword} Inc",
            "place_id": "SIM_002",
            "rating": 4.0,
            "reviews": 25,
            "categories": [keyword],
            "phone": "+1 555-0202",
            "address": f"200 Side St, {location}",
            "website": "https://badsite.com",
            "photos_count": 5,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "weakness_score": 40
        }
    ]
