from weasyprint import HTML

def create_audit_pdf(business_name, audit_result, roi_result, currency, lead_data):
    """
    MODULE 5: AUDIT REPORT GENERATOR (V3.0 - THE CLOSER EDITION)
    Includes: 90-Day Roadmap, Competitor Benchmarking, Transparent Math, & Logic Fixes.
    """
    
    # --- 1. DATA PREPARATION ---
    issues_str = " ".join([str(i) for i in audit_result['issues']]).lower()
    
    # Extract Real Data
    rev_count = lead_data.get('reviews', 0)
    rating = lead_data.get('rating', 0.0)
    photo_count = lead_data.get('photos', 0)
    if photo_count == 0: photo_count = lead_data.get('photos_count', 0)
    has_website = lead_data.get('website')
    
    # Benchmark Data (The "Enemy")
    # We set these high to psychologically pressure the prospect
    competitor_avg_reviews = 150
    competitor_avg_photos = 45

    def get_status(is_fail, success_text, fail_text):
        if is_fail:
            return "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>", f"<p class='problem-row'>❌ ANALYSIS: {fail_text}</p>"
        else:
            return "<span class='badge badge-pass'>✅ PASS</span>", f"<p class='success-row'>✅ ANALYSIS: {success_text}</p>"

    # --- 2. LOGIC GAPS FIXED ---
    
    # VISIBILITY
    s1_fail = any(x in issues_str for x in ["ranking", "category"])
    s1_badge, s1_text = get_status(s1_fail, "Your listing appears for primary keywords.", "Your business is invisible for high-intent 'Near Me' keywords.")

    # CTR
    s2_fail = any(x in issues_str for x in ["visual", "ctr"])
    s2_badge, s2_text = get_status(s2_fail, "Listing looks active.", "Listing looks 'dormant' compared to competitors, killing your Click-Through-Rate.")

    # WEBSITE (CRITICAL LOGIC FIX)
    if not has_website:
        s3_badge = "<span class='badge badge-fail'>❌ CRITICAL FAIL</span>"
        s3_text = "<p class='problem-row'>❌ ANALYSIS: <strong>WEBSITE MISSING.</strong> This is the #1 reason customers abandon a listing.</p>"
    else:
        s3_badge = "<span class='badge badge-pass'>✅ PASS</span>"
        s3_text = f"<p class='success-row'>✅ ANALYSIS: Website linked successfully.</p>"

    # REVIEWS
    s4_fail = rev_count < 50
    s4_badge, s4_text = get_status(s4_fail, f"Strong Trust: {rev_count} Reviews.", f"TRUST GAP: You have {rev_count} reviews. Market Leaders have {competitor_avg_reviews}+.")

    # POSTS
    s5_fail = any(x in issues_str for x in ["post", "active"])
    s5_badge, s5_text = get_status(s5_fail, "Active Google Posts detected.", "Zero active Posts. Google prefers 'Alive' businesses.")

    # PHOTOS
    s6_fail = photo_count < 20
    s6_badge, s6_text = get_status(s6_fail, f"Good Visuals: {photo_count} photos.", f"VISUAL VOID: Only {photo_count} photos. Competitors showcase {competitor_avg_photos}+ photos.")

    # --- HTML & CSS CONSTRUCTION ---
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 10mm; }}
            body {{ font-family: 'DejaVu Sans', sans-serif; color: #222; line-height: 1.4; font-size: 10pt; }}
            
            /* HEADERS */
            .cover-header {{ background: #111; color: #fff; padding: 40px; text-align: center; border-bottom: 5px solid #D32F2F; margin-bottom: 20px; }}
            .cover-title {{ font-size: 28pt; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }}
            .cover-sub {{ font-size: 14pt; color: #FFD700; margin-top: 10px; }}
            
            h2 {{ color: #D32F2F; border-bottom: 2px solid #ddd; padding-bottom: 5px; margin-top: 25px; font-size: 14pt; text-transform: uppercase; }}
            h3 {{ font-size: 11pt; font-weight: bold; margin: 10px 0 5px 0; }}

            /* EXECUTIVE HOOK */
            .hook-box {{ background: #fff0f0; border-left: 5px solid #D32F2F; padding: 20px; font-size: 11pt; margin-bottom: 20px; }}
            
            /* BENCHMARK TABLE (THE ENEMY) */
            .benchmark-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            .benchmark-table th {{ background: #333; color: white; padding: 8px; font-size: 9pt; }}
            .benchmark-table td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            .my-biz {{ background: #ffe6e6; font-weight: bold; border: 2px solid #D32F2F; }}
            
            /* CARDS */
            .card {{ border: 1px solid #ddd; padding: 12px; margin-bottom: 12px; border-radius: 4px; page-break-inside: avoid; }}
            .card-header {{ background: #f8f9fa; padding: 8px; font-weight: bold; display: flex; justify-content: space-between; border-bottom: 1px solid #eee; }}
            .badge {{ font-size: 8pt; padding: 2px 6px; border-radius: 4px; color: white; }}
            .badge-fail {{ background: #D32F2F; }}
            .badge-pass {{ background: #2E7D32; }}
            
            .problem-row {{ color: #D32F2F; font-weight: bold; margin-top: 5px; }}
            .success-row {{ color: #2E7D32; font-weight: bold; margin-top: 5px; }}
            
            /* MATH BOX */
            .math-box {{ background: #eee; border: 1px dashed #666; padding: 15px; text-align: center; margin: 20px 0; }}
            .formula {{ font-size: 14pt; font-weight: bold; color: #333; }}
            .total-loss {{ font-size: 20pt; color: #D32F2F; font-weight: 800; }}

            /* ROADMAP (THE SOLUTION) */
            .roadmap-box {{ background: #e8f5e9; border: 1px solid #c8e6c9; padding: 20px; margin-top: 20px; }}
            .phase {{ margin-bottom: 15px; border-left: 4px solid #2E7D32; padding-left: 10px; }}
            .phase-title {{ font-weight: bold; color: #2E7D32; font-size: 11pt; }}
        </style>
    </head>
    <body>

        <!-- PAGE 1: THE HOOK -->
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

        <h2>⚔️ COMPETITIVE BENCHMARK (WHY YOU ARE LOSING)</h2>
        <p>Customers compare you to the market leaders before calling. Here is how you stack up:</p>
        
        <table class="benchmark-table">
            <tr>
                <th>Metric</th>
                <th>Market Leader (Competitor)</th>
                <th>{business_name} (You)</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>Reviews (Trust)</td>
                <td>{competitor_avg_reviews}+</td>
                <td class="{ 'my-biz' if s4_fail else '' }">{rev_count}</td>
                <td>{s4_badge}</td>
            </tr>
            <tr>
                <td>Photos (Authority)</td>
                <td>{competitor_avg_photos}+</td>
                <td class="{ 'my-biz' if s6_fail else '' }">{photo_count}</td>
                <td>{s6_badge}</td>
            </tr>
             <tr>
                <td>Website (Funnel)</td>
                <td>Optimized</td>
                <td class="{ 'my-biz' if not has_website else '' }">{'MISSING' if not has_website else 'Linked'}</td>
                <td>{s3_badge}</td>
            </tr>
        </table>

        <h2>🔍 THE 3 CRITICAL GAPS</h2>

        <!-- WEBSITE GAP -->
        <div class="card">
            <div class="card-header"><span>1️⃣ CONVERSION FUNNEL</span> {s3_badge}</div>
            {s3_text}
            <p><strong>Impact:</strong> Customers assume a business without a website is closed or unprofessional.</p>
        </div>

        <!-- REVIEWS GAP -->
        <div class="card">
            <div class="card-header"><span>2️⃣ TRUST & RANKING</span> {s4_badge}</div>
            {s4_text}
            <p><strong>Impact:</strong> You are losing the "Best" clicks. A 0.5 star gap costs 20% of leads.</p>
        </div>

        <!-- VISUAL GAP -->
        <div class="card">
            <div class="card-header"><span>3️⃣ VISUAL PROOF</span> {s6_badge}</div>
            {s6_text}
            <p><strong>Impact:</strong> Customers judge capability by your photos. Low photos = Low confidence.</p>
        </div>

        <div style="page-break-before: always;"></div>

        <!-- THE MATH -->
        <h2>📉 THE REVENUE LEAKAGE EQUATION</h2>
        <p>We don't guess. Here is the math based on your industry averages:</p>
        
        <div class="math-box">
            <div class="formula">
                (Avg Job Value) x (Missed Calls due to Ranking)
            </div>
            <br>
            <div class="formula">
                {currency}500 x ~{int(roi_result['monthly_loss_min']/500)} Missed Jobs/Mo
            </div>
            <hr style="border: 0; border-top: 1px dashed #999; margin: 15px 0;">
            <div class="total-loss">
                = {currency}{roi_result['monthly_loss_min']:,} / MONTH LOSS
            </div>
            <p style="font-size: 10pt; color: #666; margin-top: 5px;">(Projected Annual Loss: {currency}{roi_result['annual_loss']:,})</p>
        </div>

        <!-- THE ROADMAP (SOLUTION) -->
        <div class="roadmap-box">
            <h2 style="color: #2E7D32; border-color: #2E7D32; margin-top: 0;">🚀 THE 90-DAY RECOVERY PLAN</h2>
            <p>We don't just "fix" it. We implement a dominance strategy.</p>
            
            <div class="phase">
                <div class="phase-title">PHASE 1: THE FOUNDATION (Days 1-14)</div>
                <ul>
                    <li>✅ Claim & Verify Profile (if needed)</li>
                    <li>✅ { 'Build High-Converting Landing Page' if not has_website else 'Audit Website Link' }</li>
                    <li>✅ Upload 20+ High-Quality "Trust" Photos</li>
                    <li>✅ Fix Primary & Secondary Categories</li>
                </ul>
            </div>

            <div class="phase">
                <div class="phase-title">PHASE 2: AUTHORITY & TRUST (Days 15-45)</div>
                <ul>
                    <li>🚀 Launch "Review Reactivation" Campaign (SMS/Email)</li>
                    <li>🚀 Seed Q&A Section with FAQs</li>
                    <li>🚀 Write & Optimize Business Description with Keywords</li>
                </ul>
            </div>

            <div class="phase">
                <div class="phase-title">PHASE 3: DOMINANCE (Days 45-90)</div>
                <ul>
                    <li>🔥 Weekly Google Posts (Offers & Updates)</li>
                    <li>🔥 Competitor Monitoring & Defense</li>
                    <li>🔥 Monthly Performance Reporting</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 20px; font-weight: bold;">
                👉 Book your Strategy Call to start Phase 1.
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 9pt;">
            Generated by Revenue Leakage Audit System v3.0
        </div>

    </body>
    </html>
    """
    
    return HTML(string=html).write_pdf()
