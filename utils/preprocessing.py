import os
import pandas as pd
import asyncio
from src.otodom_scraper import main_otodom_sale
from src.olx_scraper import main_olx_sale
from config.otodom_config import FOLDER_PATH_OTODOM
from config.olx_config import FOLDER_PATH_OLX
from datetime import datetime

if not os.path.exists(FOLDER_PATH_OTODOM):
    os.makedirs(FOLDER_PATH_OTODOM)

if not os.path.exists(FOLDER_PATH_OLX):
    os.makedirs(FOLDER_PATH_OLX)


def save_data_to_excel(data_list, file_path):
    df = pd.DataFrame(data_list)
    #df.to_excel(file_path, index=False)
    return df

def get_sale_path(folder_path, number, formatted_date):
    return f'{folder_path}//otodom_sale_from_{number}_days_{formatted_date}.xlsx'

def scrap_data_sale_otodom(selected_option_city, number, option_type, option_market_type, area):
    today_date = datetime.today()
    formatted_date = today_date.strftime("%Y-%m-%d-%H-%M")
    PATH_SALE = get_sale_path(FOLDER_PATH_OTODOM, number, formatted_date)
    result_otodom = asyncio.run(main_otodom_sale(selected_option_city, number, option_type, option_market_type, area))
    result_otodom_filtered = [result for result in result_otodom if result is not None]
    if result_otodom_filtered:
        updated_data_list = [{key: value if value is not None and value != '' else 'No data' for key, value in item.items()} for item in result_otodom_filtered]
        df_otodom = save_data_to_excel(updated_data_list, PATH_SALE)
        return df_otodom
    else:
        return None

'''
OLX
'''

def get_sale_path_olx(folder_path,formatted_date):
    return f'{folder_path}//olx_sale_{formatted_date}.xlsx'


def scrap_data_sale_olx(selected_option_city,selected_option_type):
    today_date = datetime.today()
    formatted_date = today_date.strftime("%Y-%m-%d-%H-%M")
    result_olx_sale = asyncio.run(main_olx_sale(selected_option_city,selected_option_type))
    result_olx_sale_filtered = [result for result in result_olx_sale if result is not None]
    if result_olx_sale_filtered:
        updated_data_list = [{key: value if value is not None and value != '' else 'No data' for key, value in item.items()} for item in result_olx_sale_filtered]
        df_olx = save_data_to_excel(updated_data_list,get_sale_path_olx(FOLDER_PATH_OLX,formatted_date))
        return df_olx
    else:
        return None
