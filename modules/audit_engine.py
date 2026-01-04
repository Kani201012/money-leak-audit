def calculate_leakage(business_data):
    score = 0
    issues = []
    
    # Check Rating
    if business_data['rating'] < 4.0:
        score += 25
        issues.append("Rating is below 4.0 (Trust Issue)")
    
    # Check Reviews
    if business_data['reviews'] < 20:
        score += 20
        issues.append("Low review count (Low Authority)")
        
    # Check Website
    if not business_data['website']:
        score += 20
        issues.append("No Website listed (Conversion Killer)")
        
    # Check Photos
    if business_data['photos_count'] < 10:
        score += 15
        issues.append("Very few photos (Low Engagement)")
        
    return {
        "score": min(score, 100),
        "severity": "High" if score > 50 else "Medium" if score > 20 else "Low",
        "issues": issues
    }

def calculate_roi_loss(leak_score, avg_sale):
    # Math: Higher score = more lost customers
    lost_customers = int((leak_score / 100) * 20) # Assume 20 leads lost if score is 100
    money_lost = lost_customers * avg_sale
    return {
        "min_revenue_loss": money_lost,
        "annual_loss": money_lost * 12
    }
