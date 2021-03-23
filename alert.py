#cvs-availability-alert

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib

from os import environ

from threading import Timer

FROM_EMAIL = environ['FROM_EMAIL']
FROM_PASS = environ['FROM_PASS']
TO_EMAIL = environ['TO_EMAIL']
INPUT_CITY = environ['INPUT_CITY']

PATH = "C:\\Users\\futur\\Documents\\Github\\covid-availability-alert\\chromedriver"

driver = webdriver.Chrome(PATH)

driver.get('https://www.cvs.com/immunizations/covid-19-vaccine')
print("\n\n" + driver.title + "\n\n")

link = driver.find_element_by_link_text("California")
link.click()

content = "COVID 19 vaccine appointment is now AVAILABLE at " + INPUT_CITY + "!\n\nBook NOW!"
def checkAvail():
    trs = table.find_elements_by_tag_name("tr")
    for tr in trs:
        city = tr.find_element_by_class_name("city")
        if (city.text == INPUT_CITY):
            status = tr.find_element_by_class_name("status")
            print("\n" + city.text + "\nAvailability: " + status.text)
            if (status.text == "Available"):
                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(FROM_EMAIL, FROM_PASS)
                    mail.sendmail(FROM_EMAIL, TO_EMAIL, content)
                    mail.close()
                    print("\n" + INPUT_CITY + " is now Available! Email has been sent!")
                    exit()
            Timer(10, checkAvail).start()

checkVal = 0

try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="vaccineinfo-CA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody'))
    )

    checkAvail()           
except:
    driver.quit()
