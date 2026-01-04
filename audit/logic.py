import random

def run_money_leak_audit(business_data):
    """
    MODULE 3: MONEY-LEAK AUDIT ENGINE (CORE IP)
    Calculates Revenue Leakage Index (RLI) based on specific rules.
    """
    leak_score = 0
    issues = []
    risk_summary = ""

    # --- RULE SET: TRUST & AUTHORITY ---
    # Spec: "if reviews < 50: leak += 15"
    if business_data['reviews'] < 50:
        leak_score += 15
        issues.append({
            "area": "Trust & Review Gaps",
            "impact": "High",
            "problem": f"Only {business_data['reviews']} reviews found (Threshold is 50).",
            "fix": "Launch automated review request campaign immediately."
        })
    elif business_data['rating'] < 4.3:
        # Spec: Rating < 4.3 is a filter/leak
        leak_score += 15
        issues.append({
            "area": "Trust & Review Gaps",
            "impact": "High",
            "problem": f"Rating is {business_data['rating']} (Target: 4.8+).",
            "fix": "Address negative feedback publicly and dilute with positive reviews."
        })

    # --- RULE SET: VISUALS & CTR ---
    # Spec: "if photos < 10: leak += 10"
    if business_data['photos_count'] < 10:
        leak_score += 10
        issues.append({
            "area": "Low Click-Through Rate (CTR)",
            "impact": "High",
            "problem": "Less than 10 photos. Listing looks 'dead'.",
            "fix": "Upload 10+ high-quality team/interior photos."
        })

    # --- RULE SET: ACTIVITY & ALGORITHM ---
    # Spec: "if no_posts: leak += 10"
    if not business_data.get('posts_active'):
        leak_score += 10
        issues.append({
            "area": "Inactive Engagement Signals",
            "impact": "Medium",
            "problem": "No active Google Posts detected.",
            "fix": "Post 1 offer weekly to trigger algorithm activity signals."
        })

    # --- RULE SET: CONVERSION ---
    # Spec: "if missing_services: leak += 15"
    if not business_data.get('has_website'):
        leak_score += 15
        issues.append({
            "area": "Missed Calls & Walk-ins",
            "impact": "Critical",
            "problem": "No Website linked.",
            "fix": "Link a landing page or website immediately."
        })

    if not business_data.get('claimed'):
        leak_score += 20
        issues.append({
            "area": "Ownership Risk",
            "impact": "Critical",
            "problem": "Business Profile is Unclaimed.",
            "fix": "Claim listing immediately to prevent competitor hijack."
        })

    # Cap score at 100
    leak_score = min(leak_score, 100)

    # Determine Risk Summary
    if leak_score > 60:
        risk_summary = "SEVERE REVENUE LEAKAGE (Immediate Action Required)"
    elif leak_score > 30:
        risk_summary = "MODERATE REVENUE LOSS"
    else:
        risk_summary = "LOW RISK (Optimization Opportunity)"

    return {
        "rli_score": leak_score,
        "leak_level": risk_summary,
        "issues": issues
    }

def calculate_roi_impact(leak_score, avg_sale_value, est_calls_monthly=50):
    """
    MODULE 4: SCORING & ROI CALCULATOR
    Converts leaks into real money numbers.
    """
    # Logic: Higher leak score = Higher % of lost calls
    # If score is 100, we assume 60% loss (based on your spec "30-60% loss")
    loss_percentage = (leak_score / 100) * 0.60
    
    calls_lost = int(est_calls_monthly * loss_percentage)
    monthly_loss_min = calls_lost * avg_sale_value
    monthly_loss_max = monthly_loss_min * 1.5 # Range
    
    return {
        "calls_lost": calls_lost,
        "monthly_loss_min": monthly_loss_min,
        "monthly_loss_max": monthly_loss_max,
        "annual_loss": monthly_loss_min * 12
    }
