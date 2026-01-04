import requests
import streamlit as st
import random
import urllib.parse

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (V3.1 - ACCURACY & DEEP LINKS)
    Fixes: Photo Count Accuracy (0 instead of 5), Deep Website Extraction, Map Links.
    """
    
    # 1. GET API KEY
    api_key = st.secrets.get("SERPAPI_KEY")
    
    # 2. DEFINE PARAMS
    params = {
        "engine": "google_maps",
        "q": f"{keyword} in {location}",
        "type": "search",
        "ll": "@40.7455096,-74.0083012,14z" 
    }
    
    if api_key: params["api_key"] = api_key

    try:
        # 3. CALL API (Or Simulate if no key)
        if not api_key:
            return _simulate_data(keyword, location)

        search = requests.get("https://serpapi.com/search", params=params)
        
        if search.status_code != 200:
            st.error(f"API Error {search.status_code}: {search.text}")
            return []
            
        results = search.json()
        
        # 4. PARSE RESULTS SAFELY
        local_results = results.get("local_results", [])
        
        cleaned_leads = []
        
        for result in local_results:
            # --- 1. ACCURATE PHOTO EXTRACTION (THE FIX) ---
            # We explicitly default to 0 to catch "Visual Void" businesses
            photo_data = result.get("photos_link")
            photos_count = 0
            if isinstance(photo_data, dict):
                photos_count = photo_data.get("count", 0)
            
            # --- 2. ACCURATE WEBSITE EXTRACTION (THE FIX) ---
            # Sometimes SerpAPI hides the website in a 'links' dictionary
            website = result.get("website")
            if not website:
                website = result.get("links", {}).get("website")
            
            # --- 3. RATING SAFETY ---
            try:
                rating = float(result.get("rating", 0))
            except:
                rating = 0.0

            # --- 4. MAP LINK GENERATION ---
            # Try to get the direct link. If missing, construct a search query link.
            maps_url = result.get("gps_coordinates", {}).get("link")
            if not maps_url:
                query = f"{result.get('title')} {result.get('address')}"
                encoded_query = urllib.parse.quote(query)
                maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

            cleaned_leads.append({
                "business_name": result.get("title", "Unknown Business"),
                "place_id": result.get("place_id", str(random.randint(1000,9999))),
                "rating": rating,
                "reviews": int(result.get("reviews", 0)),
                "categories": [result.get("type", "Business")],
                "phone": result.get("phone", "N/A"),
                "address": result.get("address", "Unknown Address"),
                "website": website, 
                "photos_count": photos_count,
                "maps_url": maps_url,
                "posts_active": False, # API limitation, assume False for audit pressure
                "owner_response_rate": 0.5
            })
            
        return cleaned_leads

    except Exception as e:
        st.error(f"Scraping Error: {str(e)}")
        return []

def _simulate_data(keyword, location):
    """
    Fallback simulation if API Key fails or is missing.
    """
    import time
    time.sleep(1)
    return [
        {
            "business_name": f"{keyword} Experts of {location}",
            "place_id": "SIM_001",
            "rating": 4.9,
            "reviews": 120,
            "categories": [keyword],
            "phone": "+1 555-0101",
            "address": f"101 Main St, {location}",
            "website": "https://example.com",
            "photos_count": 50,
            "maps_url": "https://google.com/maps", 
            "posts_active": True,
            "owner_response_rate": 0.9
        },
        {
            "business_name": f"{location} {keyword} Services",
            "place_id": "SIM_002",
            "rating": 3.5,
            "reviews": 15,
            "categories": [keyword],
            "phone": "+1 555-0202",
            "address": f"200 Side St, {location}",
            "website": None,
            "photos_count": 0,
            "maps_url": "https://google.com/maps", 
            "posts_active": False,
            "owner_response_rate": 0.0
        }
    ]
