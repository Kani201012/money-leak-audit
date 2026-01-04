def calculate_money_loss(rli_score, avg_sale, est_calls=50):
    """
    MODULE 4: SCORING & ROI CALCULATOR
    Spec: "Convert leaks into real money numbers."
    """
    # Logic: 
    # If RLI is 100 (Max), we assume 60% loss of potential business.
    # If RLI is 0 (Perfect), we assume 0% loss.
    
    loss_factor = (rli_score / 100) * 0.60
    
    missed_calls = int(est_calls * loss_factor)
    min_loss = missed_calls * avg_sale
    max_loss = min_loss * 1.5 # Range
    
    return {
        "estimated_calls_lost": missed_calls,
        "monthly_loss_min": min_loss,
        "monthly_loss_max": max_loss,
        "annual_loss": min_loss * 12
    }
