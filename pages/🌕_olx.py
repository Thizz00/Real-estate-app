import streamlit as st
from utils.preprocessing import scrap_data_olx

st.markdown("<h1 style='text-align: center; color: white;'>Scraper Olx</h1>", unsafe_allow_html=True)
st.markdown("""
    <style>
    div.stButton {text-align: center;}
    div.stSpinner > div {
        text-align: center;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

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

offer_type = st.selectbox("Select type", ('Rent', 'Sale'), index=0)

def display_rent_options():
    city = st.selectbox("Select city", list(type_display_city.values()), index=0)
    option = st.selectbox("Select type", list(type_display_names.values()), index=0)
    area = st.number_input('Select area in square meters (max 200)', min_value=20, max_value=200, value=100, step=1)
    return city, option, area

def display_sale_options():
    city = st.selectbox("Select city", list(type_display_city.values()), index=0)
    option = st.selectbox("Select type", list(type_display_names.values()), index=0)
    market = st.selectbox("Select market type", list(type_display_market.values()), index=0)
    area = st.number_input('Select area in square meters (max 200)', min_value=20, max_value=200, value=100, step=1)
    return city, option, market, area

def start_scraping(offer, city, area, option, market=''):
 
    with st.spinner("In progress..."):
        df_olx = scrap_data_olx(offer, city, option, market, area)
    
    if df_olx is not None:
        st.dataframe(df_olx, column_config={"Link": st.column_config.LinkColumn()}, hide_index=False)
    else:
        st.warning("No data available.")

if offer_type == 'Rent':
    city, option, area = display_rent_options()
    if st.button("Start Scraping"):
        if city and option and area:
            city_key = next(key for key, value in type_display_city.items() if value == city)
            option_key = next(key for key, value in type_display_names.items() if value == option)
            start_scraping(offer_type, city_key, area, option_key)
        else:
            st.warning("Fill in all fields.")

if offer_type == 'Sale':
    city, option, market, area = display_sale_options()
    if st.button("Start Scraping"):
        if city and option and market and area:
            city_key = next(key for key, value in type_display_city.items() if value == city)
            option_key = next(key for key, value in type_display_names.items() if value == option)
            market_key = next(key for key, value in type_display_market.items() if value == market)
            start_scraping(offer_type, city_key, area, option_key, market_key)
        else:
            st.warning("Fill in all fields.")
