import streamlit as st

st.set_page_config(
    page_title="Real estate scraper",
    page_icon="👋",
    layout="centered",
)


st.title("Choose what you want to do? 🏠")

st.page_link("pages/🌑_otodom.py", label="Scrap only data from Otodom 🏡", icon="1️⃣")
st.page_link("pages/🌕_olx.py", label="Scrap only data from Olx 🏢", icon="2️⃣")

