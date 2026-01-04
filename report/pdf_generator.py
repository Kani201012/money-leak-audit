from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency):
    """
    MODULE 5: AUDIT REPORT GENERATOR (SALES COPY EDITION)
    Generates a report using the exact "Money-Leak" narrative provided.
    """
    
    # 1. Determine Pass/Fail Status for the 8 Points based on Audit Data
    # We look at the 'issues' list to see if a specific problem was flagged.
    
    issues_text = " ".join([i for i in audit_result['issues']])
    
    def get_status(trigger_words):
        # If the issue text contains relevant keywords, they FAILED this section.
        for word in trigger_words:
            if word in issues_text:
                return "<span style='color: #D32F2F;'>❌ CRITICAL FAIL</span>"
        return "<span style='color: green;'>✅ PASS</span>"

    # Map the 8 sections to logic triggers
    s1_status = get_status(["Trust", "Rating", "Review"]) # Visibility/Ranking often tied to trust
    s2_status = get_status(["Photos", "Visual"]) # CTR tied to photos
    s3_status = get_status(["Website", "Conversion"]) # Product/Service confusion
    s4_status = get_status(["Trust", "Review"]) # Reviews
    s5_status = get_status(["Posts", "Active"]) # Posts
    s6_status = get_status(["Photos", "Visual"]) # Visual Authority
    s7_status = "<span style='color: orange;'>⚠️ RISK (Unmonitored)</span>" # Q&A is hard to scrape, assume risk
    s8_status = "<span style='color: #D32F2F;'>❌ LOW SIGNAL</span>" # Behavior signals are usually low for unoptimized profiles

    # 2. Build the HTML using YOUR EXACT TEXT
    html_content = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 1.5cm; }}
            body {{ font-family: 'Helvetica', 'Arial', sans-serif; color: #333; line-height: 1.4; font-size: 11pt; }}
            .header {{ background-color: #000; color: #fff; padding: 20px; text-align: center; margin-bottom: 30px; }}
            .header h1 {{ margin: 0; font-size: 24pt; text-transform: uppercase; }}
            .header h3 {{ margin: 5px 0 0 0; font-weight: normal; color: #FFD700; }}
            
            .section-title {{ background-color: #eee; padding: 10px; border-left: 5px solid #D32F2F; margin-top: 25px; font-weight: bold; font-size: 12pt; }}
            .status-badge {{ float: right; font-weight: bold; }}
            
            .problem-box {{ border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: #fafafa; }}
            .money-impact {{ color: #D32F2F; font-weight: bold; font-style: italic; margin-top: 5px; }}
            
            .exec-summary {{ border: 2px solid #000; padding: 20px; margin-bottom: 20px; }}
            .highlight {{ background-color: #ffffcc; }}
            
            .roi-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            .roi-table td {{ padding: 10px; border: 1px solid #ccc; }}
            .roi-table th {{ background: #D32F2F; color: white; padding: 10px; }}
            
            .big-loss {{ font-size: 18pt; color: #D32F2F; font-weight: bold; text-align: center; }}
        </style>
    </head>
    <body>
        
        <!-- HEADER -->
        <div class="header">
            <h1>💸 MONEY-LEAK AUDIT REPORT</h1>
            <h3>Prepared for: {business_name}</h3>
        </div>

        <!-- EXECUTIVE SUMMARY -->
        <div class="exec-summary">
            <h2 style="margin-top: 0; color: #D32F2F;">🧠 EXECUTIVE SUMMARY</h2>
            <p>Your business is visible on Google Maps, but it is <strong>not optimized to capture buyer intent.</strong></p>
            <p>As a result, high-intent customers are finding competitors instead of you, or abandoning your listing before contacting you.</p>
            
            <div style="background: #D32F2F; color: white; padding: 15px; text-align: center; margin-top: 15px;">
                <strong>📉 ESTIMATED IMPACT:</strong><br>
                30–60% potential revenue leakage from Google Maps traffic alone.<br>
                This loss is happening every day, silently.
            </div>
        </div>

        <!-- SECTION 1 -->
        <div class="section-title">
            1️⃣ LOST VISIBILITY → LOST CUSTOMERS
            <span class="status-badge">{s1_status}</span>
        </div>
        <div class="problem-box">
            <strong>❌ Problem:</strong> Your business does not fully appear for high-intent searches such as "buy [product] near me" or "best [service] nearby".<br><br>
            <strong>Why this loses money:</strong> Customers searching these terms are ready to buy NOW. If you are not in the top 3 map results, you are effectively invisible.<br><br>
            <div class="money-impact">💸 Revenue Impact: Even losing 5 calls/day × average sale value = thousands lost monthly.</div>
        </div>

        <!-- SECTION 2 -->
        <div class="section-title">
            2️⃣ LOW CLICK-THROUGH RATE (CTR)
            <span class="status-badge">{s2_status}</span>
        </div>
        <div class="problem-box">
            <strong>❌ Problem:</strong> When customers see your listing, many do not click due to weak descriptions, no compelling photos, or lack of offers.<br><br>
            <strong>What customers think:</strong> "This business looks outdated or less trustworthy."<br><br>
            <div class="money-impact">💸 Revenue Impact: People choose who looks more active, not who is better.</div>
        </div>

        <!-- SECTION 3 -->
        <div class="section-title">
            3️⃣ BUYER CONFUSION (PRODUCTS/SERVICES)
            <span class="status-badge">{s3_status}</span>
        </div>
        <div class="problem-box">
            <strong>❌ Problem:</strong> Customers cannot clearly see what exactly you sell, your price range, or availability.<br><br>
            <strong>Result:</strong> Customers leave your listing to check competitors who clearly show Services, Products, and Pricing.<br><br>
            <div class="money-impact">💸 Revenue Impact: You lose ready-to-buy customers due to lack of clarity.</div>
        </div>

        <!-- SECTION 4 -->
        <div class="section-title">
            4️⃣ WEAK REVIEW STRATEGY → TRUST LOSS
            <span class="status-badge">{s4_status}</span>
        </div>
        <div class="problem-box">
            <strong>❌ Problem:</strong> Although reviews exist, they are not being monetized. (No keyword-rich reviews, no owner replies, no growth system).<br><br>
            <strong>What happens:</strong> Google trusts active businesses more. Customers trust engaged businesses more.<br><br>
            <div class="money-impact">💸 Revenue Impact: A 0.2–0.5 star difference can reduce conversions by 15–25%.</div>
        </div>

        <!-- SECTION 5 -->
        <div class="section-title">
            5️⃣ ZERO POSTS / OFFERS → DEAD LISTING
            <span class="status-badge">{s5_status}</span>
        </div>
        <div class="problem-box">
            <strong>❌ Problem:</strong> No regular Google Posts found.<br><br>
            <strong>What Google sees:</strong> "This business is not actively managed."<br>
            <strong>What customers see:</strong> "Maybe this shop is closed or not serious."<br><br>
            <div class="money-impact">💸 Revenue Impact: You lose customers to competitors who show Offers, New Stock, and Activity.</div>
        </div>

        <!-- SECTION 6 -->
        <div class="section-title">
            6️⃣ POOR VISUAL AUTHORITY → LOW FOOTFALL
            <span class="status-badge">{s6_status}</span>
        </div>
        <div class="problem-box">
            <strong>❌ Problem:</strong> Insufficient photos (No product showcase, no interior/exterior clarity).<br><br>
            <strong>Buyer behavior:</strong> Customers judge before visiting.<br><br>
            <div class="money-impact">💸 Revenue Impact: Fewer direction clicks → fewer walk-ins → direct sales loss.</div>
        </div>

        <!-- PAGE BREAK FOR FINANCIALS -->
        <div style="page-break-before: always;"></div>

        <!-- SECTION 7 & 8 SUMMARY -->
        <div class="section-title">7️⃣ & 8️⃣ REPUTATION & SIGNAL RISK</div>
        <p>Uncontrolled Q&A and low behavioral signals (calls/clicks) create a downward visibility loop.</p>

        <!-- FINANCIAL IMPACT -->
        <h2 style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px;">📉 TOTAL BUSINESS IMPACT ESTIMATION</h2>
        
        <table class="roi-table">
            <tr>
                <th>Leakage Area</th>
                <th>Impact Level</th>
            </tr>
            <tr>
                <td>Lost Map Rankings</td>
                <td style="color: red; font-weight: bold;">🔴 High</td>
            </tr>
            <tr>
                <td>Low Click-Through Rate</td>
                <td style="color: red; font-weight: bold;">🔴 High</td>
            </tr>
             <tr>
                <td>Missed Calls & Walk-ins</td>
                <td style="color: red; font-weight: bold;">🔴 High</td>
            </tr>
             <tr>
                <td>Review Trust Loss</td>
                <td style="color: orange; font-weight: bold;">🟠 Medium</td>
            </tr>
        </table>

        <br>
        <div style="border: 2px dashed #D32F2F; padding: 20px; text-align: center; background-color: #fff0f0;">
            <h3>⚠️ ESTIMATED MONTHLY LOSS</h3>
            <p class="big-loss">{currency}{roi_result['monthly_loss_min']:,} - {currency}{roi_result['monthly_loss_max']:,}</p>
            <p><strong>ANNUAL LOSS EXPOSURE: {currency}{roi_result['annual_loss']:,}</strong></p>
        </div>

        <!-- SOLUTION -->
        <div style="margin-top: 30px;">
            <h2 style="color: green;">🛠️ SOLUTION (THE FIX)</h2>
            <p><strong>What Optimization Fixes:</strong></p>
            <ul>
                <li>✔ Higher visibility for "Buy Now" keywords</li>
                <li>✔ More inbound calls & direction requests</li>
                <li>✔ Increased walk-in traffic</li>
                <li>✔ Higher conversion rate from Maps traffic</li>
            </ul>
            
            <p><strong>Timeframe:</strong></p>
            <ul>
                <li>First improvements: <strong>7–14 days</strong></li>
                <li>Strong, measurable growth: <strong>30–45 days</strong></li>
            </ul>
        </div>

        <br><br>
        <div style="text-align: center; font-size: 10pt; color: #777;">
            Generated by Revenue Leakage Audit System v1.0
        </div>

    </body>
    </html>
    """
    
    return HTML(string=html_content).write_pdf()
