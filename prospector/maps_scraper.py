import requests
import streamlit as st
import random
import urllib.parse
import time

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (V5.0 - MEDICAL/SERVICE CONTEXT AWARE)
    Updates:
    1. Checks 'reservations_link' (Book Online) if website is missing.
    2. Handles "1 Photo" detection more gracefully.
    """
    
    api_key = st.secrets.get("SERPAPI_KEY")
    
    # Config
    TARGET_LEAD_COUNT = 30
    MAX_PAGES = 5
    
    cleaned_leads = []
    seen_place_ids = set()
    
    if not api_key: return _simulate_data(keyword, location)

    for page in range(MAX_PAGES):
        if len(cleaned_leads) >= TARGET_LEAD_COUNT: break
        st.toast(f"Scanning Page {page + 1}...", icon="🕵️")
        
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
                # --- DEDUPING ---
                pid = result.get("place_id", str(random.randint(10000,99999)))
                if pid in seen_place_ids: continue
                seen_place_ids.add(pid)

                # --- 1. SMART WEBSITE EXTRACTION (The Fix) ---
                # Check standard website
                website = result.get("website")
                if not website: website = result.get("links", {}).get("website")
                
                # Check for "Book Online" / Reservations (Common for Dentists/Doctors)
                if not website: website = result.get("reservations_link")
                if not website: website = result.get("booking_link")
                if not website: website = result.get("order_online_link")

                # --- 2. SMART PHOTO EXTRACTION ---
                photo_data = result.get("photos_link")
                photos_count = 0
                if isinstance(photo_data, dict):
                    photos_count = photo_data.get("count", 0)
                
                # Fallbacks
                if photos_count == 0 and result.get("thumbnail"): photos_count = 1
                if photos_count == 0 and result.get("images"): photos_count = len(result.get("images"))

                # --- 3. BASIC DATA ---
                try: rating = float(result.get("rating", 0))
                except: rating = 0.0
                reviews = int(result.get("reviews", 0))
                
                phone = result.get("phone")
                if not phone: phone = result.get("phone_number")
                if not phone: phone = "N/A"

                # --- 4. MAP LINK ---
                maps_url = result.get("gps_coordinates", {}).get("link")
                if not maps_url:
                    query = urllib.parse.quote(f"{result.get('title')} {result.get('address')}")
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"

                # --- 5. WEAKNESS SCORE ---
                weakness_score = 0
                if not website: weakness_score += 1000 
                if rating < 4.0: weakness_score += 500
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
                    "website": website, # Now includes Booking Links
                    "photos_count": photos_count,
                    "maps_url": maps_url,
                    "posts_active": False,
                    "owner_response_rate": 0.5,
                    "weakness_score": weakness_score
                })
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            break
            
        time.sleep(0.5)
    
    cleaned_leads.sort(key=lambda x: x['weakness_score'], reverse=True)
    return cleaned_leads

def _simulate_data(keyword, location):
    return [] # Removed for brevity
