def generate_cold_email(lead, template_type="Initial"):
    """
    Generates high-converting outreach based on specific gaps.
    """
    first_name = "Owner" # In a real scraper, we try to find names
    business_name = lead['business_name']
    gap_focus = "Google Maps Visibility"
    
    if lead['reviews'] < 20: gap_focus = "Trust & Reputation"
    if not lead['website']: gap_focus = "Digital Conversion"
    
    if template_type == "T1 (Initial)":
        subject = f"URGENT: Revenue leak identified at {business_name}"
        body = f"""
        Hi {first_name},
        
        I am writing to you directly because our recent benchmark analysis flagged a critical anomaly in your operations. 
        
        It appears {business_name} is currently losing traffic to competitors because of specific gaps in {gap_focus}.
        
        I have prepared a breakdown of where this leakage is occurring (approx value: $50k/year).
        
        Are you available for a brief 10-minute call tomorrow to review these findings?
        
        Best,
        [Your Name]
        """
        
    elif template_type == "T2 (Follow Up)":
        subject = f"Re: The cost of inaction for {business_name}"
        body = f"""
        Hi {first_name},
        
        Following up on my previous note. To put this in perspective, this operational gap in {gap_focus} is likely costing you high-intent customers daily.
        
        Competitors in your area have already closed these gaps. I do not want you to leave this money on the table.
        
        Can we schedule a quick review of the audit data this Thursday?
        
        Regards,
        [Your Name]
        """
        
    else: # Breakup
        subject = "Final Notice: Closing your audit file"
        body = f"""
        Hi {first_name},
        
        Since I have not heard back, I assume fixing this revenue leak is not a priority right now.
        
        I am closing your file today to prioritize other firms who are actively looking to optimize their revenue cycles.
        
        Best of luck,
        [Your Name]
        """
        
    return subject.strip(), body.strip()
