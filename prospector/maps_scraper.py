import time
import random

def search_google_maps(keyword, location, api_key=None):
    """
    MODULE 1: PROSPECTOR
    Finds businesses and extracts data structure defined in spec.
    """
    # NOTE: To make this work instantly without you buying an API key yet,
    # we simulate the "Outscraper" / "SerpAPI" response here.
    
    time.sleep(1.5) # Simulate network request
    
    # We generate semi-random data to simulate finding "Bad" and "Good" businesses
    results = []
    
    names = [f"{keyword} Pro", f"{location} {keyword}", f"Best {keyword} Services", f"{keyword} Express"]
    
    for name in names:
        # Randomize attributes to test the Audit Engine logic
        rating = random.choice([3.5, 3.9, 4.5, 4.9])
        reviews = random.choice([5, 15, 45, 120])
        photos = random.choice([3, 8, 20, 50])
        has_site = random.choice([True, False])
        posts_active = random.choice([True, False])
        
        results.append({
            "business_name": name,
            "address": f"{random.randint(1,999)} Main St, {location}",
            "rating": rating,
            "reviews": reviews,
            "photos_count": photos,
            "has_website": has_site,
            "posts_active": posts_active,
            "claimed": True, # Assume claimed for now
            "phone": "+1 555-0000"
        })
        
    return results
