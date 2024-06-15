import asyncio
import logging
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from config.main_config import *
from config.otodom_config import *

logging.basicConfig(level=logging.INFO, filename=log_file_path, format='%(asctime)s [%(levelname)s]: %(message)s')

async def parse_link_to_get_num_pages_for_firstsite(offer_type,selected_option_city,option_market_type, option_type, area, number):
    if offer_type == 'Rent':
        if option_type == 'All':
            base_url = f'{OTODOM_LINK_RENT_OPTION_ALL}&page=1'
            formatted_url = base_url.format(
                selected_option_city = selected_option_city, number=number, area=area
            )
        else:
            base_url = f'{OTODOM_LINK_RENT}&page=1'
            formatted_url = base_url.format(
                selected_option_city = selected_option_city, number=number, area=area,option_type = option_type
            )
    elif offer_type == 'Sale':
        base_url = f'{OTODOM_LINK_SALE}&page=1'
        formatted_url = base_url.format(
            selected_option_city = selected_option_city,option_market_type=option_market_type, optiontype=option_type, number=number, area=area
        )
    return formatted_url

async def get_num_pages(offer_type,selected_option_city,option_market_type, option_type, area, number):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                await parse_link_to_get_num_pages_for_firstsite(offer_type,selected_option_city,option_market_type, option_type, area, number),
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
                    logging.warning(f"Failed to fetch {OTODOM_LINK_SALE} - Status code: {response.status}")
                    return 1
    except IndexError:
        logging.error("The list of announcements contains a maximum of 1 page")
        return 1
    except Exception as e:
        logging.error(f"Error while fetching {OTODOM_LINK_SALE}: {type(e).__name__} - {str(e)}", exc_info=True)
        return 1

async def parse_links(response):
    soup = BeautifulSoup(await response.text(), 'html.parser')
    divs = soup.find_all(LINK_DIV_TAG, class_=LINK_DIV_CLASS)
    links = set()
    for div in divs:
        anchor_tags = div.find_all(LINK_TAG, href=True)
        for tag in anchor_tags:
            href = tag['href']
            absolute_url = urljoin(URL_JOIN, href)
            if URL_JOIN + '/pl/oferta/' in absolute_url:
                links.add(absolute_url)
                logging.info(f"Successfully fetched URL {absolute_url}")
    return links

async def fetch_links_from_page(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=HEADERS, timeout=TIMEOUT) as response:
                if response.status == 200:
                    return await parse_links(response)
                else:
                    logging.warning(f"Failed to fetch link {link} - Status code: {response.status}")
                    return set()
    except Exception as e:
        logging.error(f"Error while fetching link {link}: {type(e).__name__} - {str(e)}", exc_info=True)
        return set()

async def fetch_page(offer_type,selected_option_city,page_number, number, option_type, option_market_type, area):
    if offer_type == 'Rent':
        if option_type == 'All':
            base_url = f'{OTODOM_LINK_RENT_OPTION_ALL}&page={page_number}'
            formatted_url = base_url.format(
                selected_option_city = selected_option_city, number=number, area=area
            )
        else:
            base_url = f'{OTODOM_LINK_RENT}&page={page_number}'
            formatted_url = base_url.format(
                selected_option_city = selected_option_city, number=number, area=area,option_type = option_type
            )
    elif offer_type == 'Sale':
        base_url = f'{OTODOM_LINK_SALE}&page={page_number}'
        formatted_url = base_url.format(
            selected_option_city = selected_option_city,optiontype=option_type, number=number, option_market_type=option_market_type, area=area
        )
    return await fetch_links_from_page(formatted_url)

async def scrap_data_otodom(link,semaphore,offer_type):
    async with semaphore: 
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link, headers=HEADERS) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'html.parser')

                        if offer_type == 'Rent':
                            KEYS = KEYS_RENT
                        
                        elif offer_type == 'Sale':
                            KEYS = KEYS_SALE

                        address = ",".join([i.text if i.text else 'No data' for i in soup.find_all(class_=ADRESS_CLASS)])
                        price = ",".join([i.text if i.text else 'No data' for i in soup.find_all(class_=PRICE_CLASS)])

                        category_classes_to_search = [CATEGORY_CLASS_TO_SEARCH]
                        category_text = []
                        for class_name in category_classes_to_search:
                            category = soup.find_all(class_=class_name)
                            category_text.extend([i.text if i.text else 'No data' for i in category])

                        data_dict = {
                            'Link': link,
                            'Adres': address,
                            'Cena': price
                        }

                        data_dict.update({
                            category_text[i]: category_text[i + 1] if category_text[i] in KEYS else "No data"
                            for i in range(0, len(category_text), 2)
                        })

                        missing_keys = [key for key in KEYS if key not in data_dict]
                        for key in missing_keys:
                            data_dict[key] = "No data"


                        if data_dict:
                            logging.info(f"Data successfully scraped from link: {link}")
                            return data_dict
                        else:
                            return None
                    else:
                        logging.warning(f"Failed to fetch {link} - Status code: {response.status}")
            except Exception as e:
                logging.error(f"Error while scraping data from link {link}: {type(e).__name__} - {str(e)}", exc_info=True)

async def main_otodom(offer_type,selected_option_city, number, option_type, option_market_type, area):
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    try:
        num_pages = await get_num_pages(offer_type,selected_option_city, option_market_type, option_type, area, number)
        tasks = [fetch_page(offer_type,selected_option_city, i, number, option_type, option_market_type, area) for i in range(1, num_pages + 1)]
        scraped_links = set().union(*await asyncio.gather(*tasks))
        logging.info(f"Successfully fetched {len(scraped_links)} URLs")
        results_scrape_data = await asyncio.gather(*[scrap_data_otodom(link, semaphore,offer_type) for link in scraped_links])
        logging.info(f"Scraped: {len(results_scrape_data)} out of: {len(scraped_links)}")
        return results_scrape_data
    except Exception as e:
        logging.error(f"Error in main_otodom_rent: {type(e).__name__} - {str(e)}", exc_info=True)
        return []