from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency):
    """
    MODULE 5: AUDIT REPORT GENERATOR
    Uses Jinja2-style string formatting to create the PDF.
    """
    
    # Dynamic Issue List
    issues_html = ""
    for issue in audit_result['issues']:
        issues_html += f"<li style='color: #D32F2F; margin-bottom: 8px;'><strong>❌ {issue}</strong></li>"

    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; color: #333; }}
            .header {{ background-color: #222; color: #fff; padding: 40px; text-align: center; }}
            .alert-box {{ border: 2px solid #D32F2F; background-color: #fff5f5; padding: 20px; margin: 20px 0; border-radius: 8px; }}
            .score {{ font-size: 4em; font-weight: bold; color: #D32F2F; margin: 0; }}
            .money {{ font-size: 1.5em; font-weight: bold; color: #000; }}
            h2 {{ border-bottom: 2px solid #ccc; padding-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>MONEY-LEAK AUDIT REPORT</h1>
            <h3>Prepared for: {business_name}</h3>
        </div>

        <div style="padding: 40px;">
            <h2>🧠 EXECUTIVE SUMMARY</h2>
            <p>Your business appears on Google Maps, but it is not optimized. 
            <strong>This is not a branding issue — this is a direct revenue leakage problem.</strong></p>

            <div class="alert-box" style="text-align: center;">
                <h3>REVENUE LEAKAGE INDEX (RLI™)</h3>
                <p class="score">{audit_result['rli_score']}/100</p>
                <p><strong>Status: {audit_result['leak_level']}</strong></p>
            </div>

            <h2>📉 FINANCIAL IMPACT ESTIMATION</h2>
            <p>Based on your visibility gaps, you are losing approximately:</p>
            <ul>
                <li><strong>Missed Calls/Month:</strong> {roi_result['estimated_calls_lost']}</li>
                <li><strong>Monthly Revenue Lost:</strong> {currency}{roi_result['monthly_loss_min']:,} - {currency}{roi_result['monthly_loss_max']:,}</li>
                <li style="font-size: 1.2em;"><strong>ANNUAL LOSS: {currency}{roi_result['annual_loss']:,}</strong></li>
            </ul>

            <h2>🔍 IDENTIFIED LEAKS</h2>
            <ul>
                {issues_html}
            </ul>

            <br><br>
            <div style="background-color: #eee; padding: 20px; text-align: center;">
                <h3>🚀 30-DAY FIX PLAN</h3>
                <p>We can fix these issues and reclaim this revenue. Contact us immediately.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTML(string=html_content).write_pdf()
