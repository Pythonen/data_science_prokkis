from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def scraper(num_apart):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="C:/Users/Lassi/Downloads/chromedriver_win32/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.etuovi.com/myytavat-asunnot/jyvaskyla?haku=M1520346994'

    driver.get(url)
    asunnot = []

    time.sleep(4)

    try:
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/button").click()
    except ElementClickInterceptedException:
        pass

    while len(asunnot) < num_apart:


        for asunto_kortti in driver.find_elements_by_class_name('ListPage__cardContainer__39dKQ'):
            try:
                asunnon_tyyppi = asunto_kortti.find_element_by_xpath('.//div/div/div[2]/div[1]/div[1]/div/h5').text
            except:
                asunnon_tyyppi = -1
            try:
                sijainti = asunto_kortti.find_element_by_xpath('.//div/div/div[2]/div[1]/div[1]/div/h4').text
            except:
                sijainti = -1
            try:
                hinta = asunto_kortti.find_element_by_xpath('.//div/div/div[2]/div[1]/div[2]/div/div[1]/span').text
            except:
                hinta = -1
            try:
                koko = asunto_kortti.find_element_by_xpath('.//div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
            except:
                koko = -1
            try:
                rak_vuosi = asunto_kortti.find_element_by_xpath('.//div/div/div[2]/div[1]/div[2]/div/div[3]/span').text
            except:
                rak_vuosi = -1
            print(f"{asunnon_tyyppi} {sijainti}")
            print(len(asunnot))

            asunnot.append({"Asunnon tyyppi" : asunnon_tyyppi,
                            "Sijanti" : sijainti,
                            "Hinta" : hinta,
                            "Koko" : koko,
                            "Rakennus vuosi" : rak_vuosi})
        try:
            driver.find_element_by_xpath('//*[@id="paginationNext"]').click()
            time.sleep(4)
        except NoSuchElementException:
            print(
                "Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_apart, len(asunnot)))
            break
    return pd.DataFrame(asunnot)

df = scraper(1900)
df.to_csv('etuovi_asunnot.csv', index=False)