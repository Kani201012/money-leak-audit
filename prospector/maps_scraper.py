import time
import random

def find_leads(keyword, location):
    """
    MODULE 1: PROSPECTOR (LEAD FINDER)
    Simulates finding businesses based on specific "Weakness Filters".
    In production, this connects to SerpAPI/Outscraper.
    """
    time.sleep(1) # Network simulation
    
    # We generate a mix of "High Leak" and "Low Leak" businesses to test the system
    leads = [
        {
            "business_name": f"{keyword} Pro Services",
            "place_id": "PID_001",
            "rating": 4.9,
            "reviews": 150,
            "categories": [keyword],
            "phone": "+1 555-0101",
            "address": f"100 Main St, {location}",
            "website": "https://example.com",
            "photos_count": 45,
            "posts_active": True,
            "owner_response_rate": 0.9
        },
        {
            "business_name": f"{location} {keyword} Depot",
            "place_id": "PID_002",
            "rating": 3.6, # LEAK: Low Rating
            "reviews": 14, # LEAK: Low Trust
            "categories": [keyword],
            "phone": "+1 555-0202",
            "address": f"200 Side St, {location}",
            "website": None, # LEAK: No Website
            "photos_count": 3, # LEAK: Visual Void
            "posts_active": False, # LEAK: Dead Listing
            "owner_response_rate": 0.0
        },
        {
            "business_name": f"Bob's {keyword}",
            "place_id": "PID_003",
            "rating": 4.1,
            "reviews": 35, # LEAK: Low Trust
            "categories": [keyword],
            "phone": "+1 555-0303",
            "address": f"300 Broad Ave, {location}",
            "website": "https://bobs-site.com",
            "photos_count": 8, # LEAK: Low Photos
            "posts_active": False, # LEAK: No Posts
            "owner_response_rate": 0.2
        }
    ]
    return leads
