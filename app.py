import streamlit as st
from prospector.maps_scraper import find_leads
from harvester.gbp_data import normalize_gbp_data
from audit.leakage_index import calculate_rli_score
from audit.roi_calculator import calculate_money_loss
from report.pdf_generator import create_audit_pdf

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Google Maps Money-Leak Audit", layout="wide")

st.title("💸 Google Maps Money-Leak Audit System")
st.markdown("### Identify exactly where business is losing customers, calls, and revenue.")

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header("⚙️ Audit Parameters")
    currency = st.selectbox("Currency", ["$", "₹", "€", "£", "SAR"])
    avg_sale = st.number_input("Average Sale Value", min_value=10, value=500)
    est_calls = st.number_input("Est. Monthly Call Volume", min_value=10, value=100)

# --- MODULE 1: PROSPECTOR ---
col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input("Business Keyword (e.g. Plumber)")
with col2:
    location = st.text_input("Location (e.g. Dammam)")

if st.button("🚀 Run Prospector & Audit"):
    if keyword and location:
        with st.spinner("Prospecting and Analyzing..."):
            
            # 1. FIND LEADS (Module 1)
            raw_leads = find_leads(keyword, location)
            
            st.write(f"Found {len(raw_leads)} potential businesses.")
            st.divider()

            for lead in raw_leads:
                # 2. HARVEST & NORMALIZE (Module 2)
                clean_data = normalize_gbp_data(lead)
                
                # 3. AUDIT ENGINE (Module 3)
                audit_result = calculate_rli_score(clean_data)
                
                # 4. ROI CALCULATOR (Module 4)
                roi_result = calculate_money_loss(audit_result['rli_score'], avg_sale, est_calls)

                # DISPLAY CARD
                with st.expander(f"{clean_data['name']} (Score: {audit_result['rli_score']}/100)"):
                    c1, c2, c3 = st.columns([1, 2, 1])
                    
                    with c1:
                        if audit_result['rli_score'] > 50:
                            st.error(f"RLI: {audit_result['rli_score']}")
                        else:
                            st.warning(f"RLI: {audit_result['rli_score']}")
                            
                    with c2:
                        st.write(f"**Status:** {audit_result['leak_level']}")
                        st.write(f"**Est. Annual Loss:** {currency}{roi_result['annual_loss']:,}")
                        st.caption(f"Issues: {len(audit_result['issues'])} detected")
                    
                    with c3:
                        # 5. GENERATE PDF (Module 5)
                        pdf_data = create_audit_pdf(clean_data['name'], audit_result, roi_result, currency)
                        
                        st.download_button(
                            label="📥 Download Audit PDF",
                            data=pdf_data,
                            file_name=f"{clean_data['name']}_Audit.pdf",
                            mime="application/pdf"
                        )
