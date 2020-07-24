from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def scraper(num_apart):
    options = webdriver.ChromeOptions()

    #change the executable_path to corresponding path in your machine
    driver = webdriver.Chrome(executable_path="C:/../../chromedriver_win32/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.etuovi.com/myytavat-asunnot/jyvaskyla?haku=M1520346994'

    driver.get(url)
    apartments = []

    time.sleep(4)

    try:
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/button").click()
    except ElementClickInterceptedException:
        pass

    while len(apartments) < num_apart:


        for apartment_card in driver.find_elements_by_class_name('ListPage__cardContainer__39dKQ'):
            try:
                apart_type = apartment_card.find_element_by_xpath('.//div/div/div[2]/div[1]/div[1]/div/h5').text
            except:
                apart_type = -1
            try:
                location = apartment_card.find_element_by_xpath('.//div/div/div[2]/div[1]/div[1]/div/h4').text
            except:
                location = -1
            try:
                price = apartment_card.find_element_by_xpath('.//div/div/div[2]/div[1]/div[2]/div/div[1]/span').text
            except:
                price = -1
            try:
                size = apartment_card.find_element_by_xpath('.//div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
            except:
                size = -1
            try:
                constr_year = apartment_card.find_element_by_xpath('.//div/div/div[2]/div[1]/div[2]/div/div[3]/span').text
            except:
                rak_vuosi = -1
            print(f"{apart_type} {location}")
            print(len(apartments))

            apartments.append({"Asunnon tyyppi" : apart_type,
                            "Sijanti" : location,
                            "Hinta" : price,
                            "Koko" : size,
                            "Rakennus vuosi" : constr_year})
        try:
            driver.find_element_by_xpath('//*[@id="paginationNext"]').click()
            time.sleep(4)
        except NoSuchElementException:
            print(
                "Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_apart, len(apartments)))
            break
    return pd.DataFrame(apartments)

df = scraper(1900)
df.to_csv('etuovi_asunnot.csv', index=False)