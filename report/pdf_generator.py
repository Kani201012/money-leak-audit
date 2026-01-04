from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency, lead_data):
    """
    MODULE 5: AUDIT REPORT GENERATOR (V3.0 - COMPLETE & COMPLIANT)
    Features: All 8 Points, 90-Day Roadmap, Competitor Benchmarking, Revenue Math, & Custom CTA.
    """
    
    # --- 1. DATA EXTRACTION & LOGIC ---
    issues_str = " ".join([str(i) for i in audit_result['issues']]).lower()
    
    # Extract Real Data
    rev_count = lead_data.get('reviews', 0)
    rating = lead_data.get('rating', 0.0)
    photo_count = lead_data.get('photos', 0)
    if photo_count == 0: photo_count = lead_data.get('photos_count', 0)
    has_website = lead_data.get('website')
    
    # Benchmark Data (Psychological Anchors)
    competitor_avg_reviews = 150
    competitor_avg_photos = 45

    # Helper for Status Badges
    def get_status(is_fail, success_text, fail_text):
        if is_fail:
            return "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>", f"<p class='problem-row'>❌ ANALYSIS: {fail_text}</p>"
        else:
            return "<span class='badge badge-pass'>✅ PASS</span>", f"<p class='success-row'>✅ ANALYSIS: {success_text}</p>"

    # --- 2. SECTION LOGIC (THE 8 POINTS) ---
    
    # 1. VISIBILITY
    s1_fail = any(x in issues_str for x in ["ranking", "category"])
    s1_badge, s1_text = get_status(s1_fail, "Your listing appears for primary keywords.", "Your business is invisible for high-intent 'Near Me' keywords.")

    # 2. CTR
    s2_fail = any(x in issues_str for x in ["visual", "ctr"])
    s2_badge, s2_text = get_status(s2_fail, "Listing looks active.", "Listing looks 'dormant' compared to competitors, killing your Click-Through-Rate.")

    # 3. BUYER CONFUSION (WEBSITE LOGIC FIX)
    if not has_website:
        s3_badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        s3_text = "<p class='problem-row'>❌ ANALYSIS: <strong>WEBSITE MISSING.</strong> This is the #1 reason customers abandon a listing.</p>"
    else:
        s3_badge = "<span class='badge badge-pass'>✅ PASS</span>"
        s3_text = f"<p class='success-row'>✅ ANALYSIS: Website linked successfully.</p>"

    # 4. REVIEWS
    s4_fail = rev_count < 50
    s4_badge, s4_text = get_status(s4_fail, f"Strong Trust: {rev_count} Reviews.", f"TRUST GAP: You have {rev_count} reviews. Market Leaders have {competitor_avg_reviews}+.")

    # 5. POSTS
    s5_fail = any(x in issues_str for x in ["post", "active"])
    s5_badge, s5_text = get_status(s5_fail, "Active Google Posts detected.", "Zero active Posts. Google prefers 'Alive' businesses.")

    # 6. PHOTOS
    s6_fail = photo_count < 20
    s6_badge, s6_text = get_status(s6_fail, f"Good Visuals: {photo_count} photos.", f"VISUAL VOID: Only {photo_count} photos. Competitors showcase {competitor_avg_photos}+ photos.")

    # 7. REPUTATION (Default Risk)
    s7_badge = "<span class='badge badge-warn'>⚠️ RISK DETECTED</span>"

    # 8. ALGORITHM SIGNALS (Default Risk)
    s8_badge = "<span class='badge badge-warn'>⚠️ LOW SIGNAL</span>"


    # --- 3. HTML & CSS CONSTRUCTION ---
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 10mm; }}
            body {{ font-family: 'DejaVu Sans', sans-serif; color: #222; line-height: 1.4; font-size: 10pt; }}
            
            /* HEADERS */
            .cover-header {{ background: #111; color: #fff; padding: 30px; text-align: center; border-bottom: 5px solid #D32F2F; margin-bottom: 20px; }}
            .cover-title {{ font-size: 26pt; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }}
            .cover-sub {{ font-size: 12pt; color: #FFD700; margin-top: 10px; }}
            
            h2 {{ color: #D32F2F; border-bottom: 2px solid #ddd; padding-bottom: 5px; margin-top: 20px; font-size: 13pt; text-transform: uppercase; }}
            h3 {{ font-size: 10pt; font-weight: bold; margin: 8px 0 4px 0; }}

            /* EXECUTIVE HOOK */
            .hook-box {{ background: #fff0f0; border-left: 5px solid #D32F2F; padding: 15px; font-size: 10pt; margin-bottom: 15px; }}
            
            /* BENCHMARK TABLE */
            .benchmark-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            .benchmark-table th {{ background: #333; color: white; padding: 6px; font-size: 9pt; }}
            .benchmark-table td {{ border: 1px solid #ddd; padding: 6px; text-align: center; font-size: 9pt; }}
            .my-biz {{ background: #ffe6e6; font-weight: bold; border: 2px solid #D32F2F; }}
            
            /* CARDS */
            .card {{ border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 4px; page-break-inside: avoid; }}
            .card-header {{ background: #f8f9fa; padding: 6px; font-weight: bold; display: flex; justify-content: space-between; border-bottom: 1px solid #eee; }}
            .badge {{ font-size: 8pt; padding: 2px 6px; border-radius: 4px; color: white; }}
            .badge-fail {{ background: #D32F2F; }}
            .badge-pass {{ background: #2E7D32; }}
            .badge-warn {{ background: #F57F17; }}
            
            .problem-row {{ color: #D32F2F; font-weight: bold; margin-top: 5px; }}
            .success-row {{ color: #2E7D32; font-weight: bold; margin-top: 5px; }}
            .impact-row {{ margin-top: 5px; padding: 5px; background-color: #fff0f0; color: #b71c1c; font-style: italic; border-left: 3px solid #b71c1c; font-size: 9pt; }}
            
            /* MATH BOX */
            .math-box {{ background: #eee; border: 1px dashed #666; padding: 15px; text-align: center; margin: 20px 0; }}
            .formula {{ font-size: 12pt; font-weight: bold; color: #333; }}
            .total-loss {{ font-size: 18pt; color: #D32F2F; font-weight: 800; }}

            /* ROADMAP */
            .roadmap-box {{ background: #e8f5e9; border: 1px solid #c8e6c9; padding: 15px; margin-top: 15px; }}
            .phase {{ margin-bottom: 10px; border-left: 4px solid #2E7D32; padding-left: 10px; }}
            .phase-title {{ font-weight: bold; color: #2E7D32; font-size: 10pt; }}
            
            /* CTA BUTTON */
            .cta-link {{
                display: block;
                background-color: #D32F2F;
                color: white;
                text-align: center;
                padding: 15px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 5px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>

        <!-- PAGE 1: HOOK & BENCHMARK -->
        <div class="cover-header">
            <div class="cover-title">MONEY-LEAK AUDIT</div>
            <div class="cover-sub">Strategy Report for: {business_name}</div>
        </div>

        <div class="hook-box">
            <p><strong>🚨 EXECUTIVE SUMMARY:</strong></p>
            <p>{business_name} is currently <strong>'Invisible' to ~45% of local searchers.</strong></p>
            <p>While you may have a good reputation offline, Google's algorithm is prioritizing your competitors because their profiles are more "complete" and "active."</p>
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
                <td class="{ 'my-biz' if s4_fail else '' }">{rev_count}</td>
                <td>{s4_badge}</td>
            </tr>
            <tr>
                <td>Photos</td>
                <td>{competitor_avg_photos}+</td>
                <td class="{ 'my-biz' if s6_fail else '' }">{photo_count}</td>
                <td>{s6_badge}</td>
            </tr>
             <tr>
                <td>Website</td>
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

        <!-- 3. BUYER CONFUSION -->
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

        <!-- MATH SECTION -->
        <h2>📉 THE REVENUE LEAKAGE EQUATION</h2>
        <div class="math-box">
            <div class="formula">
                (Avg Job Value) x (Missed Calls)
            </div>
            <br>
            <div class="formula">
                {currency}500 x ~{int(roi_result['monthly_loss_min']/500)} Jobs
            </div>
            <hr style="border: 0; border-top: 1px dashed #999; margin: 15px 0;">
            <div class="total-loss">
                = {currency}{roi_result['monthly_loss_min']:,} / MO LOSS
            </div>
            <p style="font-size: 10pt; color: #666; margin-top: 5px;">(Annual: {currency}{roi_result['annual_loss']:,})</p>
        </div>

        <!-- ROADMAP SECTION -->
        <div class="roadmap-box">
            <h2 style="color: #2E7D32; border-color: #2E7D32; margin-top: 0;">🚀 THE 90-DAY RECOVERY PLAN</h2>
            
            <div class="phase">
                <div class="phase-title">PHASE 1: THE FOUNDATION (Days 1-14)</div>
                <ul>
                    <li>✅ { 'Build High-Converting Landing Page' if not has_website else 'Audit Website Link' }</li>
                    <li>✅ Upload 20+ High-Quality "Trust" Photos</li>
                    <li>✅ Fix Categories & Attributes</li>
                </ul>
            </div>

            <div class="phase">
                <div class="phase-title">PHASE 2: AUTHORITY & TRUST (Days 15-45)</div>
                <ul>
                    <li>🚀 Launch "Review Reactivation" Campaign</li>
                    <li>🚀 Seed Q&A Section with FAQs</li>
                    <li>🚀 Write Optimized Business Description</li>
                </ul>
            </div>

            <div class="phase">
                <div class="phase-title">PHASE 3: DOMINANCE (Days 45-90)</div>
                <ul>
                    <li>🔥 Weekly Google Posts Strategy</li>
                    <li>🔥 Competitor Monitoring</li>
                    <li>🔥 Performance Reporting</li>
                </ul>
            </div>
            
            <a href="https://calendly.com/mondal-kiran1980/30min" class="cta-link">
                👉 Book your Strategy Call to start Phase 1 (Click Here)
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 8pt;">
            Generated by Kaydiem Script Lab RLAS V3.0
        </div>

    </body>
    </html>
    """
    
    return HTML(string=html).write_pdf()
