#Links
OTODOM_LINK_RENT_OPTION_ALL = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/{selected_option_city}?limit=24&areaMax={area}&daysSinceCreated={number}&by=DEFAULT&direction=DESC&viewType=listing"
OTODOM_LINK_RENT = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/{selected_option_city}?limit=24&areaMax={area}&daysSinceCreated={number}&extras={option_type}&by=DEFAULT&direction=DESC&viewType=listing"
OTODOM_LINK_SALE = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie{option_market_type}/{selected_option_city}?limit=24&ownerTypeSingleSelect={optiontype}&areaMax={area}&daysSinceCreated={number}&by=DEFAULT&direction=DESC&viewType=listing"
URL_JOIN = 'https://www.otodom.pl'

#Elements
NUM_PAGES_TAG = 'li' 
NUM_PAGES_CLASS = 'css-1tospdx'
LINK_DIV_TAG = 'ul'
LINK_DIV_CLASS = 'css-rqwdxd e127mklk0'
LINK_TAG = 'a'
ADRESS_CLASS = 'eozeyij0 css-1helwne e1p0dzoz0'
PRICE_CLASS = 'css-t3wmkv e9aa0kv0'
CATEGORY_CLASS_TO_SEARCH = 'css-1qzszy5 e26jmad2'

#Folder path otodom
FOLDER_PATH_OTODOM = 'data/otodom'

#Keys to search
KEYS_SALE = [
        'Powierzchnia', 'Forma własności', 'Liczba pokoi', 'Stan wykończenia',
        'Balkon / ogród / taras', 'Piętro', 'Czynsz', 'Miejsce parkingowe', 'Ogrzewanie',
        'Rynek', 'Typ ogłoszeniodawcy', 'Dostępne od', 'Rok budowy', 'Rodzaj zabudowy',
        'Winda', 'Media', 'Zabezpieczenia', 'Informacje dodatkowe',
        'Materiał budynku', 'Wyposażenie', 'Okna', 'Certyfikat energetyczny', 'Obsługa zdalna',
        'Rozpoczęcie budowy', 'Liczba kondygnacji', 'Stan inwestycji', 'Wysokość pomieszczeń',
        'Bezpieczeństwo', 'Udogodnienia', 'Powierzchnie dodatkowe', 'Wysokość pomieszczeń'
        ]

KEYS_RENT = [
        'Powierzchnia', 'Czynsz', 'Liczba pokoi', 'Kaucja', 'Piętro','Miejsce parkingowe', 'Ogrzewanie',
        'Rynek', 'Typ ogłoszeniodawcy','Wyposażenie','Zabezpieczenia', 'Dostępne od', 'Rok budowy',
        'Rodzaj zabudowy','Materiał budynku','Informacje dodatkowe','Rynek','Certyfikat energetyczny',
        'Media','Okna','Wynajmę również studentom','Rozpoczęcie budowy','Liczba kondygnacji',
        'Stan inwestycji', 'Wysokość pomieszczeń','Bezpieczeństwo', 'Udogodnienia', 'Powierzchnie dodatkowe',
        'Wysokość pomieszczeń'
        ]