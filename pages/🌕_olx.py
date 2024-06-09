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

type_display_city = {
    "krakow": "Kraków",
    "warszawa": "Warszawa",
    "wroclaw": "Wrocław",
    "poznan": "Poznań",
    "rzeszow": "Rzeszów",
    "katowice": "Katowice",
    "lodz": "Łódź"
}
type_display_names = {
    'All': 'All advertisers',
    '5Bprivate_business%5D=business': 'Developers and Real estate offices',
    '5Bprivate_business%5D=private': 'Individuals'
}



type_display_market = {
    'All': 'Primary and secondary market',
    '5Bfilter_enum_market%5D%5B0%5D=primary': 'Primary market',
    '5Bfilter_enum_market%5D%5B0%5D=secondary': 'Secondary market'
}


city_type = st.selectbox("Select city", list(type_display_city.values()), index=0)
option_type = st.selectbox("Select type", list(type_display_names.values()), index=0)
market_type = st.selectbox("Select market type", list(type_display_market.values()), index=0)
selected_area = st.number_input('Select areas in square meters (max 200)', min_value=20, max_value=200, value=100, step=1)
if city_type and option_type:
  selected_option_city = next(key for key, value in type_display_city.items() if value == city_type)
  selected_option_type = next(key for key, value in type_display_names.items() if value == option_type)
  selected_market_type = next(key for key, value in type_display_market.items() if value == market_type)
  if st.button("Start Scraping"):
      with st.spinner("In progress..."):
          df_olx = scrap_data_sale_olx(selected_option_city,selected_option_type,selected_market_type,selected_area)
      if df_olx is not None:
          st.dataframe(df_olx, column_config={"Link": st.column_config.LinkColumn()}, hide_index=False)
      else:
          st.warning("No data available.")

