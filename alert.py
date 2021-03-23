#cvs-availability-alert

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib

inputCity = input("Enter the City you want to check in the correct format (e.g Los Angeles, CA): ")

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get('https://www.cvs.com/immunizations/covid-19-vaccine')
print("\n\n" + driver.title + "\n\n")

link = driver.find_element_by_link_text("California")
link.click()

checkVal = 0

try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="vaccineinfo-CA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody'))
    )

    trs = table.find_elements_by_tag_name("tr")
    
    for tr in trs:
        city = tr.find_element_by_class_name("city")
        if (city.text == inputCity):
            status = tr.find_element_by_class_name("status")
            print("\n" + city.text + "\nAvailability: " + status.text)
            if (status.text == "Fully Booked"):
                print("\n" + inputCity + " is currently fully booked :(")
                inputEmail = input("\n" + "Would you like to receive an email when a spot becomes available? (Y/N): ")
                if (inputEmail == "Y"):

                    content = "Covid vaccine is now AVAILABLE at " + inputCity + "\n\n BOOK NOW!"

                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login('DeveloperMinsoo@gmail.com', 'DeveloperMinsoo123')
                    mail.sendmail('DeveloperMinsoo@gmail.com', 'minsooerickim@gmail.com', content)
                    mail.close()
                else:
                    print("\nThank you for using covid-availability-alert!")
                checkVal = 1
                break
            else:
                print("\n\n" + inputCity + " is currently AVAILBLE, book your appoint now!")
                print("\nThank you for using covid-availability-alert!")
                exit()
                
            
    if (checkVal != 1):
        print(inputCity + " was not found! Please make sure your input was in the right format (e.g Los Angeles, CA)")
        exit()
finally:
    driver.quit()




