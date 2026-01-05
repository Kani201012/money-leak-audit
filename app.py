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
        background-color: #F8FAFC; 
        font-family: 'Inter', sans-serif;
    }
    
    /* PREVENT STRETCHING ON WIDE SCREENS */
    .block-container { 
        max_width: 1000px; 
        padding-top: 2rem; 
        padding-bottom: 5rem; 
        margin: auto; 
    }
    
    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* HERO TEXT */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 30px;
    }
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* CARD DESIGN (PROSPECTOR) */
    .pro-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 10px;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #4F46E5;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    .pro-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    
    .biz-name { font-size: 1.25rem; font-weight: 700; color: #1E293B; margin-bottom: 5px; }
    .biz-meta { font-size: 0.9rem; color: #64748B; display: flex; gap: 15px; align-items: center; margin-bottom: 10px; }
    
    /* BADGES */
    .rating-badge { background: #FEF3C7; color: #D97706; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; }
    .gap-badge { background: #FEE2E2; color: #991B1B; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; }
    
    /* AUDIT CARD (AUDITOR) */
    .audit-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
    }

    /* NAVIGATION BAR */
    .nav-link-selected { background-color: #4F46E5 !important; }
    
    /* BUTTONS */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #E5E7EB;
        transition: all 0.2s;
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
    st.markdown("""
        <div style="margin-top: 30px;">
            <div class="hero-title">
                Stop pitching websites.<br>
                Start pitching <span class="gradient-text">Revenue.</span>
            </div>
            <div class="hero-subtitle">
                Calculate exactly how much monthly revenue a local business is losing.
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        # Centered Card Layout
        _, center_col, _ = st.columns([1, 8, 1])
        with center_col:
            st.markdown('<div class="audit-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: target_name = st.text_input("📍 Business Name", placeholder="e.g. Smile Dental")
            with c2: target_loc = st.text_input("🏙️ Location", placeholder="e.g. Chicago, IL")
            
            st.write("")
            audit_btn = st.button("⚡ GENERATE AUDIT", use_container_width=True, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

    if audit_btn:
        if not target_name or not target_loc:
            st.error("Please enter Name and Location.")
        else:
            with st.spinner("Analyzing Map Pack..."):
                raw_leads = find_leads(target_name, target_loc)
                target_lead = raw_leads[0] if raw_leads else None
                
                if not target_lead:
                    st.warning(f"Could not find '{target_name}' in '{target_loc}'.")
                else:
                    currency_symbol = get_currency_symbol(target_loc)
                    data = normalize_gbp_data(target_lead)
                    audit = calculate_rli_score(data)
                    roi = calculate_money_loss(audit['rli_score'], 500, 50)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
                    r1, r2 = st.columns(2)
                    with r1:
                        st.markdown(f"""
                        <div style="background:white; padding:20px; border-radius:12px; border-left:5px solid #DC2626; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                            <h3 style="margin:0; color:#DC2626;">📉 Revenue Leakage</h3>
                            <div style="font-size:2rem; font-weight:800; color:#1E293B;">{currency_symbol}{roi['monthly_loss_min']:,}</div>
                            <div style="color:#64748B;">Monthly Loss Estimate</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with r2:
                        pdf = create_audit_pdf(data['name'], audit, roi, currency_symbol, data)
                        st.download_button("📄 DOWNLOAD REPORT", data=pdf, file_name=f"{data['name']}_Audit.pdf", mime="application/pdf", use_container_width=True)
                        if st.button("📥 Add to Pipeline", use_container_width=True):
                            target_lead['audit_score'], target_lead['monthly_gap'], target_lead['currency'] = audit['rli_score'], roi['monthly_loss_min'], currency_symbol
                            add_lead(target_lead)
                            st.success("Added!")

# ==========================================
# 🌍 VIEW 2: PROSPECTOR (BULK SEARCH)
# ==========================================
elif selected == "Prospector":
    
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: keyword = st.text_input("Industry", placeholder="e.g. Emergency Plumber")
        with c2: location = st.text_input("Region", placeholder="e.g. Los Angeles")
        with c3:
            st.write("") 
            st.write("") 
            run_btn = st.button("🚀 DEPLOY SCAN", use_container_width=True, type="primary")

    if 'scan_results' not in st.session_state: st.session_state['scan_results'] = []

    if run_btn and keyword and location:
        with st.spinner("Hunting for weak profiles..."):
            raw_leads = find_leads(keyword, location)
            if not raw_leads:
                st.warning("No leads found.")
            else:
                for lead in raw_leads: lead['search_location'] = location 
                st.session_state['scan_results'] = raw_leads
                save_scan(keyword, location, raw_leads)
                st.toast(f"Found {len(raw_leads)} Targets", icon="✅")

    results = st.session_state['scan_results']
    if results:
        if st.button("Clear Results"): st.session_state['scan_results'] = []; st.experimental_rerun()
            
        # CRASH FIX: Use enumerate(results) to create unique keys
        for i, lead in enumerate(results):
            loc = lead.get('search_location', location) 
            currency_symbol = get_currency_symbol(loc)
            data = normalize_gbp_data(lead)
            audit = calculate_rli_score(data)
            roi = calculate_money_loss(audit['rli_score'], 500, 50) 
            
            # --- CARD UI ---
            with st.container():
                c_info, c_actions = st.columns([3, 2])
                with c_info:
                    st.markdown(f"""
                    <div class="pro-card">
                        <div class="biz-name">{data['name']}</div>
                        <div class="biz-meta">
                            <span class="rating-badge">⭐ {data['rating']} ({data['reviews']})</span>
                            <span>📍 {data['address'][:35]}...</span>
                        </div>
                        <div class="biz-meta">
                            <span class="gap-badge">GAP: {currency_symbol}{roi['monthly_loss_min']:,}/mo</span>
                            <span style="font-family:monospace; font-weight:600;">📞 {lead.get('phone', 'N/A')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_actions:
                    st.write("") # Top alignment
                    b1, b2 = st.columns(2)
                    b3, b4 = st.columns(2)
                    
                    # Unique Keys using index 'i'
                    with b1:
                        if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'], use_container_width=True)
                        else: st.button("No Map", disabled=True, key=f"nm_{i}", use_container_width=True)
                    with b2:
                        if lead.get('website'): st.link_button("🌐 Site", lead['website'], use_container_width=True)
                        else: st.button("No Web", disabled=True, key=f"nw_{i}", use_container_width=True)
                    with b3:
                        if st.button("📥 Track", key=f"add_{i}", use_container_width=True):
                            lead['audit_score'], lead['monthly_gap'], lead['currency'] = audit['rli_score'], roi['monthly_loss_min'], currency_symbol
                            if add_lead(lead): st.toast("Added", icon="✅")
                            else: st.toast("Already Tracking", icon="⚠️")
                    with b4:
                        pdf = create_audit_pdf(data['name'], audit, roi, currency_symbol, data)
                        st.download_button("📄 PDF", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"dl_{i}", use_container_width=True)
            
            st.markdown("---") 

# ==========================================
# 📊 VIEW 3: PIPELINE
# ==========================================
elif selected == "Pipeline":
    val, count = get_metrics()
    st.subheader("Mission Control")
    c1, c2, c3 = st.columns(3)
    c1.metric("Targets", count)
    c2.metric("Pipeline Value", f"${val:,.0f}")
    c3.metric("Status", "Active")
    st.divider()
    
    db = load_db()
    if not db: st.info("Pipeline is empty.")
    else:
        for i, lead in enumerate(db): # Enumerate here too just in case
            sym = lead.get('currency', "$")
            with st.expander(f"{lead['business_name']} | Gap: {sym}{lead.get('monthly_gap', 0):,}"):
                
                c_map, c_web, c_regen = st.columns([1, 1, 2])
                with c_map:
                    if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'])
                with c_web:
                    if lead.get('website'): st.link_button("🌐 Web", lead['website'])
                with c_regen:
                    if st.button("📄 Regenerate Report", key=f"regen_pipe_{i}"):
                        data = normalize_gbp_data(lead)
                        audit = calculate_rli_score(data)
                        roi = calculate_money_loss(audit['rli_score'], 500, 50)
                        pdf = create_audit_pdf(data['name'], audit, roi, sym, data)
                        st.download_button("Download", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"redl_pipe_{i}")
                
                st.divider()
                c1, c2 = st.columns([1, 2])
                with c1:
                    new_st = st.selectbox("Status", ["New Lead", "Outreach", "Negotiation", "Won", "Lost"], index=["New Lead", "Outreach", "Negotiation", "Won", "Lost"].index(lead.get('status', "New Lead")), key=f"st_{i}")
                    if new_st != lead.get('status'): update_lead_status(lead['place_id'], new_st); st.experimental_rerun()
                    if st.button("🗑️ Delete", key=f"del_pipe_{i}"): delete_lead(lead['place_id']); st.experimental_rerun()
                with c2:
                    t1, t2 = st.tabs(["✉️ Email", "📝 Notes"])
                    with t1:
                        kind = st.radio("Template", ["Initial", "Follow Up"], horizontal=True, key=f"r_pipe_{i}")
                        s, b = generate_cold_email(lead, f"T1 ({kind})")
                        st.text_input("Subject", s, key=f"s_pipe_{i}")
                        st.text_area("Body", b, height=150, key=f"b_pipe_{i}")
                    with t2:
                        st.text_area("Notes", lead.get('notes', ''), key=f"n_pipe_{i}")

# ==========================================
# 📈 VIEW 4: ANALYTICS
# ==========================================
elif selected == "Mission Control":
    st.markdown("## Deployment Registry")
    db = load_db()
    if db: st.dataframe(pd.DataFrame(db)[['business_name', 'status', 'monthly_gap']], use_container_width=True)
    else: st.info("No data.")
