import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time

# Import Modules
from prospector.maps_scraper import find_leads
from harvester.gbp_data import normalize_gbp_data
from audit.leakage_index import calculate_rli_score
from audit.roi_calculator import calculate_money_loss
from report.pdf_generator import create_audit_pdf
from modules.pipeline_manager import add_lead, load_db, update_lead_status, delete_lead, get_metrics
from modules.outreach import generate_cold_email
from modules.scan_history import save_scan, load_history

# --- PAGE CONFIG ---
st.set_page_config(page_title="CRGG Growth OS", layout="wide", initial_sidebar_state="collapsed")

# --- CSS INJECTION (SAAS GRADE UI) ---
st.markdown("""
<style>
    /* GLOBAL FONTS & COLORS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #F8FAFC; /* Light Blue-Grey Background */
        font-family: 'Inter', sans-serif;
    }
    
    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* CUSTOM HEADLINES */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 400;
    }
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* THE AUDIT CARD (WHITE BOX) */
    .audit-card {
        background: white;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        max-width: 900px;
        margin: 0 auto;
        border: 1px solid #E2E8F0;
    }

    /* INPUT FIELDS STYLING */
    div[data-baseweb="input"] > div {
        background-color: #F1F5F9;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 5px;
    }
    
    /* GENERATE BUTTON */
    div.stButton > button {
        background-color: #0F172A;
        color: white;
        border-radius: 12px;
        padding: 15px 30px;
        font-weight: 600;
        width: 100%;
        border: none;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background-color: #1E293B;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* RESULT CARD STYLING */
    .result-box {
        background: white;
        border-radius: 16px;
        padding: 25px;
        margin-top: 20px;
        border-left: 6px solid #4F46E5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* NAVIGATION BAR CLEANUP */
    .nav-link-selected {
        background-color: #4F46E5 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CURRENCY LOGIC ---
def get_currency_symbol(location_text):
    if not location_text: return "$"
    loc = location_text.lower()
    if any(x in loc for x in ["saudi", "ksa", "riyadh", "dammam", "jeddah"]): return "SAR"
    if any(x in loc for x in ["uae", "dubai", "abu dhabi"]): return "AED"
    if any(x in loc for x in ["uk", "london", "manchester"]): return "£"
    if any(x in loc for x in ["europe", "germany", "france"]): return "€"
    if any(x in loc for x in ["india", "delhi", "mumbai"]): return "₹"
    return "$"

# --- NAVIGATION ---
selected = option_menu(
    menu_title=None,
    options=["Auditor", "Prospector", "Pipeline", "Mission Control"],
    icons=["search", "map", "kanban", "speedometer2"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0 5px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#4F46E5", "color": "white"},
    }
)

# ==========================================
# 🔍 VIEW 1: AUDITOR (SINGLE BUSINESS)
# ==========================================
if selected == "Auditor":
    
    # 1. HERO SECTION
    st.markdown("""
        <div style="margin-top: 40px;">
            <div class="hero-title">
                Stop pitching websites.<br>
                Start pitching <span class="gradient-text">Revenue.</span>
            </div>
            <div class="hero-subtitle">
                Enter a local business's details to calculate exactly how much monthly<br>
                revenue they are losing to their top competitors.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. THE AUDIT FORM (CENTERED CARD)
    with st.container():
        # Using columns to center the card visually (Streamlit hack)
        _, center_col, _ = st.columns([1, 6, 1])
        
        with center_col:
            st.markdown('<div class="audit-card">', unsafe_allow_html=True)
            
            # Row 1
            c1, c2 = st.columns(2)
            with c1:
                target_name = st.text_input("📍 Target Business Name", placeholder="e.g. Smile Dental Studio")
            with c2:
                target_web = st.text_input("🔗 Website URL (Optional)", placeholder="https://smiledental.com")
            
            # Row 2
            c3, c4 = st.columns(2)
            with c3:
                target_loc = st.text_input("🏙️ Location", placeholder="e.g. Chicago, IL")
            with c4:
                target_niche = st.text_input("🎯 Industry / Niche", placeholder="e.g. Dentist")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # THE BIG BUTTON
            audit_btn = st.button("⚡ GENERATE REVENUE AUDIT")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center; margin-top:20px; color:#94A3B8; font-size:0.8rem; font-weight:600; letter-spacing:1px;">TRUSTED BY 500+ TOP-TIER AGENCIES GLOBALLY</div>', unsafe_allow_html=True)

    # 3. AUDIT LOGIC
    if audit_btn:
        if not target_name or not target_loc:
            st.error("Please enter Business Name and Location to run the audit.")
        else:
            with st.spinner("🛰️ Satellite Audit In Progress... analyzing map pack ranking..."):
                # Use the existing scraper but specifically for this one business
                # We search for "Business Name in Location"
                raw_leads = find_leads(target_name, target_loc)
                
                # Filter to find the EXACT match (or closest)
                target_lead = None
                if raw_leads:
                    # Simple fuzzy match: take the first result since we searched specifically
                    target_lead = raw_leads[0] 
                
                if not target_lead:
                    st.warning(f"Could not find '{target_name}' on Google Maps in '{target_loc}'. Try refining the location.")
                else:
                    # PROCESS THE LEAD
                    currency_symbol = get_currency_symbol(target_loc)
                    data = normalize_gbp_data(target_lead)
                    audit = calculate_rli_score(data)
                    roi = calculate_money_loss(audit['rli_score'], 500, 50) # Defaults
                    
                    # --- DISPLAY RESULTS (SAAS STYLE) ---
                    st.markdown("<hr style='margin: 40px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
                    
                    r1, r2 = st.columns([1, 1])
                    
                    with r1:
                        st.markdown(f"""
                        <div class="result-box">
                            <h3 style="margin:0;">📉 Revenue Leakage Detected</h3>
                            <div style="font-size: 2.5rem; font-weight: 800; color: #DC2626;">
                                {currency_symbol}{roi['monthly_loss_min']:,} <span style="font-size:1rem; color:#64748B;">/ month</span>
                            </div>
                            <p style="color:#64748B;">Based on {audit['rli_score']}/100 Risk Score</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with r2:
                        st.markdown(f"""
                        <div class="result-box" style="border-left-color: #10B981;">
                            <h3 style="margin:0;">🔍 Audit Summary</h3>
                            <ul style="margin-top:10px; color:#334155;">
                                <li><strong>Listing:</strong> {data['name']}</li>
                                <li><strong>Rating:</strong> {data['rating']} ⭐ ({data['reviews']} reviews)</li>
                                <li><strong>Website:</strong> {'✅ Linked' if data['has_website'] else '❌ MISSING'}</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                    # PDF DOWNLOAD
                    pdf = create_audit_pdf(data['name'], audit, roi, currency_symbol, data)
                    st.download_button(
                        label="📄 DOWNLOAD CLIENT REPORT (PDF)",
                        data=pdf,
                        file_name=f"{data['name']}_Audit_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # ADD TO PIPELINE OPTION
                    if st.button("📥 SAVE TARGET TO PIPELINE", use_container_width=True):
                        target_lead['audit_score'] = audit['rli_score']
                        target_lead['monthly_gap'] = roi['monthly_loss_min']
                        target_lead['currency'] = currency_symbol
                        if add_lead(target_lead):
                            st.success(f"{data['name']} added to Pipeline!")
                        else:
                            st.warning("Target already exists in pipeline.")


# ==========================================
# 🌍 VIEW 2: PROSPECTOR (BULK SEARCH)
# ==========================================
elif selected == "Prospector":
    
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            keyword = st.text_input("Industry", placeholder="e.g. Emergency Plumber")
        with c2:
            location = st.text_input("Region", placeholder="e.g. Los Angeles")
        with c3:
            st.write("") 
            st.write("") 
            run_btn = st.button("🚀 DEPLOY SCAN", use_container_width=True)

    if 'scan_results' not in st.session_state:
        st.session_state['scan_results'] = []

    if run_btn and keyword and location:
        with st.spinner("Scanning Market Data..."):
            raw_leads = find_leads(keyword, location)
            if not raw_leads:
                st.warning("No leads found.")
            else:
                for lead in raw_leads: lead['search_location'] = location 
                st.session_state['scan_results'] = raw_leads
                save_scan(keyword, location, raw_leads)
                st.toast(f"Acquired {len(raw_leads)} Targets", icon="✅")

    results = st.session_state['scan_results']
    if results:
        if st.button("Clear Results"):
            st.session_state['scan_results'] = []
            st.experimental_rerun()
            
         for i, lead in enumerate(results):
            loc = lead.get('search_location', location) 
            currency_symbol = get_currency_symbol(loc)
            data = normalize_gbp_data(lead)
            audit = calculate_rli_score(data)
            roi = calculate_money_loss(audit['rli_score'], 500, 50) 
            
            with st.container():
                c_info, c_actions = st.columns([3, 2])
                with c_info:
                    st.markdown(f"""
                    <div class="result-box" style="margin-top:0; padding:15px; border-left:4px solid #4F46E5;">
                        <h4 style="margin:0; color:#1E293B;">{data['name']}</h4>
                        <div style="font-size:0.9rem; color:#64748B; margin-top:5px;">
                            ⭐ {data['rating']} ({data['reviews']}) | 📍 {data['address'][:30]}...
                        </div>
                        <div style="margin-top:8px;">
                            <span style="background:#FEF2F2; color:#DC2626; padding:2px 8px; border-radius:4px; font-weight:700; font-size:0.8rem;">
                                GAP: {currency_symbol}{roi['monthly_loss_min']:,}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_actions:
                    st.write("")
                    b1, b2 = st.columns(2)
                    b3, b4 = st.columns(2)
                    with b1:
                        if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'], use_container_width=True)
                        else: st.button("No Map", disabled=True, key=f"nm_{lead['place_id']}_{i}", use_container_width=True)
                    with b2:
                        if lead.get('website'): st.link_button("🌐 Web", lead['website'], use_container_width=True)
                        else: st.button("No Web", disabled=True, key=f"nw_{lead['place_id']}_{i}", use_container_width=True)
                    with b3:
                        if st.button("📥 Track", key=f"add_{lead['place_id']}_{i}", use_container_width=True):
                            lead['audit_score'], lead['monthly_gap'], lead['currency'] = audit['rli_score'], roi['monthly_loss_min'], currency_symbol
                            if add_lead(lead): st.toast("Added", icon="✅")
                    with b4:
                        pdf = create_audit_pdf(data['name'], audit, roi, currency_symbol, data)
                        st.download_button("📄 Report", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"dl_{lead['place_id']}_{i}", use_container_width=True)

# ==========================================
# 📊 VIEW 3: PIPELINE
# ==========================================
elif selected == "Pipeline":
    val, count = get_metrics()
    st.markdown("## Mission Control")
    m1, m2, m3 = st.columns(3)
    m1.metric("Targets", count)
    m2.metric("Pipeline Value", f"${val:,.0f}")
    m3.metric("Status", "Active")
    st.divider()
    
    db = load_db()
    if not db: st.info("Pipeline is empty.")
    else:
        for lead in db:
            sym = lead.get('currency', "$")
            with st.expander(f"{lead['business_name']} | Gap: {sym}{lead.get('monthly_gap', 0):,}"):
                c_map, c_web, c_regen = st.columns([1, 1, 2])
                with c_map:
                    if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'])
                with c_web:
                    if lead.get('website'): st.link_button("🌐 Web", lead['website'])
                with c_regen:
                    if st.button("📄 Regenerate Report", key=f"regen_{lead['place_id']}"):
                        data = normalize_gbp_data(lead)
                        audit = calculate_rli_score(data)
                        roi = calculate_money_loss(audit['rli_score'], 500, 50)
                        pdf = create_audit_pdf(data['name'], audit, roi, sym, data)
                        st.download_button("Download Now", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"re_dl_{lead['place_id']}")
                st.divider()
                c1, c2 = st.columns([1, 2])
                with c1:
                    new_st = st.selectbox("Status", ["New Lead", "Outreach", "Negotiation", "Won", "Lost"], index=["New Lead", "Outreach", "Negotiation", "Won", "Lost"].index(lead.get('status', "New Lead")), key=f"st_{lead['place_id']}")
                    if new_st != lead.get('status'): update_lead_status(lead['place_id'], new_st); st.experimental_rerun()
                    if st.button("🗑️ Delete", key=f"del_{lead['place_id']}"): delete_lead(lead['place_id']); st.experimental_rerun()
                with c2:
                    t1, t2 = st.tabs(["✉️ Email", "📝 Notes"])
                    with t1:
                        kind = st.radio("Template", ["Initial", "Follow Up"], horizontal=True, key=f"r_{lead['place_id']}")
                        s, b = generate_cold_email(lead, f"T1 ({kind})")
                        st.text_input("Subject", s, key=f"s_{lead['place_id']}")
                        st.text_area("Body", b, height=150, key=f"b_{lead['place_id']}")
                    with t2:
                        st.text_area("Notes", lead.get('notes', ''), key=f"n_{lead['place_id']}")

# ==========================================
# 📈 VIEW 4: ANALYTICS
# ==========================================
elif selected == "Mission Control":
    st.markdown("## Deployment Registry")
    db = load_db()
    if db: st.dataframe(pd.DataFrame(db)[['business_name', 'status', 'monthly_gap']], use_container_width=True)
    else: st.info("No data.")
