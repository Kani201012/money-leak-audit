from weasyprint import HTML

def generate_consulting_pdf(business, audit_data, roi_data, currency):
    """
    MODULE 5: AUDIT REPORT GENERATOR
    Creates the fear-driven, action-oriented PDF.
    """
    
    # Generate Rows for the Issues Table
    issues_html = ""
    for issue in audit_data['issues']:
        color = "red" if issue['impact'] == "Critical" or issue['impact'] == "High" else "orange"
        issues_html += f"""
        <tr style="border-bottom: 1px solid #ddd;">
            <td style="padding: 10px; color: {color}; font-weight: bold;">{issue['impact']}</td>
            <td style="padding: 10px;">{issue['area']}</td>
            <td style="padding: 10px;">{issue['problem']}</td>
            <td style="padding: 10px; background-color: #f9f9f9;">{issue['fix']}</td>
        </tr>
        """

    html_string = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, sans-serif; color: #333; }}
            .header {{ background: #000; color: #fff; padding: 30px; text-align: center; }}
            .score-box {{ background: #ffeded; border: 2px solid #d32f2f; padding: 20px; text-align: center; margin: 20px 0; }}
            .money-loss {{ font-size: 24px; color: #d32f2f; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #333; color: #fff; padding: 10px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>GOOGLE MAPS MONEY-LEAK AUDIT</h1>
            <h3>Prepared for: {business['business_name']}</h3>
        </div>

        <div style="padding: 20px;">
            <h2>🚨 EXECUTIVE SUMMARY</h2>
            <p>Your business appears on Google Maps, but it is not optimized to capture buyer intent. 
            High-intent customers are finding competitors instead of you. 
            <strong>This is not a branding issue — this is a direct revenue leakage problem.</strong></p>

            <div class="score-box">
                <h2>REVENUE LEAKAGE INDEX (RLI™)</h2>
                <h1 style="font-size: 50px; margin: 0; color: #d32f2f;">{audit_data['rli_score']}/100</h1>
                <h3>{audit_data['leak_level']}</h3>
            </div>

            <h2>📉 ESTIMATED FINANCIAL IMPACT</h2>
            <p>Based on your visibility gaps, we estimate you are losing:</p>
            <ul>
                <li><strong>Missed Calls/Month:</strong> {roi_data['calls_lost']}</li>
                <li class="money-loss">Monthly Loss: {currency}{roi_data['monthly_loss_min']:,} - {currency}{roi_data['monthly_loss_max']:,}</li>
                <li><strong>Annual Projected Loss: {currency}{roi_data['annual_loss']:,}</strong></li>
            </ul>

            <h2>🔍 IDENTIFIED LEAKS & FIX PLAN</h2>
            <table>
                <thead>
                    <tr>
                        <th>Impact</th>
                        <th>Leak Area</th>
                        <th>Problem</th>
                        <th>30-Day Fix Plan</th>
                    </tr>
                </thead>
                <tbody>
                    {issues_html}
                </tbody>
            </table>

            <br><br>
            <div style="background: #eee; padding: 20px; text-align: center;">
                <h3>🚀 STOP THE LEAK</h3>
                <p>We can fix these issues in 30 days. Contact us to reclaim this revenue.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTML(string=html_string).write_pdf()
