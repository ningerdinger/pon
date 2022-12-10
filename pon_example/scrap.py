from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

import pandas as pd
from .util import scrape_website


logger = logging.getLogger(__name__)


def web_scrap(kentekens: list, path: str) -> pd.DataFrame:
    """
    The main scrapper to retrieve car details
    based on 'kentekens'
    Args:
            kentekens (list): list of kentekens where details need to be retrieved
            path (str): the path to your chromedriver.exe

    Returns:
            df: a pandas dataframe
    """
    options = Options()
    options.add_argument("--headless")
    # options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    url = "https://ovi.rdw.nl/"
    driver.get(url)
    dataframe_list = scrape_website(driver=driver, kentekens=kentekens)

    columns_data = [
            "Merk",
            "Type",
            "Variant",
            "Typegoedkeuringsnummer",
            "Eerste tenaamstelling",
            "Jaar laatste registratie",
            "toelichting",
            "Bruto BPM",
            "Catalogusprijs",
            ]

    df = pd.DataFrame(data=dataframe_list, columns=columns_data)

    return df
