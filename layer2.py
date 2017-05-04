from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


def main():
    browser = webdriver.Firefox(
        executable_path='/Users/dannyshau/code/facebook_crawler/browser_driver/geckodriver'
    )
    browser.maximize_window()
    browser.get(
        'https://www.facebook.com/app_scoped_user_id/1588827478031807/')
    browser.quit()
