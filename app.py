import streamlit as st
from prospector.maps_scraper import search_google_maps
from audit.logic import run_money_leak_audit, calculate_roi_impact
from report.generator import generate_consulting_pdf

# --- UI CONFIG ---
st.set_page_config(page_title="Revenue Leak Audit", layout="wide")

# --- HEADER ---
st.title("💸 Google Maps Money-Leak Audit System")
st.markdown("**Purpose:** Identify exactly where this business is losing customers, calls, and revenue.")

# --- SIDEBAR: MONETIZATION SETTINGS ---
with st.sidebar:
    st.header("💰 Audit Calibration")
    currency = st.selectbox("Currency", ["$", "€", "£", "₹", "SAR"])
    avg_sale = st.number_input("Avg. Sale Value", value=500)
    est_leads = st.number_input("Est. Monthly Traffic", value=100)
    st.divider()
    st.info("System Ready: V1.0")

# --- STEP 1: PROSPECTOR ---
st.subheader("1️⃣ Prospector (Find Weak Businesses)")
c1, c2 = st.columns(2)
with c1:
    keyword = st.text_input("Keyword", "Dentist")
with c2:
    location = st.text_input("Location", "Dubai")

if st.button("🔍 Run Prospector"):
    if keyword and location:
        with st.spinner("Harvesting Google Maps Data..."):
            # Call Module 1
            results = search_google_maps(keyword, location)
            st.session_state['results'] = results
            st.success(f"Found {len(results)} Businesses")

# --- STEP 2: LEAD TABLE ---
if 'results' in st.session_state:
    st.divider()
    st.subheader("2️⃣ Lead Selection")
    
    for biz in st.session_state['results']:
        with st.expander(f"{biz['business_name']} (Rating: {biz['rating']} | Reviews: {biz['reviews']})"):
            
            # --- STEP 3: RUN AUDIT ENGINE (HIDDEN LOGIC) ---
            audit = run_money_leak_audit(biz)
            roi = calculate_roi_impact(audit['rli_score'], avg_sale, est_leads)
            
            # Display Summary
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**RLI Score:** {audit['rli_score']}/100")
                if audit['rli_score'] > 50:
                    st.error(f"Status: {audit['leak_level']}")
                else:
                    st.warning(f"Status: {audit['leak_level']}")
            
            with col_b:
                st.metric("Est. Monthly Loss", f"{currency}{roi['monthly_loss_min']:,}")

            # --- STEP 4: GENERATE REPORT ---
            pdf_bytes = generate_consulting_pdf(biz, audit, roi, currency)
            
            st.download_button(
                label=f"📄 Download Audit for {biz['business_name']}",
                data=pdf_bytes,
                file_name=f"{biz['business_name']}_Money_Leak_Audit.pdf",
                mime="application/pdf"
            )
