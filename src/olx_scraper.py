import asyncio
import logging
from urllib.parse import urljoin
import re
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from config.main_config import *
from config.olx_config import *

logging.basicConfig(level=logging.INFO, filename=log_file_path, format='%(asctime)s [%(levelname)s]: %(message)s')

semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

async def get_num_pages_sale(selected_option_city,selected_option_type,selected_market_type,selected_area):
    if selected_option_type == 'All' and selected_market_type == 'All':
        link = OLX_LINK_SALE_ALL.format(page_number=2,selected_option_city = selected_option_city,selected_area = selected_area)
    elif selected_option_type == 'All' and selected_market_type != 'All':
        link = OLX_LINK_SALE_ALL_CUSTOM.format(page_number=2,selected_option_city = selected_option_city, selected_market_type = selected_market_type, selected_area = selected_area)
    elif selected_option_type != 'All' and selected_market_type == 'All':
        link = OLX_LINK_SALE_MARKET_TYPE_ALL.format(page_number=2,selected_option_city = selected_option_city,selected_area = selected_area,selected_option_type = selected_option_type)
    else:
        link= OLX_LINK_SALE.format(page_number=2,selected_option_city = selected_option_city,selected_option_type = selected_option_type,selected_market_type = selected_market_type,selected_area = selected_area)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    link,
                    headers=HEADERS,
                    timeout=TIMEOUT,
                ) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        num_pages_element = soup.find_all(NUM_PAGES_TAG, class_=NUM_PAGES_CLASS)[-1]
                        if num_pages_element and num_pages_element.text.isdigit():
                            return int(num_pages_element.text)
                        else:
                            logging.warning("Could not find num_pages on the page or it's not a number")
                            return 1
                    else:
                        logging.warning(f"Failed to fetch {link} - Status code: {response.status}")
                        return 1
    except Exception as e:
        logging.error(f"Error while fetching {link}: {e}")
        return 1

async def parse_links_sale(response):
    soup = BeautifulSoup(await response.text(), 'html.parser')
    divs = soup.find_all(LINK_DIV_TAG, class_=LINK_DIV_CLASS)
    links = set()
    for div in divs:
        anchor_tags = div.find_all(LINK_TAG, href=True)
        for tag in anchor_tags:
            href = tag['href']
            absolute_url = urljoin(OLX_LINK_SALE, href)
            if URL_JOIN in absolute_url:
                links.add(absolute_url)
                logging.info(f"Successfully fetched {absolute_url}")
    return links

async def fetch_links_from_page_sale(page_number,selected_option_city,selected_option_type,selected_market_type,selected_area):

    if selected_option_type == 'All' and selected_market_type == 'All':
        link = OLX_LINK_SALE_ALL.format(page_number=page_number,selected_option_city = selected_option_city,selected_area = selected_area)
    elif selected_option_type == 'All' and selected_market_type != 'All':
        link = OLX_LINK_SALE_ALL_CUSTOM.format(page_number=page_number,selected_option_city = selected_option_city, selected_market_type = selected_market_type,selected_area = selected_area)
    elif selected_option_type != 'All' and selected_market_type == 'All':
        link = OLX_LINK_SALE_MARKET_TYPE_ALL.format(page_number=page_number,selected_option_city = selected_option_city,selected_area = selected_area,selected_option_type = selected_option_type)
    else:
        link = OLX_LINK_SALE.format(page_number=page_number,selected_option_city = selected_option_city,selected_option_type = selected_option_type,selected_market_type = selected_market_type, selected_area = selected_area)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=HEADERS, timeout=TIMEOUT) as response:
                if response.status == 200:
                    return await parse_links_sale(response)
                else:
                    logging.warning(f"Failed to fetch link {link} - Status code: {response.status}")
                    return set()
    except Exception as e:
        logging.error(f"Error while fetching link {link}: {type(e).__name__} - {str(e)}", exc_info=True)
        return set()
    

async def scrap_data_olx_sale(link,semaphore):
    async with semaphore: 
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link, headers=HEADERS) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        address = [i.text.replace(',', '').replace('Strona główna,Nieruchomości,Mieszkania,Wynajem,Wynajem', '').replace(
                                'Wynajem', '').replace('Strona główna,Nieruchomości,Mieszkania,, ', '').replace('-', '').replace('Sprzedaż', '').replace(
                                'Nieruchomości', '').replace('Strona główna', '').replace('Mieszkania', '').replace(',', '').replace(',,,,', '') if i.text != '' else 'No data' for i in soup.find_all(class_=ADRESS_CLASS)]

                        address = ','.join(address[4:7]).replace('  ','')

                        price = ",".join([i.text.replace('do negocjacji',' do negocjacji') if i.text != '' else 'No data' for i in soup.find_all(class_=PRICE_CLASS)])
                        
                        currrent_date = datetime.now().strftime("%d %m %Y")

                        date = ",".join([currrent_date if 'Dzisiaj' in i.text else i.text.replace('stycznia','01').replace('lutego','02').replace('marca','03').replace('kwietnia','04').replace('maja','05').replace('czerwca','06').replace('lipca','07').replace('sierpnia','08').replace('września','09').replace('października','10').replace('listopada','11').replace('grudnia','12') if i.text != '' else 'No data' for i in soup.find_all(class_=DATE_CLASS)])

                        data_dict = {'Link': link, 'Data wystawienia': date,'Adres':address , 'Cena': price}

                        category_text_list = [i.text if i.text != '' else 'No data' for i in soup.find_all(class_=CATEGORY_CLASS_LIST)]

                        keys = ['Cena za m²','Poziom', 'Umeblowane','Rynek','Rodzaj zabudowy', 'Powierzchnia', 'Liczba pokoi']


                        for key in keys:
                            pattern = re.compile(f'{key}:(.+?)(?={ "|".join(map(re.escape, keys[1:])) }|$)')
                            match = pattern.search(category_text_list[0])
                            data_dict[key] = match.group(1).strip() if match else "No data"
                        logging.info(f"Data successfully scraped from link: {link}")
                        return data_dict
                                
                    else:
                        logging.warning(f"Failed to fetch {link} - Status code: {response.status}")

            except Exception as e:
                logging.error(f"Error while scraping data from link {link}: {type(e).__name__} - {str(e)}", exc_info=True)

async def main_olx_sale(selected_option_city,selected_option_type,selected_market_type,selected_area):
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    try:
            num_pages = await get_num_pages_sale(selected_option_city,selected_option_type,selected_market_type,selected_area)
            tasks = [fetch_links_from_page_sale(i,selected_option_city,selected_option_type,selected_market_type,selected_area) for i in range(1, num_pages + 1)]
            results = await asyncio.gather(*tasks)
            scraped_links = set().union(*results)
            logging.info(f"Successfully fetched {len(scraped_links)} URLs")
            results_scrap_data = await asyncio.gather(*[scrap_data_olx_sale(link,semaphore) for link in scraped_links])

            logging.info(f"Scraped: {len(results_scrap_data)} out of: {len(scraped_links)}")
            
            return results_scrap_data
    except Exception as e:
        logging.error(f"Error in main_olx: {type(e).__name__} - {str(e)}", exc_info=True)
        return []

