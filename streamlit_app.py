import streamlit as st
import pandas as pd
from datetime import datetime
from tariff_monitor import fetch_federal_register_updates
from report_generator import generate_client_report

st.set_page_config(
    page_title="Delta Node Advisory",
    page_icon="🇪🇬",
    layout="wide"
)

st.title("🇪🇬 Delta Node Advisory")
st.caption("AI-powered trade compliance intelligence for US importers sourcing from Egypt")

st.divider()

st.header("Quick Stats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Egypt → US Apparel Exports", value="$1.3B", delta="48.7% of total")
with col2:
    st.metric(label="Section 301 Tariff", value="12.5%", delta="Since July 2026", delta_color="inverse")
with col3:
    st.metric(label="QIZ Minimum Input", value="10%", delta="Israeli content required")

st.divider()

st.header("🇺🇸 Latest US Trade Actions Affecting Egypt")

categories = [
    "All products",
    "Steel & Metals",
    "Textiles & Apparel",
    "Aluminum",
    "Agriculture & Food",
    "Chemicals",
    "Machinery"
]

selected_category = st.selectbox("Filter by product category:", categories)

category_map = {
    "All products": "Egypt tariff trade",
    "Steel & Metals": "Egypt steel",
    "Textiles & Apparel": "Egypt textile",
    "Aluminum": "Egypt aluminum",
    "Agriculture & Food": "Egypt agriculture",
    "Chemicals": "Egypt chemical",
    "Machinery": "Egypt machinery"
}

search_term = category_map[selected_category]

with st.spinner(f"Checking the Federal Register for {selected_category.lower()}..."):
    df = fetch_federal_register_updates(search_term)

if not df.empty:
    st.success(f"Found {len(df)} recent notices for **{selected_category}**.")
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Link": st.column_config.LinkColumn("Read Full Notice", display_text="Open →")
        },
        hide_index=True
    )
    st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

    st.divider()
    st.subheader("📄 Generate Client Report")
    st.write("Create a client-ready PDF compliance brief based on the data above.")

    col_a, col_b = st.columns(2)
    with col_a:
        client_name = st.text_input("Client company name:", placeholder="e.g., Acme Importers LLC")
    with col_b:
        contact_name = st.text_input("Contact person:", placeholder="e.g., John Smith")

    if st.button("Generate PDF Report", type="primary"):
        if not client_name:
            st.warning("Please enter a client company name.")
        else:
            with st.spinner("Building report..."):
                pdf_bytes = generate_client_report(
                    client_name=client_name,
                    contact_name=contact_name or "Client",
                    category=selected_category,
                    df=df
                )
                filename = f"Delta_Node_Brief_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf"
                )
                st.success("Report generated. Click the button above to download.")
else:
    st.info(f"No recent notices found for **{selected_category}**.")

st.divider()
st.caption("Data source: Federal Register API (public domain) | Built by Delta Node Advisory, LLC")
