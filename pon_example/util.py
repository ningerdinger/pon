import time
import datetime
import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)


def get_data(driver: object) -> list:
    """
    This function gathers all the data that we want to scrape
    after we have accesed the website
    Args:
        driver (object):    the selenium driver to input values

    Returns:
        data_list:  returns a list that contains data to be appended to our main list
    """
    Merk = driver.find_element(
        By.XPATH,
        '//*[@id="Merk"]'
        ).text
    Type = driver.find_element(
        By.XPATH,
        '//*[@id="Type"]'
        ).text
    Variant = driver.find_element(
        By.XPATH,
        '//*[@id="Variant"]'
        ).text
    Typegoedkeuringsnummer = driver.find_element(
        By.XPATH,
        '//*[@id="Typegoedkeuring"]'
        ).text
    driver.find_element(
        By.XPATH,
        '//*[@id="ctl00_MainContent_BasisVervaldata en historie"]/h2/a'
        ).click()
    tenaamstelling_preprocessing = driver.find_element(
        By.XPATH,
        '//*[@id="EersteAfgifteNederland"]'
        ).text
    tenaamstelling = datetime.datetime.strptime(
        tenaamstelling_preprocessing,
        '%d-%m-%Y'
        ).strftime('%Y-%m-%d')
    driver.find_element(
        By.XPATH,
        '//*[@id="ctl00_MainContent_BasisTellerstanden"]/h2/a'
    ).click()
    TellerstandDatum = driver.find_element(
        By.XPATH,
        '//*[@id="TellerstandDatum"]'
        ).text
    TellerstandToelichting = driver.find_element(
        By.XPATH,
        '//*[@id="TellerstandToelichting"]'
        ).text
    driver.find_element(
        By.XPATH,
        '//*[@id="Fiscaal"]'
    ).click()
    BpmBedrag = driver.find_element(
        By.XPATH,
        '//*[@id="BpmBedrag"]'
        ).text.replace("€ ","")
    CatalogusPrijs = driver.find_element(
        By.XPATH,
        '//*[@id="CatalogusPrijs"]'
    ).text.replace("€ ","")
    data_list = [
        Merk, 
        Type, 
        Variant, 
        Typegoedkeuringsnummer, 
        tenaamstelling, 
        TellerstandDatum, 
        TellerstandToelichting, 
        BpmBedrag, 
        CatalogusPrijs
        ]
    return data_list


def scrape_website(driver: object, kentekens: list) -> list:
    """
    This function accesses the main website and gathers all the data
    It will then return everything in a nested list that can be used for our
    pd dataframe
    Args:
        driver (object): the selenium driver required to access the web
        kentekens (list): a list of 'kentekens' that are required
                        to get the data from the correct cars

    Returns:
        dataframe_list: a nested list
    """
    first = True
    dataframe_list = []
    for kenteken in kentekens:
        try:
            if first:
                driver.find_element(
                    By.XPATH, 
                    '/html/body/div/form/div[3]/div[2]/div[1]/div/div[2]/div/div[1]/div/input'
                    ).send_keys(kenteken)
                time.sleep(1)
                driver.find_element(
                    By.XPATH,
                    '/html/body/div/form/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/button'
                    ).click()
                time.sleep(1)
                first = False

                data_list = get_data(driver=driver)
                dataframe_list.append(data_list)

            else:
                driver.find_element(
                    By.XPATH,
                    '/html/body/div/form/div[5]/div[2]/div[1]/div/div[2]/div/div[1]/div/input'
                    ).send_keys(kenteken)
                time.sleep(1)
                driver.find_element(
                    By.XPATH,
                    '/html/body/div/form/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/button'
                    ).click()
                time.sleep(1)

                data_list = get_data(driver=driver)
                dataframe_list.append(data_list)

        except NoSuchElementException:
            logger.warning(
                f"No car found for kenteken: {kenteken}"
                )
            continue
    return dataframe_list
