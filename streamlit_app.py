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

with st.spinner("Checking the Federal Register..."):
    df = fetch_federal_register_updates()

if not df.empty:
    st.success(f"Found {len(df)} recent trade-related notices. Review the latest actions below.")
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
    st.info("No recent notices found. Your Egypt-sourced supply chain is clear of new US trade actions this week.")

st.caption("Data source: Federal Register API (public domain)")
