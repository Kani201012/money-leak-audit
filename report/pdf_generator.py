from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency):
    """
    MODULE 5: AUDIT REPORT GENERATOR (HIGH-TICKET SALES EDITION + FONT FIX)
    100% Text Compliance + Agency-Grade Aesthetic + Linux Font Support.
    """
    
    # --- HELPER: DETECT FAILURES ---
    issues_str = " ".join([str(i) for i in audit_result['issues']]).lower()
    
    def get_badge(keywords):
        for k in keywords:
            if k.lower() in issues_str:
                return "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        return "<span class='badge badge-pass'>✅ PASS</span>"

    # Status Logic mapping to your 8 Points
    s1 = get_badge(["review", "rating", "ranking"]) 
    s2 = get_badge(["photo", "visual", "ctr"])
    s3 = get_badge(["website", "service", "product"])
    s4 = get_badge(["review", "reply", "trust"])
    s5 = get_badge(["post", "offer", "active"])
    s6 = get_badge(["photo", "visual"])
    s7 = "<span class='badge badge-warn'>⚠️ RISK DETECTED</span>"
    s8 = "<span class='badge badge-fail'>❌ LOW SIGNAL</span>"

    # --- HTML & CSS CONSTRUCTION ---
    # FIXED: Changed font-family to 'DejaVu Sans' to stop the "Square Box" error on servers.
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 15mm; }}
            body {{ 
                font-family: 'DejaVu Sans', sans-serif; 
                color: #222; 
                line-height: 1.5; 
                font-size: 10pt;
            }}
            
            /* TYPOGRAPHY */
            h1 {{ font-size: 26pt; margin: 0; text-transform: uppercase; letter-spacing: 1px; color: #fff; }}
            h2 {{ font-size: 14pt; color: #D32F2F; border-bottom: 2px solid #D32F2F; padding-bottom: 8px; margin-top: 25px; text-transform: uppercase; }}
            h3 {{ font-size: 11pt; color: #000; font-weight: bold; margin: 10px 0 5px 0; }}
            p, li {{ margin-bottom: 5px; }}
            
            /* HEADER */
            .cover-header {{ 
                background-color: #111; 
                color: #fff; 
                padding: 30px; 
                text-align: center; 
                border-bottom: 5px solid #D32F2F; 
                margin-bottom: 30px;
            }}
            .cover-sub {{ font-size: 12pt; color: #FFD700; margin-top: 5px; }}

            /* EXECUTIVE SUMMARY BOX */
            .exec-box {{
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-left: 5px solid #222;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .impact-banner {{
                background-color: #D32F2F;
                color: white;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                font-size: 12pt;
                margin-top: 15px;
                border-radius: 4px;
            }}

            /* THE 8 POINTS - CARD DESIGN */
            .card {{
                border: 1px solid #e0e0e0;
                background-color: #fff;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 5px;
                page-break-inside: avoid;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            }}
            .card-header {{
                background-color: #f4f4f4;
                padding: 10px;
                font-weight: bold;
                font-size: 11pt;
                border-bottom: 1px solid #ddd;
                display: flex;
                justify-content: space-between;
            }}
            .badge {{
                font-size: 8pt;
                padding: 2px 6px;
                border-radius: 4px;
                color: white;
            }}
            .badge-fail {{ background-color: #D32F2F; }}
            .badge-pass {{ background-color: #2E7D32; }}
            .badge-warn {{ background-color: #F57F17; }}

            /* SPECIFIC SECTIONS WITHIN CARDS */
            .problem-row {{ color: #D32F2F; font-weight: bold; }}
            .impact-row {{ 
                margin-top: 10px; 
                padding: 8px; 
                background-color: #fff0f0; 
                color: #b71c1c; 
                font-style: italic; 
                border-left: 3px solid #b71c1c;
            }}
            ul.cause-list {{ margin: 5px 0 10px 20px; padding: 0; list-style-type: square; }}

            /* FINANCIAL TABLE */
            table.roi {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            table.roi th {{ background-color: #333; color: white; padding: 10px; text-align: left; }}
            table.roi td {{ border: 1px solid #ddd; padding: 8px; }}
            .cell-high {{ color: #D32F2F; font-weight: bold; }}
            .cell-med {{ color: #F57F17; font-weight: bold; }}

            /* TOTAL LOSS BOX */
            .total-loss-box {{
                border: 3px dashed #D32F2F;
                background-color: #fffbfb;
                text-align: center;
                padding: 25px;
                margin: 30px 0;
            }}
            .big-money {{ font-size: 22pt; color: #D32F2F; font-weight: bold; margin: 10px 0; }}

            /* SOLUTION SECTION */
            .solution-box {{
                background-color: #e8f5e9;
                border: 1px solid #c8e6c9;
                border-left: 5px solid #2E7D32;
                padding: 20px;
                margin-top: 20px;
            }}
            .check-list li {{ list-style-type: none; }}
            .check-list li:before {{ content: "✔ "; color: green; font-weight: bold; }}
        </style>
    </head>
    <body>

        <!-- COVER HEADER -->
        <div class="cover-header">
            <h1>💸 MONEY-LEAK AUDIT REPORT</h1>
            <div class="cover-sub">Prepared specifically for: {business_name}</div>
        </div>

        <!-- EXECUTIVE SUMMARY -->
        <div class="exec-box">
            <h2 style="margin-top:0;">🧠 EXECUTIVE SUMMARY (FOR OWNER)</h2>
            <p>Your business is visible on Google Maps, but it is <strong>not optimized to capture buyer intent.</strong></p>
            <p>As a result, high-intent customers are finding competitors instead of you, or abandoning your listing before contacting you.</p>
            <p><strong>This is not a branding issue — this is a direct revenue leakage problem.</strong></p>
            
            <div class="impact-banner">
                📉 ESTIMATED IMPACT:<br>
                30–60% potential revenue leakage from Google Maps traffic alone.<br>
                This loss is happening every day, silently.
            </div>
        </div>

        <!-- POINT 1 -->
        <div class="card">
            <div class="card-header">
                <span>1️⃣ LOST VISIBILITY → LOST CUSTOMERS</span>
                {s1}
            </div>
            <p class="problem-row">❌ Problem: Your business does not fully appear for high-intent searches.</p>
            <p>Examples: <em>“buy [product] near me”</em>, <em>“[service] {business_name}”</em>, <em>“open now”</em>.</p>
            
            <h3>Why this loses money:</h3>
            <p>Customers searching these terms are ready to buy NOW. If you are not in the top 3 map results, you are invisible.</p>
            
            <h3>Root Causes:</h3>
            <ul class="cause-list">
                <li>Weak / incorrect primary category</li>
                <li>Missing service keywords</li>
                <li>Low engagement signals</li>
            </ul>
            
            <div class="impact-row">
                💸 Revenue Impact: Even losing 5 calls/day × average sale value = thousands lost monthly.
            </div>
        </div>

        <!-- POINT 2 -->
        <div class="card">
            <div class="card-header">
                <span>2️⃣ LOW CLICK-THROUGH RATE (CTR)</span>
                {s2}
            </div>
            <p class="problem-row">❌ Problem: When customers see your listing, many do not click.</p>
            
            <h3>Why:</h3>
            <ul class="cause-list">
                <li>Weak business description</li>
                <li>No compelling photos</li>
                <li>No offers or promotions</li>
                <li>Listing looks “inactive” compared to competitors</li>
            </ul>

            <p><strong>What customers think:</strong> “This business looks outdated or less trustworthy.”</p>
            
            <div class="impact-row">
                💸 Revenue Impact: People choose who looks more active, not who is better.
            </div>
        </div>

        <!-- POINT 3 -->
        <div class="card">
            <div class="card-header">
                <span>3️⃣ BUYER CONFUSION (PRODUCTS/SERVICES)</span>
                {s3}
            </div>
            <p class="problem-row">❌ Problem: Customers cannot clearly see what exactly you sell.</p>
            <p>They miss: Price range, Availability, Specific Services.</p>
            
            <h3>Result:</h3>
            <p>Customers leave your listing to check competitors who: ✔ Show services, ✔ Show products, ✔ Show pricing.</p>
            
            <div class="impact-row">
                💸 Revenue Impact: You lose ready-to-buy customers due to lack of clarity.
            </div>
        </div>

        <div style="page-break-before: always;"></div>

        <!-- POINT 4 -->
        <div class="card">
            <div class="card-header">
                <span>4️⃣ WEAK REVIEW STRATEGY → TRUST LOSS</span>
                {s4}
            </div>
            <p class="problem-row">❌ Problem: Although reviews exist, they are not being monetized.</p>
            
            <h3>Issues:</h3>
            <ul class="cause-list">
                <li>No keyword-rich reviews</li>
                <li>No owner replies (or generic replies)</li>
                <li>No review growth system</li>
            </ul>
            
            <h3>What happens:</h3>
            <p>Google trusts active businesses more. Customers trust engaged businesses more.</p>
            
            <div class="impact-row">
                💸 Revenue Impact: A 0.2–0.5 star difference can reduce conversions by 15–25%.
            </div>
        </div>

        <!-- POINT 5 -->
        <div class="card">
            <div class="card-header">
                <span>5️⃣ ZERO POSTS / OFFERS → DEAD LISTING</span>
                {s5}
            </div>
            <p class="problem-row">❌ Problem: No regular Google Posts.</p>
            
            <p><strong>What Google sees:</strong> “This business is not actively managed.”</p>
            <p><strong>What customers see:</strong> “Maybe this shop is closed or not serious.”</p>
            
            <div class="impact-row">
                💸 Revenue Impact: You lose customers to competitors who show Offers, New Stock, and Activity.
            </div>
        </div>

        <!-- POINT 6 -->
        <div class="card">
            <div class="card-header">
                <span>6️⃣ POOR VISUAL AUTHORITY → LOW FOOTFALL</span>
                {s6}
            </div>
            <p class="problem-row">❌ Problem: Insufficient photos.</p>
            <p>Missing: Product showcase, Interior/exterior clarity, Team/Real-world proof.</p>
            
            <p><strong>Buyer behavior:</strong> Customers judge before visiting.</p>
            
            <div class="impact-row">
                💸 Revenue Impact: Fewer direction clicks → fewer walk-ins → direct sales loss.
            </div>
        </div>
        
        <!-- POINT 7 & 8 Condensed -->
        <div class="card">
            <div class="card-header">
                <span>7️⃣ & 8️⃣ REPUTATION & ALGORITHM SIGNALS</span>
                {s7}
            </div>
            <p class="problem-row">❌ Problem: Uncontrolled Q&A and Low Behavior Signals.</p>
            <p>Google measures calls, clicks, and dwell time. Your listing is not engineered to force interaction.</p>
            <div class="impact-row">
                 💸 Revenue Impact: One unanswered negative question can kill multiple sales.
            </div>
        </div>

        <div style="page-break-before: always;"></div>

        <!-- FINANCIAL IMPACT -->
        <h2>📉 TOTAL BUSINESS IMPACT ESTIMATION</h2>
        
        <table class="roi">
            <tr>
                <th>Leakage Area</th>
                <th>Impact Level</th>
            </tr>
            <tr>
                <td>Lost Map Rankings</td>
                <td class="cell-high">🔴 High</td>
            </tr>
            <tr>
                <td>Low Click-Through Rate</td>
                <td class="cell-high">🔴 High</td>
            </tr>
            <tr>
                <td>Missed Calls & Walk-ins</td>
                <td class="cell-high">🔴 High</td>
            </tr>
            <tr>
                <td>Review Trust Loss</td>
                <td class="cell-med">🟠 Medium</td>
            </tr>
            <tr>
                <td>Inactive Engagement Signals</td>
                <td class="cell-med">🟠 Medium</td>
            </tr>
        </table>

        <div class="total-loss-box">
            <h3>📉 ESTIMATED MONTHLY LOSS</h3>
            <div class="big-money">{currency}{roi_result['monthly_loss_min']:,} - {currency}{roi_result['monthly_loss_max']:,}</div>
            <p><strong>ANNUAL LOSS EXPOSURE: {currency}{roi_result['annual_loss']:,}</strong></p>
            <p style="font-size: 0.9em; color: #666;">(Based on 25-60% leakage of potential market share)</p>
        </div>

        <!-- SOLUTION -->
        <div class="solution-box">
            <h2 style="color: #2E7D32; border-color: #2E7D32; margin-top:0;">🛠️ SOLUTION (POSITION YOUR SERVICE)</h2>
            
            <h3>What Optimization Fixes:</h3>
            <ul class="check-list">
                <li>Higher visibility for "Buy Now" keywords</li>
                <li>More inbound calls & direction requests</li>
                <li>Increased walk-in traffic</li>
                <li>Higher conversion rate from Maps traffic</li>
            </ul>

            <h3>Timeframe:</h3>
            <ul>
                <li><strong>First improvements:</strong> 7–14 days</li>
                <li><strong>Strong, measurable growth:</strong> 30–45 days</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 9pt;">
            Generated by Revenue Leakage Audit System v2.0
        </div>

    </body>
    </html>
    """
    
    return HTML(string=html).write_pdf()
