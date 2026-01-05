def normalize_gbp_data(raw_lead):
    """
    MODULE 2: GBP DATA HARVESTER (FIXED)
    Ensures ALL required keys (website, posts, claimed) are present to prevent KeyErrors.
    """
    
    # 1. Clean Website Logic
    website_url = raw_lead.get("website")
    
    # 2. Clean Photo Logic
    photos = raw_lead.get("photos_count", 0)
    if photos == 0: photos = raw_lead.get("photos", 0)
    
    # 3. Clean Rating/Reviews
    try:
        rating = float(raw_lead.get("rating", 0))
    except:
        rating = 0.0
        
    try:
        reviews = int(raw_lead.get("reviews", 0))
    except:
        reviews = 0

    # 4. Construct Clean Object
    return {
        "name": raw_lead.get("business_name", "Unknown"),
        "address": raw_lead.get("address", ""),
        "phone": raw_lead.get("phone", ""),
        
        # Website Data
        "website": website_url,
        "has_website": bool(website_url),
        
        # Metrics
        "rating": rating,
        "reviews": reviews,
        "photos": photos,
        "photos_count": photos,
        
        # Engagement Signals (CRITICAL FIX: Added these back)
        "posts_active": raw_lead.get("posts_active", False),
        "claimed": raw_lead.get("claimed", True), # Assume true if missing to avoid false alarm
        
        "categories": raw_lead.get("categories", []),
        "place_id": raw_lead.get("place_id", "")
    }
