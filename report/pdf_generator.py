from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency, lead_data):
    """
    MODULE 5: AUDIT REPORT GENERATOR (V4.0 - CONVERSION PSYCHOLOGY EDITION)
    Features: High-Converting Copy, 3D Buttons, "The Hook", and Outcome-Based Roadmap.
    """
    
    # --- 1. DATA PREPARATION ---
    issues_str = " ".join([str(i) for i in audit_result['issues']]).lower()
    
    rev_count = lead_data.get('reviews', 0)
    rating = lead_data.get('rating', 0.0)
    photo_count = lead_data.get('photos', 0)
    if photo_count == 0: photo_count = lead_data.get('photos_count', 0)
    has_website = lead_data.get('website') or lead_data.get('has_website')
    
    competitor_avg_reviews = 150
    competitor_avg_photos = 45

    def get_status(is_fail, success_text, fail_text):
        if is_fail:
            return "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>", f"<p class='problem-row'>❌ ANALYSIS: {fail_text}</p>"
        else:
            return "<span class='badge badge-pass'>✅ PASS</span>", f"<p class='success-row'>✅ ANALYSIS: {success_text}</p>"

    # --- 2. LOGIC ---
    
    # VISIBILITY
    s1_fail = any(x in issues_str for x in ["ranking", "category"])
    s1_badge, s1_text = get_status(s1_fail, "Your listing appears for primary keywords.", "Your business is invisible for high-intent 'Near Me' keywords.")

    # CTR
    if rating < 4.0:
        s2_badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        s2_text = f"<p class='problem-row'>❌ ANALYSIS: Your <strong>{rating} Star Rating</strong> is killing your Click-Through-Rate. Customers filter for 4.0+.</p>"
    else:
        s2_badge = "<span class='badge badge-pass'>✅ PASS</span>"
        s2_text = "<p class='success-row'>✅ ANALYSIS: Listing looks clickable and trustworthy.</p>"

    # WEBSITE
    if not has_website:
        s3_badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        s3_text = "<p class='problem-row'>❌ ANALYSIS: <strong>WEBSITE/BOOKING LINK MISSING.</strong> This is the #1 reason customers abandon a listing.</p>"
    else:
        s3_badge = "<span class='badge badge-pass'>✅ PASS</span>"
        s3_text = f"<p class='success-row'>✅ ANALYSIS: Website/Booking link active.</p>"

    # REVIEWS
    if rev_count > 50 and rating < 4.0:
        s4_badge = "<span class='badge badge-warn'>⚠️ REPUTATION RISK</span>"
        s4_text = f"<p class='problem-row'>⚠️ ANALYSIS: Volume is high ({rev_count}) but Sentiment is Low ({rating}).</p>"
    elif rev_count < 50:
        s4_badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        s4_text = f"<p class='problem-row'>❌ ANALYSIS: Trust Gap. You have {rev_count} reviews. Market Leaders have {competitor_avg_reviews}+.</p>"
    else:
        s4_badge = "<span class='badge badge-pass'>✅ PASS</span>"
        s4_text = f"<p class='success-row'>✅ ANALYSIS: Strong Trust Signals ({rev_count} Reviews).</p>"

    # POSTS
    s5_fail = any(x in issues_str for x in ["post", "active"])
    s5_badge, s5_text = get_status(s5_fail, "Active Google Posts detected.", "Zero active Posts. Google prefers 'Alive' businesses.")

    # PHOTOS
    if photo_count <= 1:
        s6_badge = "<span class='badge badge-warn'>⚠️ VERIFY</span>"
        s6_text = "<p class='problem-row'>⚠️ ANALYSIS: <strong>Limited Visual Data Detected.</strong> Google is not displaying your portfolio correctly.</p>"
    elif photo_count < 20:
        s6_badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        s6_text = f"<p class='problem-row'>❌ ANALYSIS: Only {photo_count} photos found. Competitors showcase {competitor_avg_photos}+.</p>"
    else:
        s6_badge = "<span class='badge badge-pass'>✅ PASS</span>"
        s6_text = f"<p class='success-row'>✅ ANALYSIS: Good Visual Authority ({photo_count} photos).</p>"

    # 7 & 8
    s7_badge = "<span class='badge badge-warn'>⚠️ RISK DETECTED</span>"
    s8_badge = "<span class='badge badge-warn'>⚠️ LOW SIGNAL</span>"

    # --- HTML ---
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 10mm; }}
            body {{ font-family: 'DejaVu Sans', sans-serif; color: #222; line-height: 1.4; font-size: 10pt; }}
            
            /* HEADERS & HOOK */
            .cover-header {{ 
                background: #111; 
                color: #fff; 
                padding: 35px 20px; 
                text-align: center; 
                border-bottom: 6px solid #D32F2F; 
                margin-bottom: 20px; 
            }}
            .cover-title {{ font-size: 32pt; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }}
            .cover-sub {{ font-size: 14pt; color: #FFD700; margin-top: 5px; font-weight: bold; }}
            .cover-hook {{ 
                margin-top: 15px; 
                font-size: 10pt; 
                color: #ccc; 
                font-style: italic; 
                border-top: 1px solid #444; 
                padding-top: 10px;
                max-width: 80%;
                margin-left: auto;
                margin-right: auto;
            }}
            
            h2 {{ color: #D32F2F; border-bottom: 2px solid #ddd; padding-bottom: 5px; margin-top: 20px; font-size: 13pt; text-transform: uppercase; }}
            
            /* TABLES & BOXES */
            .benchmark-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            .benchmark-table th {{ background: #333; color: white; padding: 8px; font-size: 9pt; }}
            .benchmark-table td {{ border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 10pt; }}
            .my-biz {{ background: #ffe6e6; font-weight: bold; border: 2px solid #D32F2F; }}
            
            .card {{ border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 4px; page-break-inside: avoid; }}
            .card-header {{ background: #f8f9fa; padding: 6px; font-weight: bold; display: flex; justify-content: space-between; border-bottom: 1px solid #eee; }}
            
            .badge {{ font-size: 8pt; padding: 2px 6px; border-radius: 4px; color: white; }}
            .badge-fail {{ background: #D32F2F; }} .badge-pass {{ background: #2E7D32; }} .badge-warn {{ background: #F57F17; }}
            
            .problem-row {{ color: #D32F2F; font-weight: bold; margin-top: 5px; }}
            .success-row {{ color: #2E7D32; font-weight: bold; margin-top: 5px; }}
            .impact-row {{ margin-top: 5px; padding: 5px; background-color: #fff0f0; color: #b71c1c; font-style: italic; border-left: 3px solid #b71c1c; font-size: 9pt; }}
            
            /* ROADMAP STYLING */
            .roadmap-box {{ 
                background: #F0FDF4; 
                border: 2px solid #16A34A; 
                padding: 20px; 
                margin-top: 15px; 
                border-radius: 8px;
            }}
            .phase {{ margin-bottom: 15px; border-left: 4px solid #16A34A; padding-left: 12px; }}
            .phase-title {{ font-weight: 800; color: #166534; font-size: 11pt; text-transform: uppercase; }}
            .phase ul {{ margin: 5px 0 0 0; padding-left: 20px; }}
            .phase li {{ margin-bottom: 4px; color: #333; }}
            
            /* CONVERSION BUTTON (High UI) */
            .cta-container {{ text-align: center; margin-top: 25px; margin-bottom: 20px; }}
            .cta-link {{ 
                display: inline-block;
                background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
                color: white; 
                text-align: center; 
                padding: 18px 30px; 
                text-decoration: none; 
                font-weight: 800; 
                font-size: 12pt;
                border-radius: 8px; 
                box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4);
                border-bottom: 4px solid #8E0000;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
        </style>
    </head>
    <body>

        <!-- PAGE 1: HOOK & SUMMARY -->
        <div class="cover-header">
            <div class="cover-title">MONEY-LEAK AUDIT</div>
            <div class="cover-sub">Strategy Report for: {business_name}</div>
            <div class="cover-hook">
                CONFIDENTIAL: An analysis of why {business_name} is losing market share to competitors—and the exact protocol to reclaim it.
            </div>
        </div>

        <div style="background: #fff0f0; border-left: 5px solid #D32F2F; padding: 15px; font-size: 10pt; margin-bottom: 15px;">
            <p><strong>🚨 EXECUTIVE SUMMARY:</strong></p>
            <p>{business_name} is currently <strong>'Invisible' to ~45% of local searchers.</strong></p>
            <p><strong>This is not a branding issue. This is a direct revenue leak.</strong></p>
        </div>

        <h2>⚔️ COMPETITIVE BENCHMARK (THE ENEMY)</h2>
        <table class="benchmark-table">
            <tr>
                <th>Metric</th>
                <th>Market Leader</th>
                <th>{business_name} (You)</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>Reviews</td>
                <td>{competitor_avg_reviews}+</td>
                <td class="{ 'my-biz' if s4_badge != '<span class=\'badge badge-pass\'>✅ PASS</span>' else '' }">{rev_count}</td>
                <td>{s4_badge}</td>
            </tr>
            <tr>
                <td>Rating</td>
                <td>4.8+</td>
                <td class="{ 'my-biz' if rating < 4.0 else '' }">{rating}</td>
                <td>{ '<span class="badge badge-fail">FAIL</span>' if rating < 4.0 else '<span class="badge badge-pass">PASS</span>' }</td>
            </tr>
             <tr>
                <td>Website/Booking</td>
                <td>Optimized</td>
                <td class="{ 'my-biz' if not has_website else '' }">{'MISSING' if not has_website else 'Linked'}</td>
                <td>{s3_badge}</td>
            </tr>
        </table>

        <!-- 1. VISIBILITY -->
        <div class="card">
            <div class="card-header"><span>1️⃣ LOST VISIBILITY → LOST CUSTOMERS</span> {s1_badge}</div>
            {s1_text}
            <div class="impact-row">💸 Impact: Losing 5 calls/day × Avg Sale Value = Thousands lost monthly.</div>
        </div>

        <!-- 2. CTR -->
        <div class="card">
            <div class="card-header"><span>2️⃣ LOW CLICK-THROUGH RATE (CTR)</span> {s2_badge}</div>
            {s2_text}
            <div class="impact-row">💸 Impact: People choose who looks more active, not who is better.</div>
        </div>

        <!-- 3. WEBSITE -->
        <div class="card">
            <div class="card-header"><span>3️⃣ BUYER CONFUSION (WEBSITE)</span> {s3_badge}</div>
            {s3_text}
            <div class="impact-row">💸 Impact: You lose ready-to-buy customers due to lack of clarity.</div>
        </div>
        
        <div style="page-break-before: always;"></div>

        <!-- 4. REVIEWS -->
        <div class="card">
            <div class="card-header"><span>4️⃣ WEAK REVIEW STRATEGY → TRUST LOSS</span> {s4_badge}</div>
            {s4_text}
            <div class="impact-row">💸 Impact: A 0.2 star gap can reduce conversions by 20%.</div>
        </div>

        <!-- 5. POSTS -->
        <div class="card">
            <div class="card-header"><span>5️⃣ ZERO POSTS / OFFERS → DEAD LISTING</span> {s5_badge}</div>
            {s5_text}
            <div class="impact-row">💸 Impact: You lose customers to competitors who show Offers.</div>
        </div>

        <!-- 6. PHOTOS -->
        <div class="card">
            <div class="card-header"><span>6️⃣ POOR VISUAL AUTHORITY → LOW FOOTFALL</span> {s6_badge}</div>
            {s6_text}
            <div class="impact-row">💸 Impact: Fewer direction clicks → fewer walk-ins.</div>
        </div>
        
        <!-- 7. REPUTATION -->
        <div class="card">
            <div class="card-header"><span>7️⃣ REPUTATION (Q&A RISK)</span> {s7_badge}</div>
            <p class="problem-row">❌ ANALYSIS: Uncontrolled Q&A detected.</p>
            <div class="impact-row">💸 Impact: One unanswered negative question can kill multiple sales.</div>
        </div>

        <!-- 8. ALGORITHM -->
        <div class="card">
            <div class="card-header"><span>8️⃣ ALGORITHM SIGNALS</span> {s8_badge}</div>
            <p class="problem-row">❌ ANALYSIS: Low Engagement Signals.</p>
            <div class="impact-row">💸 Impact: Lower engagement → lower ranking.</div>
        </div>

        <div style="page-break-before: always;"></div>

        <!-- ROADMAP SECTION -->
        <div class="roadmap-box">
            <h2 style="color: #166534; border-color: #16A34A; margin-top: 0; text-align: center;">🚀 THE 90-DAY RECOVERY PROTOCOL</h2>
            
            <div class="phase">
                <div class="phase-title">PHASE 1: FOUNDATION REPAIR (Days 1-14)</div>
                <ul>
                    <li>✅ <strong>Reconnect Revenue Funnel:</strong> { 'Establish High-Converting Landing Page' if not has_website else 'Technical Audit of Booking Link' }.</li>
                    <li>✅ <strong>Visual Authority Surge:</strong> Upload 20+ meta-tagged photos to force Google to see you as "Active".</li>
                    <li>✅ <strong>Category Alignment:</strong> Fix backend signals to match high-intent search terms.</li>
                </ul>
            </div>

            <div class="phase">
                <div class="phase-title">PHASE 2: TRUST ACCELERATION (Days 15-45)</div>
                <ul>
                    <li>🚀 <strong>Review Reactivation:</strong> Launch SMS campaign to convert past customers into 5-star reviews.</li>
                    <li>🚀 <strong>Defense Grid:</strong> Seed Q&A section to answer objections before they call.</li>
                    <li>🚀 <strong>Conversion Copy:</strong> Rewrite business description with psychological triggers.</li>
                </ul>
            </div>

            <div class="phase">
                <div class="phase-title">PHASE 3: TOTAL DOMINANCE (Days 45-90)</div>
                <ul>
                    <li>🔥 <strong>Algorithm Pulse:</strong> Weekly "Offer Posts" to signal constant activity to Google.</li>
                    <li>🔥 <strong>Competitor Displacement:</strong> Monitor rival rankings and adjust bids to steal their traffic.</li>
                    <li>🔥 <strong>Revenue Reporting:</strong> Monthly breakdown of calls, clicks, and captured revenue.</li>
                </ul>
            </div>
            
            <div class="cta-container">
                <a href="https://calendly.com/mondal-kiran1980/30min" class="cta-link">
                    👉 CLICK TO ACTIVATE PHASE 1 NOW
                </a>
                <p style="font-size: 8pt; margin-top: 10px; color: #666;">(Limited availability for new partners in {currency} region)</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 8pt;">
            Generated by Kaydiem Script Lab RLAS V3.0
        </div>

    </body>
    </html>
    """
    
    return HTML(string=html).write_pdf()
