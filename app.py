import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

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
st.set_page_config(page_title="Growth OS Terminal", layout="wide", initial_sidebar_state="collapsed")

def get_currency_symbol(location_text):
    if not location_text: return "$"
    loc = location_text.lower()
    if any(x in loc for x in ["saudi", "ksa", "riyadh", "dammam"]): return "SAR"
    if any(x in loc for x in ["uk", "london"]): return "£"
    if any(x in loc for x in ["india"]): return "₹"
    return "$"

# --- CSS INJECTION (CLEAN CARD UI) ---
st.markdown("""
<style>
    .block-container { max_width: 900px; padding-top: 2rem; margin: auto; }
    .stApp { background-color: #f0f2f6; font-family: 'Inter', sans-serif; }
    
    /* THE CARD */
    .pro-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* HEADER INFO */
    .biz-name { font-size: 1.4rem; font-weight: 800; color: #111827; margin-bottom: 5px; }
    .biz-meta { font-size: 1rem; color: #4B5563; display: flex; gap: 20px; align-items: center; margin-bottom: 15px; }
    
    /* BADGES */
    .rating-badge { background: #FEF3C7; color: #D97706; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
    .gap-badge { background: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .phone-text { font-size: 1.1rem; color: #111827; font-weight: 600; font-family: monospace; }

    /* HIDE DEFAULTS */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Prospector", "Pipeline", "Mission Control"],
    icons=["house", "search", "kanban", "bullseye"],
    menu_icon="cast",
    default_index=1,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "nav-link-selected": {"background-color": "#4F46E5", "color": "white"},
    }
)

# --- VIEW 1: HOME ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; margin-top: 40px;'>Local Intel Engine</h1>", unsafe_allow_html=True)
    st.info("👈 Go to Prospector to find leads.")

# --- VIEW 2: PROSPECTOR ---
if selected == "Prospector":
    
    # INPUTS
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: keyword = st.text_input("Industry", placeholder="e.g. Emergency Plumber")
        with c2: location = st.text_input("Region", placeholder="e.g. Los Angeles")
        with c3:
            st.write("")
            st.write("") 
            run_btn = st.button("🚀 DEPLOY SCAN", use_container_width=True)

    if 'scan_results' not in st.session_state: st.session_state['scan_results'] = []

    if run_btn and keyword and location:
        with st.spinner("Hunting for weak profiles (< 4.2 Stars)..."):
            raw_leads = find_leads(keyword, location)
            if not raw_leads:
                st.warning("No leads found below 4.2 stars. Try a larger city.")
            else:
                for lead in raw_leads: lead['search_location'] = location 
                st.session_state['scan_results'] = raw_leads
                save_scan(keyword, location, raw_leads)
                st.toast(f"Found {len(raw_leads)} Underdogs", icon="✅")

    # DISPLAY RESULTS (NEW UI)
    results = st.session_state['scan_results']
    if results:
        if st.button("Clear Results"): st.session_state['scan_results'] = []; st.experimental_rerun()
            
        for lead in results:
            loc = lead.get('search_location', location)
            currency_symbol = get_currency_symbol(loc)
            data = normalize_gbp_data(lead)
            audit = calculate_rli_score(data)
            roi = calculate_money_loss(audit['rli_score'], 500, 50)
            
            # --- CARD START ---
            with st.container():
                # HTML INFO SECTION
                st.markdown(f"""
                <div class="pro-card">
                    <div class="biz-name">{data['name']}</div>
                    <div class="biz-meta">
                        <span class="rating-badge">⭐ {data['rating']} ({data['reviews']})</span>
                        <span class="gap-badge">REVENUE LEAK: {currency_symbol}{roi['monthly_loss_min']:,}/mo</span>
                    </div>
                    <div class="biz-meta">
                        <span>📍 {data['address'][:45]}...</span>
                        <span class="phone-text">📞 {lead.get('phone', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # BUTTON TOOLBAR (BELOW CARD)
                # We use 4 equal columns for a clean toolbar look
                b1, b2, b3, b4 = st.columns(4)
                
                with b1:
                    if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'], use_container_width=True)
                    else: st.button("No Map", disabled=True, key=f"nm_{lead['place_id']}", use_container_width=True)
                with b2:
                    if lead.get('website'): st.link_button("🌐 Site", lead['website'], use_container_width=True)
                    else: st.button("🚫 No Site", disabled=True, key=f"nw_{lead['place_id']}", use_container_width=True)
                with b3:
                    if st.button("📥 Track", key=f"add_{lead['place_id']}", use_container_width=True):
                        lead['audit_score'], lead['monthly_gap'], lead['currency'] = audit['rli_score'], roi['monthly_loss_min'], currency_symbol
                        if add_lead(lead): st.toast("Added", icon="✅")
                with b4:
                    pdf = create_audit_pdf(data['name'], audit, roi, currency_symbol, data)
                    st.download_button("📄 PDF", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"dl_{lead['place_id']}", use_container_width=True)
            
            st.markdown("---") # Divider between businesses

# --- VIEW 3: PIPELINE ---
if selected == "Pipeline":
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
        for lead in db:
            sym = lead.get('currency', "$")
            with st.expander(f"{lead['business_name']} | {sym}{lead.get('monthly_gap', 0):,}"):
                
                # Action Bar
                c_map, c_web, c_regen = st.columns([1, 1, 2])
                with c_map:
                    if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'])
                with c_web:
                    if lead.get('website'): st.link_button("🌐 Site", lead['website'])
                with c_regen:
                    if st.button("📄 Regenerate Report", key=f"re_{lead['place_id']}"):
                        data = normalize_gbp_data(lead)
                        audit = calculate_rli_score(data)
                        roi = calculate_money_loss(audit['rli_score'], 500, 50)
                        pdf = create_audit_pdf(data['name'], audit, roi, sym, data)
                        st.download_button("Download", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"redl_{lead['place_id']}")
                st.divider()
                
                # Controls
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

# --- VIEW 4: ANALYTICS ---
if selected == "Mission Control":
    st.subheader("Registry")
    db = load_db()
    if db: st.dataframe(pd.DataFrame(db)[['business_name', 'status', 'monthly_gap']], use_container_width=True)
    else: st.info("No data.")
