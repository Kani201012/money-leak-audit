import time

# This simulates finding businesses so you don't need a paid API key yet
def get_prospects(keyword, location, api_key=None):
    time.sleep(1) # Fake loading time
    
    # We return 3 fake businesses for the demo
    return [
        {
            "business_name": f"{keyword} Kings of {location}",
            "rating": 4.9,
            "reviews": 150,
            "address": f"101 Main St, {location}",
            "phone": "+1 555-0101",
            "website": "https://example.com",
            "photos_count": 50,
            "posts_active": True
        },
        {
            "business_name": f"{location} {keyword} Center",
            "rating": 3.8,
            "reviews": 12,
            "address": f"204 Side St, {location}",
            "phone": "+1 555-0202",
            "website": None, # This is a leak!
            "photos_count": 4, # This is a leak!
            "posts_active": False
        },
        {
            "business_name": f"Budget {keyword}",
            "rating": 4.2,
            "reviews": 30,
            "address": f"88 Broad Ave, {location}",
            "phone": "+1 555-0303",
            "website": "https://example.com",
            "photos_count": 12,
            "posts_active": False # This is a leak!
        }
    ]
