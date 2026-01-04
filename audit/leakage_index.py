from audit.rules import check_trust_leak, check_visual_leak, check_activity_leak, check_conversion_leak

def calculate_rli_score(data):
    """
    MODULE 3: MONEY-LEAK AUDIT ENGINE
    Aggregates all rules into a final Revenue Leakage Index (RLI) Score.
    """
    total_leak_score = 0
    all_issues = []

    # 1. Trust Analysis
    s1, i1 = check_trust_leak(data['reviews'], data['rating'])
    total_leak_score += s1
    all_issues.extend(i1)

    # 2. Visual Analysis
    s2, i2 = check_visual_leak(data['photos'])
    total_leak_score += s2
    all_issues.extend(i2)

    # 3. Activity Analysis
    s3, i3 = check_activity_leak(data['posts_active'])
    total_leak_score += s3
    all_issues.extend(i3)

    # 4. Conversion Analysis
    s4, i4 = check_conversion_leak(data['has_website'])
    total_leak_score += s4
    all_issues.extend(i4)

    # Cap score at 100
    final_score = min(total_leak_score, 100)

    # Determine Leak Level Risk Summary
    risk_summary = "Low"
    if final_score > 30: risk_summary = "Medium Revenue Leakage"
    if final_score > 60: risk_summary = "CRITICAL REVENUE HEMORRHAGE"

    return {
        "rli_score": final_score,
        "leak_level": risk_summary,
        "issues": all_issues
    }
