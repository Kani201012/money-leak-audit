import streamlit as st
from modules.prospector import get_prospects
from modules.audit_engine import calculate_leakage, calculate_roi_loss
from modules.report_gen import generate_pdf

st.set_page_config(page_title="Money Leak Audit", layout="wide")

st.title("💸 Google Maps Money-Leak Audit")
st.write("Find local businesses losing money due to bad profiles.")

# Sidebar Inputs
with st.sidebar:
    st.header("Settings")
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR"])
    avg_sale = st.number_input("Average Sale Value", value=100)

# Main Inputs
col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input("Business Type (e.g. Dentist)")
with col2:
    location = st.text_input("City")

if st.button("Run Audit"):
    if keyword and location:
        st.write(f"Searching for {keyword} in {location}...")
        
        # 1. Get List
        results = get_prospects(keyword, location)
        
        # 2. Show Results
        for business in results:
            # Calculate Audit
            audit = calculate_leakage(business)
            roi = calculate_roi_loss(audit['score'], avg_sale)
            
            # Display in a Card
            with st.expander(f"{business['business_name']} - Score: {audit['score']}"):
                st.error(f"Leakage Score: {audit['score']}/100")
                st.write(f"Issues: {', '.join(audit['issues'])}")
                st.write(f"Est. Monthly Loss: {currency} {roi['min_revenue_loss']}")
                
                # Generate PDF
                pdf_data = generate_pdf(business['business_name'], audit, roi, currency)
                
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_data,
                    file_name=f"{business['business_name']}_Audit.pdf",
                    mime="application/pdf"
                )
