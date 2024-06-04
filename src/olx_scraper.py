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

async def fetch_html(url, session):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching HTML from {url}: {e}")
        return None

async def get_num_pages_sale(session):
    url = OLX_LINK_SALE
    try:
        html = await fetch_html(url, session)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            num_pages_element = soup.find_all(NUM_PAGES_TAG, class_=NUM_PAGES_CLASS)[-1]
            if num_pages_element and num_pages_element.text.isdigit():
                return int(num_pages_element.text)
            else:
                logging.warning("Could not find num_pages on the page or it's not a number")
    except Exception as e:
        logging.error(f"Error while fetching {url}: {e}")
    return 1

async def fetch_links_from_page_sale(session, link):
    try:
        html = await fetch_html(link, session)
        if html:
            return await parse_links_sale(html)
    except Exception as e:
        logging.error(f"Error while fetching link {link}: {e}")
    return set()

async def parse_links_sale(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all(LINK_DIV_TAG, class_=LINK_DIV_CLASS)
    links = set()
    for div in divs:
        anchor_tags = div.find_all(LINK_TAG, href=True)
        for tag in anchor_tags:
            href = tag['href']
            absolute_url = urljoin(OLX_LINK_SALE, href)
            if URL_JOIN in absolute_url:
                links.add(absolute_url)
                logging.info(f"Successfully fetched URL {absolute_url}")
    return links

async def fetch_page_sale(session, page_number):
    link = OLX_LINK_SALE.format(page_number=page_number)
    return await fetch_links_from_page_sale(session, link)

async def scrap_data_olx_sale(link):
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

async def main_olx_sale():
    results_scrape_data = []
    try:
        async with aiohttp.ClientSession() as session:

            num_pages = await get_num_pages_sale(session)
            tasks = [fetch_page_sale(session, i) for i in range(1, num_pages + 1)]
            results = await asyncio.gather(*tasks)

            scraped_links = set().union(*results)
            logging.info(f"Successfully fetched {len(scraped_links)} URLs")
            for link in scraped_links:
                result = await scrap_data_olx_sale(link)
                if result:
                    results_scrape_data.append(result)

            logging.info(f"Scraped: {len(results_scrape_data)} out of: {len(scraped_links)}")
            
            return results_scrape_data
    except Exception as e:
        logging.error(f"Error in main_olx: {type(e).__name__} - {str(e)}", exc_info=True)
        return []
