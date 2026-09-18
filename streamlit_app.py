import streamlit as st
import pandas as pd
from tariff_monitor import fetch_federal_register_updates

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

# Filter by product category
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

# Map user-friendly categories to search terms
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
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%B %d, %Y at %I:%M %p')}")
else:
    st.info(f"No recent notices found for **{selected_category}**. Your supply chain in this category is clear of new US trade actions this week.")

st.divider()
st.caption("Data source: Federal Register API (public domain) | Built by Delta Node Advisory, LLC")
