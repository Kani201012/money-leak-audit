def generate_cold_email(lead, template_type):
    """
    Generates a 4-Step High-Ticket Sales Sequence based on Audit Data.
    """
    
    # Extract Context
    business_name = lead.get('business_name', 'Business')
    rating = lead.get('rating', 0.0)
    reviews = lead.get('reviews', 0)
    website_status = "MISSING" if not lead.get('website') else "active"
    
    # Dynamic Pain Point
    pain_point = "low visibility"
    if not lead.get('website'): pain_point = "missing website link"
    elif rating < 4.0: pain_point = f"low rating ({rating} stars)"
    elif reviews < 10: pain_point = "low review count"

    # --- EMAIL 1: THE ANOMALY (DAY 0) ---
    if "Email 1" in template_type:
        subject = f"Question about {business_name}'s Google Map listing"
        body = f"""
Hi [Owner Name],

I'm writing to you directly because I found a critical anomaly in your Google Maps profile that is likely costing you customers.

While searching for '{lead.get('categories', ['Service'])[0]}' in your area, I noticed that while your competitors are showing up with optimized profiles, {business_name} is being penalized for **{pain_point}**.

I ran a quick 'Revenue Leakage Audit' on your profile to confirm this.

The data shows you are likely invisible to about 45% of high-intent mobile searchers right now.

I have the PDF report ready. Would you be opposed to me sending it over for you to review?

Best,

[Your Name]
"""

    # --- EMAIL 2: THE EVIDENCE (DAY 2) ---
    elif "Email 2" in template_type:
        subject = f"Comparison: {business_name} vs Market Leaders"
        body = f"""
Hi [Owner Name],

Following up on my previous note.

I wanted to share a specific data point from the audit I ran for {business_name}.

*   **Market Leader Avg Reviews:** 150+
*   **Your Current Reviews:** {reviews}

This 'Trust Gap' is the #1 reason customers click your competitor instead of you, even if your service is better.

I specialize in fixing this specific metric. We have a 90-Day protocol to close this gap.

Are you open to a 10-minute strategy call this Thursday to see how we do it?

Regards,

[Your Name]
"""

    # --- EMAIL 3: THE MATH (DAY 4) ---
    elif "Email 3" in template_type:
        subject = f"The cost of inaction (approx $5k/mo)"
        body = f"""
Hi [Owner Name],

I don't want to be a pest, but I hate seeing businesses leave money on the table.

Based on the average search volume in your area, a business with your current optimization score is likely missing **5-10 high-value calls per month**.

If your average customer value is $500+, that is a **$2,500 - $5,000 monthly revenue leak.**

Fixing your Google Business Profile is the highest ROI action you can take this week. It costs less than one lost customer.

Can we fix this?

[Your Name]
"""

    # --- EMAIL 4: THE BREAKUP (DAY 7) ---
    else:
        subject = f"Closing your audit file for {business_name}"
        body = f"""
Hi [Owner Name],

Since I haven't heard back, I assume fixing your Google Maps visibility isn't a priority right now.

I totally understand—running a business is busy work.

I am going to archive your audit report to clear my dashboard. If you decide later that you want to capture that lost traffic, feel free to reach out.

Best of luck with {business_name}.

[Your Name]
"""

    return subject.strip(), body.strip()
