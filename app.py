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

# --- SMART CURRENCY LOGIC ---
def get_currency_symbol(location_text):
    """
    Automatically detects currency based on the location string.
    """
    if not location_text: return "$"
    loc = location_text.lower()
    
    # GCC / Middle East
    if any(x in loc for x in ["saudi", "ksa", "riyadh", "dammam", "jeddah", "khobar", "mecca"]): return "SAR"
    if any(x in loc for x in ["uae", "dubai", "abu dhabi", "sharjah"]): return "AED"
    if "qatar" in loc or "doha" in loc: return "QAR"
    if "kuwait" in loc: return "KWD"
    
    # Europe / UK
    if any(x in loc for x in ["uk", "london", "manchester", "birmingham", "england", "scotland", "wales"]): return "£"
    if any(x in loc for x in ["europe", "germany", "france", "italy", "spain", "netherlands", "paris", "berlin"]): return "€"
    
    # Asia
    if any(x in loc for x in ["india", "delhi", "mumbai", "bangalore", "chennai"]): return "₹"
    
    # APAC
    if any(x in loc for x in ["australia", "sydney", "melbourne", "brisbane", "perth"]): return "A$"
    if any(x in loc for x in ["japan", "tokyo", "osaka", "kyoto"]): return "¥"
    
    # Default
    return "$"

