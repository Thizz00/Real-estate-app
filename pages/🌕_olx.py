import streamlit as st
from utils.preprocessing import scrap_data_sale_olx

st.markdown("<h1 style='text-align: center; color: white;'>Scraper Otodom</h1>", unsafe_allow_html=True)
st.markdown("""
  <style>
  div.stButton {text-align:center}
  </style>""", unsafe_allow_html=True)

st.markdown("""
  <style>
  div.stSpinner > div {
    text-align:center;
    align-items: center;
    justify-content: center;
  }
  </style>""", unsafe_allow_html=True)

if st.button("Start Scraping"):
    with st.spinner("In progress..."):
        df_olx = scrap_data_sale_olx()
    if df_olx is not None:
        st.dataframe(df_olx, column_config={"Link": st.column_config.LinkColumn()}, hide_index=False)
    else:
        st.warning("No data available.")

