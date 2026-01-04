def normalize_gbp_data(raw_lead):
    """
    MODULE 2: GBP DATA HARVESTER
    Cleans and prepares data for the Audit Engine.
    Ensures all fields exist to prevent errors in logic.
    """
    return {
        "name": raw_lead.get("business_name"),
        "rating": float(raw_lead.get("rating", 0)),
        "reviews": int(raw_lead.get("reviews", 0)),
        "photos": int(raw_lead.get("photos_count", 0)),
        "has_website": bool(raw_lead.get("website")),
        "posts_active": bool(raw_lead.get("posts_active")),
        "owner_responsive": raw_lead.get("owner_response_rate", 0) > 0.5,
        "phone": raw_lead.get("phone", "N/A"),
        "address": raw_lead.get("address", "Unknown")
    }
