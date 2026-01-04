# MODULE 3: RULES DEFINITION
# These are the specific logical triggers for leaks defined in your spec.

def check_trust_leak(reviews, rating):
    issues = []
    score = 0
    # Spec: "if reviews < 50: leak += 15"
    if reviews < 50:
        score += 15
        issues.append("Trust Gap: <50 Reviews (Customers don't trust you)")
    
    # Spec: "Rating < 4.3"
    if rating < 4.3:
        score += 15
        issues.append(f"Reputation Leak: Rating {rating} is below trust threshold (4.3)")
        
    return score, issues

def check_visual_leak(photos):
    issues = []
    score = 0
    # Spec: "if photos < 10: leak += 10"
    if photos < 10:
        score += 10
        issues.append("Visual Void: <10 Photos (Low Click-Through Rate)")
    return score, issues

def check_activity_leak(posts_active):
    issues = []
    score = 0
    # Spec: "if no_posts: leak += 10"
    if not posts_active:
        score += 10
        issues.append("Dead Listing: No recent Google Posts found")
    return score, issues

def check_conversion_leak(has_website):
    issues = []
    score = 0
    # Spec: "if missing_services (represented here by website): leak += 15"
    if not has_website:
        score += 15
        issues.append("Conversion Killer: No Website Linked")
    return score, issues