# --- CSS INJECTION (UI FIXES) ---
st.markdown("""
<style>
    /* 1. CONTAINER FIX: Prevents stretching on wide monitors */
    .block-container { 
        max_width: 1000px; 
        padding-top: 2rem; 
        padding-bottom: 5rem; 
        margin: auto; 
    }
    
    /* 2. BACKGROUND & FONTS */
    .stApp { background-color: #f4f6f9; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #2c3e50; font-weight: 700; }
    
    /* 3. PRO CARD DESIGN */
    .pro-card {
        background: white;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 10px;
        border-left: 5px solid #4F46E5; /* Brand Stripe */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .pro-card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    .card-title { font-size: 1.1rem; font-weight: 700; color: #111827; margin: 0; }
    .card-meta { font-size: 0.85rem; color: #6B7280; display: flex; align-items: center; gap: 15px; margin-top: 5px; }
    .card-badge { 
        background: #FEF2F2; 
        color: #DC2626; 
        padding: 2px 8px; 
        border-radius: 4px; 
        font-size: 0.75rem; 
        font-weight: 700; 
        border: 1px solid #FECACA;
    }

    /* 4. BUTTON STYLING */
    .stButton>button { border-radius: 6px; font-weight: 600; border: 1px solid #E5E7EB; }
    
    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0 5px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#4F46E5", "color": "white"},
    }
)

# --- VIEW 1: HOME ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; margin-top: 40px;'>Local Intel Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; max-width: 600px; margin: auto;'>Identify high-value local businesses with critical revenue leaks.</p>", unsafe_allow_html=True)
    
    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.info("👈 Select 'Prospector' to start hunting.")

# --- VIEW 2: PROSPECTOR ---
if selected == "Prospector":
    
    # 1. SEARCH INPUTS
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            keyword = st.text_input("Industry", placeholder="e.g. Emergency Plumber")
        with c2:
            location = st.text_input("Region", placeholder="e.g. Los Angeles")
        with c3:
            st.write("") # Spacer
            st.write("") # Spacer
            run_btn = st.button("🚀 DEPLOY SCAN", use_container_width=True)

    # 2. SESSION STATE INIT
    if 'scan_results' not in st.session_state:
        st.session_state['scan_results'] = []

    # 3. RUN LOGIC
    if run_btn and keyword and location:
        with st.spinner("Scanning Market Data..."):
            raw_leads = find_leads(keyword, location)
            
            if not raw_leads:
                st.warning("No leads found matching criteria. Try a broader area.")
            else:
                for lead in raw_leads:
                    lead['search_location'] = location # Save for currency logic
                
                st.session_state['scan_results'] = raw_leads
                save_scan(keyword, location, raw_leads)
                st.toast(f"Acquired {len(raw_leads)} Targets", icon="✅")

    # 4. DISPLAY RESULTS (NEW COMPACT UI)
    results = st.session_state['scan_results']
    
    if results:
        if st.button("Clear Results", key="clear_res"):
            st.session_state['scan_results'] = []
            st.experimental_rerun()
            
        for lead in results:
            # Currency Logic
            loc = lead.get('search_location', location) 
            currency_symbol = get_currency_symbol(loc)

            # Audit Logic
            data = normalize_gbp_data(lead)
            audit = calculate_rli_score(data)
            roi = calculate_money_loss(audit['rli_score'], 500, 50) 
            
            # --- PROFESSIONAL CARD UI ---
            with st.container():
                c_info, c_actions = st.columns([3, 2])
                
                with c_info:
                    # HTML Structure for Card Information
                    st.markdown(f"""
                    <div class="pro-card">
                        <div class="card-title">{data['name']}</div>
                        <div class="card-meta">
                            <span>⭐ {data['rating']} ({data['reviews']})</span>
                            <span>📍 {data['address'][:35]}...</span>
                        </div>
                        <div class="card-meta">
                            <span class="card-badge">GAP: {currency_symbol}{roi['monthly_loss_min']:,}/mo</span>
                            <span>📞 {lead.get('phone', 'N/A')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_actions:
                    # ACTION BUTTONS GRID
                    st.write("") # Top alignment spacer
                    b1, b2 = st.columns(2)
                    b3, b4 = st.columns(2)
                    
                    with b1:
                        if lead.get('maps_url'):
                            st.link_button("📍 Map", lead['maps_url'], use_container_width=True)
                        else:
                            st.button("No Map", disabled=True, key=f"nm_{lead['place_id']}", use_container_width=True)
                    
                    with b2:
                        if lead.get('website'):
                            st.link_button("🌐 Web", lead['website'], use_container_width=True)
                        else:
                            st.button("No Web", disabled=True, key=f"nw_{lead['place_id']}", use_container_width=True)
                            
                    with b3:
                        if st.button("📥 Track", key=f"add_{lead['place_id']}", use_container_width=True):
                            lead['audit_score'] = audit['rli_score']
                            lead['monthly_gap'] = roi['monthly_loss_min']
                            lead['currency'] = currency_symbol
                            if add_lead(lead):
                                st.toast("Added to Pipeline", icon="✅")
                            else:
                                st.toast("Already Tracking", icon="⚠️")
                                
                    with b4:
                        pdf = create_audit_pdf(data['name'], audit, roi, currency_symbol, data)
                        st.download_button("📄 PDF", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"dl_{lead['place_id']}", use_container_width=True)

    # 5. HISTORY
    st.divider()
    with st.expander("📂 Scan History"):
        history = load_history()
        if history:
            for scan in history:
                c_h1, c_h2 = st.columns([4, 1])
                with c_h1:
                    st.write(f"**{scan['keyword']}** - {scan['location']} ({scan['count']} leads) [{scan['timestamp']}]")
                with c_h2:
                    if st.button("Load", key=f"load_{scan['timestamp']}"):
                        st.session_state['scan_results'] = scan['leads']
                        st.experimental_rerun()

# --- VIEW 3: PIPELINE ---
if selected == "Pipeline":
    val, count = get_metrics()
    
    st.subheader("Mission Control")
    m1, m2, m3 = st.columns(3)
    m1.metric("Targets", count)
    m2.metric("Pipeline Value", f"${val:,.0f}")
    m3.metric("Status", "Active")
    
    st.divider()
    
    db = load_db()
    if not db:
        st.info("Pipeline is empty.")
    else:
        for lead in db:
            sym = lead.get('currency', "$")
            
            with st.expander(f"{lead['business_name']} | Gap: {sym}{lead.get('monthly_gap', 0):,}"):
                
                # Action Bar inside Pipeline
                c_map, c_web, c_regen = st.columns([1, 1, 2])
                with c_map:
                    if lead.get('maps_url'): st.link_button("📍 Map", lead['maps_url'])
                with c_web:
                    if lead.get('website'): st.link_button("🌐 Web", lead['website'])
                with c_regen:
                    if st.button("📄 Regenerate PDF", key=f"re_{lead['place_id']}"):
                        data = normalize_gbp_data(lead)
                        audit = calculate_rli_score(data)
                        roi = calculate_money_loss(audit['rli_score'], 500, 50)
                        pdf = create_audit_pdf(data['name'], audit, roi, sym, data)
                        st.download_button("Download Now", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"redl_{lead['place_id']}")

                st.divider()
                
                # CRM Controls
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.caption("Stage")
                    options = ["New Lead", "Outreach Sent", "Negotiation", "Closed Won", "Lost"]
                    curr_idx = options.index(lead.get('status', "New Lead")) if lead.get('status') in options else 0
                    new_st = st.selectbox("Status", options, index=curr_idx, key=f"st_{lead['place_id']}", label_visibility="collapsed")
                    
                    if new_st != lead.get('status'):
                        update_lead_status(lead['place_id'], new_st)
                        st.experimental_rerun()
                        
                    if st.button("🗑️ Delete Lead", key=f"del_{lead['place_id']}"):
                        delete_lead(lead['place_id'])
                        st.experimental_rerun()
                        
                with c2:
                    t1, t2 = st.tabs(["✉️ Email Generator", "📝 Notes"])
                    with t1:
                        kind = st.radio("Template", ["Initial", "Follow Up", "Breakup"], horizontal=True, key=f"r_{lead['place_id']}")
                        s, b = generate_cold_email(lead, f"T1 ({kind})") # Mapping simplified for demo
                        st.text_input("Subject", s, key=f"s_{lead['place_id']}")
                        st.text_area("Body", b, height=150, key=f"b_{lead['place_id']}")
                    with t2:
                        st.text_area("Notes", lead.get('notes', ''), key=f"n_{lead['place_id']}")

# --- VIEW 4: ANALYTICS ---
if selected == "Mission Control":
    st.subheader("Registry")
    db = load_db()
    if db:
        df = pd.DataFrame(db)
        st.dataframe(
            df[['business_name', 'status', 'rating', 'monthly_gap']], 
            use_container_width=True
        )
    else:
        st.info("No data available.")
