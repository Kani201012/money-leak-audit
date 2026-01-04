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
from modules.scan_history import save_scan, load_history  # <--- NEW IMPORT

# --- PAGE CONFIG ---
st.set_page_config(page_title="Growth OS Terminal", layout="wide", initial_sidebar_state="collapsed")

# --- CSS INJECTION (THE "MISSION CONTROL" LOOK) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation Bar */
    .nav-container { background: white; padding: 1rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    
    /* Card Styling */
    .metric-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; border: 1px solid #eee; }
    .lead-card { background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #4F46E5; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    
    /* Typography */
    h1 { color: #111827; font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { color: #374151; }
    
    /* Buttons */
    .stButton>button { border-radius: 8px; font-weight: 600; }
    
    /* Dark Mode Text Area for Emails */
    .stTextArea textarea { background-color: #111827; color: #00ff41; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Prospector", "Pipeline", "Mission Control"],
    icons=["house", "search", "kanban", "bullseye"],
    menu_icon="cast",
    default_index=1, # Defaulting to Prospector for workflow speed
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "10px"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#4F46E5", "color": "white"},
    }
)

# --- VIEW 1: HOME ---
if selected == "Home":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>Discover High-Value Opportunities</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Crawl regional markets and harvest leads with significant competitive gaps.</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=100) # Placeholder logo

# --- VIEW 2: PROSPECTOR (FIXED PERSISTENCE) ---
if selected == "Prospector":
    st.title("🌐 Local Intel Engine")
    
    # 1. SEARCH INPUTS
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        keyword = st.text_input("Industry", placeholder="e.g. Dentists, HVAC")
    with c2:
        location = st.text_input("Region", placeholder="City, State")
    with c3:
        st.write("")
        st.write("")
        run_btn = st.button("🚀 DEPLOY INTEL SCAN", use_container_width=True)

    # 2. INITIALIZE SESSION STATE (MEMORY)
    if 'scan_results' not in st.session_state:
        st.session_state['scan_results'] = []

    # 3. HANDLE SEARCH BUTTON CLICK
    if run_btn and keyword and location:
        with st.spinner("Harvesting Market Data..."):
            # Fetch Data
            raw_leads = find_leads(keyword, location)
            
            if not raw_leads:
                st.warning("No leads found. Check API Key or try a larger city.")
            else:
                # Save to Session State (RAM)
                st.session_state['scan_results'] = raw_leads
                
                # Save to History File (Disk)
                save_scan(keyword, location, raw_leads)
                st.toast(f"Intel Acquired: {len(raw_leads)} Targets Found", icon="✅")

    # 4. DISPLAY RESULTS (PERSISTENT LOOP)
    results = st.session_state['scan_results']
    
    if results:
        # Option to clear results
        if st.button("Clear Results", key="clear_res"):
            st.session_state['scan_results'] = []
            st.experimental_rerun()
            
        for lead in results:
            # Normalize & Audit Logic
            data = normalize_gbp_data(lead)
            audit = calculate_rli_score(data)
            roi = calculate_money_loss(audit['rli_score'], 500, 50) # Avg sale $500, 50 calls
            
            # Display Lead Card
            with st.container():
                st.markdown(f"""
                <div class="lead-card">
                    <h3>{data['name']}</h3>
                    <p>📍 {data['address']} | ⭐ {data['rating']} ({data['reviews']})</p>
                    <p style="color: #D32F2F; font-weight: bold;">MONTHLY GAP: ${roi['monthly_loss_min']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    # Save to Pipeline Button
                    if st.button(f"📥 Add to Pipeline", key=f"add_{lead['place_id']}"):
                        lead['audit_score'] = audit['rli_score']
                        lead['monthly_gap'] = roi['monthly_loss_min']
                        if add_lead(lead):
                            st.toast(f"Target {data['name']} Acquired!", icon="✅")
                        else:
                            st.toast("Target already in pipeline.", icon="⚠️")
                with col_b:
                    # Instant Report Generation
                    pdf = create_audit_pdf(data['name'], audit, roi, "$", data)
                    st.download_button("📄 Download Audit", data=pdf, file_name=f"{data['name']}_Audit.pdf", key=f"dl_{lead['place_id']}")

    # 5. SHOW HISTORY ARCHIVE
    st.divider()
    with st.expander("📂 Scan History (Market Archive)"):
        history = load_history()
        if not history:
            st.write("No previous scans found.")
        else:
            for scan in history:
                col_h1, col_h2 = st.columns([4, 1])
                with col_h1:
                    st.write(f"**{scan['keyword']}** in {scan['location']} ({scan['count']} leads) - {scan['timestamp']}")
                with col_h2:
                    if st.button("Load", key=f"load_{scan['timestamp']}"):
                        st.session_state['scan_results'] = scan['leads']
                        st.experimental_rerun()

# --- VIEW 3: PIPELINE (CRM) ---
if selected == "Pipeline":
    val, count = get_metrics()
    
    # Dashboard Header
    st.markdown("## Mission Control")
    m1, m2, m3 = st.columns(3)
    m1.metric("Active Targets", count)
    m2.metric("Pipeline Potential", f"${val:,.0f}")
    m3.metric("Deployment Phase", "Active")
    
    st.divider()
    
    # Load Data
    db = load_db()
    if not db:
        st.info("Pipeline is empty. Go to Prospector to add targets.")
    else:
        # Pipeline Display
        for lead in db:
            with st.expander(f"{lead['business_name']} | Gap: ${lead.get('monthly_gap', 0):,}", expanded=False):
                
                # Top Row: Metrics
                p1, p2, p3 = st.columns([2,1,1])
                with p1:
                    st.caption("Status")
                    current_status = lead.get('status', "New Lead")
                    options = ["New Lead", "Outreach Sent", "Negotiation", "Closed Won", "Lost"]
                    # Safety check for index
                    try:
                        idx = options.index(current_status)
                    except ValueError:
                        idx = 0
                        
                    new_status = st.selectbox("Current Phase", 
                                            options, 
                                            index=idx,
                                            key=f"status_{lead['place_id']}",
                                            label_visibility="collapsed")
                    
                    if new_status != current_status:
                        update_lead_status(lead['place_id'], new_status)
                        st.experimental_rerun()
                        
                with p2:
                    st.caption("Win Prob.")
                    st.markdown(f"**{lead.get('win_probability', 'Medium')}**")
                with p3:
                    if st.button("🗑️", key=f"del_{lead['place_id']}"):
                        delete_lead(lead['place_id'])
                        st.experimental_rerun()

                # Bottom Row: Action Center
                tab1, tab2 = st.tabs(["📧 Sales Sequence", "✅ Mission Objectives"])
                
                with tab1:
                    # Email Generator
                    email_type = st.radio("Select Template", ["T1 (Initial)", "T2 (Follow Up)", "T3 (Breakup)"], horizontal=True, key=f"rad_{lead['place_id']}")
                    subj, body = generate_cold_email(lead, email_type)
                    
                    st.text_input("Subject", value=subj, key=f"subj_{lead['place_id']}")
                    st.text_area("Email Body", value=body, height=250, key=f"body_{lead['place_id']}")
                    st.caption("Copy this text into your email client.")
                    
                with tab2:
                    st.checkbox("Verify Business Ownership", key=f"c1_{lead['place_id']}")
                    st.checkbox("Draft Personalized Gap Report", key=f"c2_{lead['place_id']}")
                    st.checkbox("Initial Outreach Call", key=f"c3_{lead['place_id']}")
                    st.checkbox("Technical Audit Presentation", key=f"c4_{lead['place_id']}")

# --- VIEW 4: MISSION CONTROL (Analytics) ---
if selected == "Mission Control":
    st.markdown("## Deployment Registry")
    db = load_db()
    if db:
        df = pd.DataFrame(db)
        st.dataframe(
            df[['business_name', 'status', 'rating', 'monthly_gap']], 
            use_container_width=True,
            column_config={
                "monthly_gap": st.column_config.NumberColumn("Revenue Gap", format="$%d")
            }
        )
    else:
        st.info("No data available.")
