import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Indian Stock Dashboard",
                   layout="wide")

st.title("Indian Stock Market Dashboard")
st.markdown("---")

st.sidebar.title("Dashboard Controls")
selected_stock = st.sidebar.selectbox(
    "Select Stock",
    ["RELIANCE", "TCS", "INFOSYS", "HDFC", "WIPRO"]
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Selected Stock", selected_stock)
with col2:
    st.metric("Best Performer", "WIPRO +26.79%")
with col3:
    st.metric("Worst Performer", "RELIANCE -5.83%")

st.markdown("---")

df = pd.DataFrame({
    'Stock': ['WIPRO', 'INFY', 'TCS', 'HDFC', 'RELIANCE'],
    'Return': [26.79, 25.02, 9.50, 5.83, -5.83]
})

fig = px.bar(df, x='Stock', y='Return',
             color='Return',
             color_continuous_scale='RdYlGn',
             title='Indian Stocks 2024 Annual Returns')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
if st.checkbox("Show raw data"):
    st.dataframe(df)
