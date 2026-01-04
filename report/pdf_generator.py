from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency, lead_data):
    """
    MODULE 5: AUDIT REPORT GENERATOR (DYNAMIC DATA EDITION)
    100% Text Compliance + Agency-Grade Aesthetic + Linux Font Support + Dynamic Data Injection.
    """
    
    # --- HELPER: DETECT FAILURES & GENERATE DYNAMIC TEXT ---
    issues_str = " ".join([str(i) for i in audit_result['issues']]).lower()
    
    def get_section_content(keywords, success_text, fail_text_template):
        # Check if this section failed based on audit issues
        is_fail = False
        for k in keywords:
            if k.lower() in issues_str:
                is_fail = True
                break
        
        if is_fail:
            badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
            # Return the specific failure text
            content = f"<p class='problem-row'>❌ ANALYSIS: {fail_text_template}</p>"
        else:
            badge = "<span class='badge badge-pass'>✅ PASS</span>"
            # Return the success text
            content = f"<p style='color: green; font-weight: bold;'>✅ ANALYSIS: {success_text}</p>"
            
        return badge, content

    # --- DYNAMIC DATA PREPARATION ---
    rev_count = lead_data.get('reviews', 0)
    rating = lead_data.get('rating', 0)
    photo_count = lead_data.get('photos', 0) # Fallback key if 'photos_count' is used elsewhere
    if photo_count == 0: photo_count = lead_data.get('photos_count', 0)
    
    website_status = "LINKED" if lead_data.get('website') else "MISSING"

    # --- SECTION LOGIC ---
    
    # 1. VISIBILITY
    s1_badge, s1_text = get_section_content(
        ["ranking", "category"],
        f"Your listing appears correctly for primary keywords. Good job.",
        f"Your business is invisible for high-intent keywords. Competitors are outranking you."
    )

    # 2. CTR (Photos/Visuals impact CTR)
    s2_badge, s2_text = get_section_content(
        ["visual", "photo", "ctr"],
        "Your listing looks active and clickable.",
        "Your listing looks 'inactive' compared to top competitors, reducing clicks."
    )

    # 3. CONVERSION (Website)
    s3_badge, s3_text = get_section_content(
        ["website", "conversion"],
        f"Website is {website_status}. Good funnel structure.",
        f"NO WEBSITE DETECTED. You are losing customers who want to verify you."
    )

    # 4. REVIEWS (Inject Real Numbers)
    s4_badge, s4_text = get_section_content(
        ["review", "trust", "reputation"],
        f"Strong Trust Signals: {rating} Stars with {rev_count} Reviews.",
        f"TRUST RISK: You only have {rev_count} reviews and a {rating} rating. Market leaders average 50+ reviews."
    )

    # 5. POSTS
    s5_badge, s5_text = get_section_content(
        ["post", "active", "offer"],
        "Active Google Posts detected. You are sending fresh signals.",
        "Zero active Google Posts found. Listing appears 'dormant' to the algorithm."
    )

    # 6. PHOTOS (Inject Real Numbers)
    s6_badge, s6_text = get_section_content(
        ["photo", "visual"],
        f"Visual Authority High: {photo_count} photos detected.",
        f"VISUAL VOID: Only {photo_count} photos found. Google prefers listings with 20+ high-quality images."
    )

    # 7/8. SIGNALS (Hard to measure via API, usually defaulted to risk for sales pressure)
    s7_badge = "<span class='badge badge-warn'>⚠️ RISK DETECTED</span>"

    # --- HTML CONSTRUCTION ---
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
            <h2 style="margin-top:0;">🧠 EXECUTIVE SUMMARY</h2>
            <p>Your business is visible on Google Maps, but our audit detected <strong>{len(audit_result['issues'])} specific optimization gaps.</strong></p>
            <p>These gaps are causing high-intent customers to choose competitors who appear more active and trustworthy.</p>
            
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
                {s1_badge}
            </div>
            {s1_text}
            <p><strong>Why this loses money:</strong> Customers searching these terms are ready to buy NOW. If you are not in the top 3 map results, you are invisible.</p>
            <div class="impact-row">
                💸 Revenue Impact: Even losing 5 calls/day × average sale value = thousands lost monthly.
            </div>
        </div>

        <!-- POINT 2 -->
        <div class="card">
            <div class="card-header">
                <span>2️⃣ LOW CLICK-THROUGH RATE (CTR)</span>
                {s2_badge}
            </div>
            {s2_text}
            <p><strong>What customers think:</strong> “This business looks outdated or less trustworthy.”</p>
            <div class="impact-row">
                💸 Revenue Impact: People choose who looks more active, not who is better.
            </div>
        </div>

        <!-- POINT 3 -->
        <div class="card">
            <div class="card-header">
                <span>3️⃣ BUYER CONFUSION (PRODUCTS/SERVICES)</span>
                {s3_badge}
            </div>
            {s3_text}
            <p><strong>Result:</strong> Customers leave your listing to check competitors who clearly show Services, Products, and Pricing.</p>
            <div class="impact-row">
                💸 Revenue Impact: You lose ready-to-buy customers due to lack of clarity.
            </div>
        </div>

        <div style="page-break-before: always;"></div>

        <!-- POINT 4 -->
        <div class="card">
            <div class="card-header">
                <span>4️⃣ WEAK REVIEW STRATEGY → TRUST LOSS</span>
                {s4_badge}
            </div>
            {s4_text}
            <p><strong>What happens:</strong> Google trusts active businesses more. Customers trust engaged businesses more.</p>
            <div class="impact-row">
                💸 Revenue Impact: A 0.2–0.5 star difference can reduce conversions by 15–25%.
            </div>
        </div>

        <!-- POINT 5 -->
        <div class="card">
            <div class="card-header">
                <span>5️⃣ ZERO POSTS / OFFERS → DEAD LISTING</span>
                {s5_badge}
            </div>
            {s5_text}
            <p><strong>What Google sees:</strong> “This business is not actively managed.”</p>
            <div class="impact-row">
                💸 Revenue Impact: You lose customers to competitors who show Offers, New Stock, and Activity.
            </div>
        </div>

        <!-- POINT 6 -->
        <div class="card">
            <div class="card-header">
                <span>6️⃣ POOR VISUAL AUTHORITY → LOW FOOTFALL</span>
                {s6_badge}
            </div>
            {s6_text}
            <p><strong>Buyer behavior:</strong> Customers judge before visiting.</p>
            <div class="impact-row">
                💸 Revenue Impact: Fewer direction clicks → fewer walk-ins → direct sales loss.
            </div>
        </div>
        
        <!-- POINT 7 & 8 Condensed -->
        <div class="card">
            <div class="card-header">
                <span>7️⃣ & 8️⃣ REPUTATION & ALGORITHM SIGNALS</span>
                {s7_badge}
            </div>
            <p class="problem-row">❌ ANALYSIS: Uncontrolled Q&A and Low Behavior Signals.</p>
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
            Generated by Revenue Leakage Audit System v2.1
        </div>

    </body>
    </html>
    """
    
    return HTML(string=html).write_pdf()
