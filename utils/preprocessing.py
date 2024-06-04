import os
import pandas as pd
import asyncio
from src.otodom_scraper import main_otodom_sale
from config.otodom_config import FOLDER_PATH_OTODOM
from datetime import datetime

FOLDER_PATH_OTODOM = "ścieżka/do/folderu"

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_data_to_excel(data_list, file_path):
    df = pd.DataFrame(data_list)
    df.to_excel(file_path, index=False)
    return df

def get_sale_path(folder_path, number, formatted_date):
    return f'{folder_path}//otodom_sale_from_{number}_days_{formatted_date}.xlsx'

def scrap_data_sale_otodom(selected_option_city, number, option_type, option_market_type, area):
    today_date = datetime.today()
    formatted_date = today_date.strftime("%Y-%m-%d-%H-%M")
    create_folder_if_not_exists(FOLDER_PATH_OTODOM)
    PATH_SALE = get_sale_path(FOLDER_PATH_OTODOM, number, formatted_date)
    result_otodom = asyncio.run(main_otodom_sale(selected_option_city, number, option_type, option_market_type, area))
    result_otodom_filtered = [result for result in result_otodom if result is not None]
    if result_otodom_filtered:
        updated_data_list = [{key: value if value is not None and value != '' else 'No data' for key, value in item.items()} for item in result_otodom_filtered]
        df_otodom = save_data_to_excel(updated_data_list, PATH_SALE)
        return df_otodom
    else:
        return None
