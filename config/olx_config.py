#Links olx
OLX_LINK_RENT_ALL = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{selected_option_city}/?page={page_number}&search%5Border%5D=created_at:desc&search%5Bfilter_float_m:to%5D={selected_area}&view=grid"
OLX_LINK_RENT = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{selected_option_city}/?page={page_number}&search%5Border%5D=created_at:desc&search%5Bfilter_float_m:to%5D={selected_area}&search%{selected_option_type}&view=grid"
OLX_LINK_SALE_ALL = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/{selected_option_city}/?page={page_number}&search%5Bfilter_float_m:to%5D={selected_area}&view=grid"
OLX_LINK_SALE_ALL_CUSTOM = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/{selected_option_city}/?page={page_number}&search%5Bfilter_float_m:to%5D={selected_area}&search%{selected_market_type}&view=grid"
OLX_LINK_SALE = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/{selected_option_city}/?page={page_number}&search%5Bfilter_float_m:to%5D={selected_area}&search%{selected_option_type}&search%{selected_market_type}&view=grid"
OLX_LINK_SALE_MARKET_TYPE_ALL = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/{selected_option_city}/?page={page_number}&search%5Bfilter_float_m:to%5D={selected_area}&search%{selected_option_type}&view=grid"
URL_JOIN = "https://www.olx.pl/"

#Elements olx
NUM_PAGES_TAG = 'a'
NUM_PAGES_CLASS = 'css-1mi714g'
LINK_DIV_TAG = 'div'
LINK_DIV_CLASS = 'css-u2ayx9'
LINK_TAG = 'a'
ADRESS_CLASS = 'css-7dfllt'
PRICE_CLASS = 'css-e2ir3r'
DATE_CLASS = 'css-19yf5ek'
CATEGORY_CLASS_LIST = 'css-px7scb'

#Folder path olx
FOLDER_PATH_OLX = 'data/olx'

KEYS_SALE = ['Cena za m²','Poziom', 'Umeblowane','Rynek','Rodzaj zabudowy', 'Powierzchnia', 'Liczba pokoi']

KEYS_RENT = ['Poziom', 'Umeblowane','Rodzaj zabudowy', 'Powierzchnia', 'Liczba pokoi','Czynsz (dodatkowo)','Czynsz(dodatkowo)']
