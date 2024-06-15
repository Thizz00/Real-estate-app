import streamlit as st
from utils.preprocessing import scrap_data_otodom

st.markdown(
    "<h1 style='text-align: center; color: white;'>Scraper Otodom</h1>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div.stButton {text-align:center}
    div.stSpinner > div {
        text-align: center;
        align-items: center;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

type_display_city = {
    "malopolskie/krakow/krakow/krakow": "Kraków",
    "mazowieckie/warszawa/warszawa/warszawa": "Warszawa",
    "dolnoslaskie/wroclaw/wroclaw/wroclaw": "Wrocław",
    "wielkopolskie/poznan/poznan/poznan": "Poznań",
    "podkarpackie/rzeszow/rzeszow/rzeszow": "Rzeszów",
    "slaskie/katowice/katowice/katowice": "Katowice",
    "lodzkie/lodz/lodz/lodz": "Łódź"
}
type_display_names = {
    'All': 'All advertisers',
    'DEVELOPER': 'Developers',
    'AGENCY': 'Real estate offices',
    'PRIVATE': 'Individuals'
}
type_display_names_rent = {
    'All':'All advertisers',
    '%5BIS_PRIVATE_OWNER%5D':"Individuals"
}

market_type_display_names = {
    '': 'Primary and secondary market',
    ',rynek-pierwotny': 'Primary market',
    ',rynek-wtorny': 'Secondary market'
}

offer_type = st.selectbox("Select type", ('Rent', 'Sale'), index=0)

def display_rent_options():
    city_type = st.selectbox("Select city", list(type_display_city.values()), index=0)
    option_type = st.selectbox("Select type", list(type_display_names_rent.values()), index=0)
    area = st.number_input('Select areas in square meters (max 200)', min_value=20, max_value=200, value=100, step=1)
    number = st.number_input('Insert a number of days to scrap (max 31 days)', min_value=1, max_value=31, value=1, step=1)
    return city_type,option_type ,area, number

def display_sale_options():
    city_type = st.selectbox("Select city", list(type_display_city.values()), index=0)
    option_type = st.selectbox("Select type", list(type_display_names.values()), index=0)
    option_market_type = st.selectbox("Select market type", list(market_type_display_names.values()), index=0)
    area = st.number_input('Select areas in square meters (max 200)', min_value=20, max_value=200, value=100, step=1)
    number = st.number_input('Insert a number of days to scrap (max 31 days)', min_value=1, max_value=31, value=1, step=1)
    return city_type, option_type, option_market_type, area, number

def start_scraping(offer_type, city_type, area, number, option_type, option_market_type=''):
    with st.spinner("In progress..."):
        df_otodom = scrap_data_otodom(offer_type, city_type, number, option_type, option_market_type, area)
    if df_otodom is not None:
        st.dataframe(df_otodom, column_config={"Link": st.column_config.LinkColumn()}, hide_index=False)
    else:
        st.warning("No data available.")

if offer_type == 'Rent':
    city_type,option_type ,area, number = display_rent_options()
    if st.button("Start Scraping"):
        if city_type and option_type and area and number:
            selected_option_city = next(key for key, value in type_display_city.items() if value == city_type)
            selected_option_type_rent = next(key for key, value in type_display_names_rent.items() if value == option_type)
            start_scraping(offer_type, selected_option_city, area, number,selected_option_type_rent)
        else:
            st.warning("Fill in all fields.")
elif offer_type == 'Sale':
    city_type, option_type, option_market_type, area, number = display_sale_options()
    if st.button("Start Scraping"):
        if city_type and option_type and option_market_type and area and number:
            selected_option_city = next(key for key, value in type_display_city.items() if value == city_type)
            selected_option_type = next(key for key, value in type_display_names.items() if value == option_type)
            selected_option_market_type = next(key for key, value in market_type_display_names.items() if value == option_market_type)
            start_scraping(offer_type, city_type, area, number, selected_option_type, selected_option_market_type)
        else:
            st.warning("Fill in all fields.")
