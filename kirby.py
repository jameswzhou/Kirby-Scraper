from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import time
from tkinter import messagebox
import pandas as pd
from io import StringIO
import numpy as np

# This is code used to navigate to the previous month, which was used to test if the "O" symbol matched
# WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/div[2]/div[1]/button[1]")))
# lastMonth = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/div[2]/div[1]/button[1]")
# lastMonth.click()


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
while True:
    driver.get("https://kirbycafe-reserve.com/guest/tokyo/reserve/")
    
    # Click the initial OK button on load
    okButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div[2]/button")))
    okButton.click()

    available = False

    while True:
        try:
            expired = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/img")
            if expired:
                print("The page has expired")
                break
            # Wait for the page to load, specifically the selection field for number of people
            # selection = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]")))
            selection = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "v-select__selections")))
            selection.click()

            # Select 2 people
            twoPeople = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div[2]")))
            twoPeople.click()

            # Wait for table to load
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[1]/th")))

            table = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/div[2]/div[2]/table")
            table = pd.read_html(StringIO(driver.page_source))
            df=table[0]

            workingTimes = df.iloc[:,5:9]
            # workingTimes = df

            if '○' in workingTimes.values:
                available = True
                break
            time.sleep(5)
    
        except Exception as e:
            print("An error occured", time.ctime(), e)
    
    if available:
        for i in range(20):
            print("There are available times")
        driver.find_element(By.XPATH, "//*[contains(text(),'○')]").click()    
        messagebox.showinfo("Kirby Cafe", "There are available times")
        break

    


