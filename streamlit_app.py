import streamlit as st

st.set_page_config(
    page_title="Delta Node Advisory",
    page_icon="🇪🇬",
    layout="wide"
)

st.title("🇪🇬 Delta Node Advisory")
st.caption("AI-powered trade compliance intelligence for US importers sourcing from Egypt")

st.divider()

st.header("Welcome")
st.write("""
This dashboard monitors US tariffs, customs regulations, and supplier risk 
for importers bringing goods from Egypt into the United States.

**Current focus areas:**
- Section 301 tariff tracking for Egyptian imports
- Supplier qualification and compliance briefs
- QIZ (Qualifying Industrial Zone) documentation verification
""")

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

st.header("Status")
st.info("🚧 Week 1: Building tariff monitoring prototype. Federal Register integration in progress.")
