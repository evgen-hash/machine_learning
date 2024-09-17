
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent
import requests

options = ["--disable-in-process-stack-traces", "--disable-logging","--disable-logging", "--log-level=3", "--output=/dev/null", "--headless", "--no-sandbox", "--disable-dev-shm-usage", "user-agent={}".format(UserAgent.chrome)]

class LikeFilmDbDriver:
  movies_pages = []
  driver = None
  logging = None
  url = ''

  def __init__(self, logging):
    self.logging = logging
    self.create_driver(options)

  def create_driver(self, _options):
    self.options = Options()
    for option in _options:
       self.options.add_argument(option)
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

  def get_html_page(self, url):
    self.driver.get(url)
    html_source = self.driver.page_source
    return html_source

  def get_all_movies(self, url):
    self.logging.info("start get movies from link")
    movies_page = []
    html_source = self.get_html_page(url)
    movies_page.append(html_source)
    self.logging.debug(html_source)
    #parse source and get movies from it and save it into list
    while True:
      try:
        c_elem = self.driver.find_element(By.CLASS_NAME, "uiPaginationListing")
        next_elem = c_elem.find_element("link text", "Вперёд")
        next_elem.click()
        time.sleep(5)
        self.logging.info("next element founded")
        html_source = self.driver.page_source
        self.logging.info("click next and get html page")
        self.logging.debug(html_source)
        movies_page.append(html_source)
        #parse source and get movies from it and save it into list
      except Exception as ex:
        self.logging.exception(ex)
        break
    return movies_page
