import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()


def update_site_dev():
      print("running command")
      cmd = r'C:\Users\colin\\anaconda3\condabin\conda.bat activate squish_site_env &' \
            r'cd C:\Users\colin\PycharmProjects\squish_site &' \
            r'python bulk_update.py '

      os.system(cmd)


def update_site_live():
      driver = webdriver.Chrome('./chromedriver.exe')
      driver.get('https://squishmallow-finder.herokuapp.com/admin/')
      username = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
      username.send_keys(str(os.getenv('USERNAME')))
      password = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
      password.send_keys(str(os.getenv('PASSWORD')))
      click = driver.find_element_by_class_name('submit-row')
      click.click()

      driver.get('https://squishmallow-finder.herokuapp.com/import/')
      element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@name="employeefile"]')))
      element.send_keys("C:/Users/colin/PycharmProjects/checker/sm_checker/items_data/master_upload.xlsx")
      button = driver.find_element_by_tag_name('button')
      button.click()


def upload_images():
      cmd = r'C:\Users\colin\\anaconda3\condabin\conda.bat activate squish_site_env &' \
            r'cd C:\Users\colin\PycharmProjects\squish_site\squishmallow-finder &' \
            r'git add C:\Users\colin\PycharmProjects\squish_site\squishmallow-finder\media\images &' \
            r'git commit -am "Automatic upload, adding images." &' \
            r'git push heroku master'

      os.system(cmd)

