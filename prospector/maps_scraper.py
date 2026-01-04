import requests
import streamlit as st

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (REAL DATA EDITION)
    Connects to SerpAPI to fetch LIVE Google Maps data.
    """
    
    # 1. CHECK FOR API KEY
    # We look for the key in Streamlit secrets, or you can hardcode it for testing (not recommended for sharing)
    api_key = st.secrets.get("SERPAPI_KEY")
    
    if not api_key:
        # FALLBACK: If no key is found, show an error (or return mock data if you prefer)
        st.error("⚠️ No SerpAPI Key found! Please add it to Streamlit Secrets.")
        return []

    # 2. PREPARE THE SEARCH
    params = {
        "engine": "google_maps",
        "q": f"{keyword} in {location}",
        "api_key": api_key,
        "type": "search",
        "ll": "@40.7455096,-74.0083012,14z" # Optional: centers search, usually auto-detected by location text
    }

    try:
        # 3. CALL THE API
        search = requests.get("https://serpapi.com/search", params=params)
        results = search.json()
        
        # 4. PARSE REAL RESULTS
        local_results = results.get("local_results", [])
        
        cleaned_leads = []
        
        for result in local_results:
            # Extract real data points
            cleaned_leads.append({
                "business_name": result.get("title"),
                "place_id": result.get("place_id"),
                "rating": result.get("rating", 0),
                "reviews": result.get("reviews", 0),
                "categories": [result.get("type", "Business")],
                "phone": result.get("phone", "N/A"),
                "address": result.get("address", "Unknown"),
                "website": result.get("website"),
                "photos_count": result.get("photos_link", {}).get("count", 0) if "photos_link" in result else 5, # API often doesn't give exact count, we estimate or default
                "posts_active": False, # SerpAPI doesn't always show posts status, assuming False for strict audit
                "owner_response_rate": 0.5 # Placeholder as API doesn't provide this deep metric easily
            })
            
        return cleaned_leads

    except Exception as e:
        st.error(f"API Error: {e}")
        return []
