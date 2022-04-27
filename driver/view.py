import os
import platform
import warnings
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class MenuViewDriver:

    def __init__(self):
        load_dotenv()
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        if platform.system() == "Darwin":
            self.driver = webdriver.Safari()
        else:
            self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER"))

        # Data
        self.menu_url = "https://flicksilvi-webview-develop.netlify.app/webview/menu"
        self.valid_table_id = insert your table id
        self.valid_merchant_name = 'Samsan Tech Restoran!!'
        self.valid_table_number = 1

        self.valid_merchant_url = "{base_url}?silvi_table:{id}".format(
            base_url=self.menu_url,
            id=self.valid_table_id
        )

        # xPaths
        self.header_text_error_xpath = "//*[@id=\"root\"]/div/div/div/div/div/h2"
        self.merchant_title_xpath = "//*[@id=\"root\"]/div/div/div[2]/div[1]/div[1]/div"
        self.merchant_table_number_xpath = "//*[@id=\"root\"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div/h1"

        # Data
        self.context = {}
        self.header_text_error = "Hmm... keliatannya ada sesuatu di QR-nya"

        # Menu View Driver
        self.driver.maximize_window()

        self.driver.get(self.valid_merchant_url)

        try:
            _ = WebDriverWait(self.driver, 3).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, self.merchant_title_xpath), self.valid_merchant_name
                )
            )
        except TimeoutException:
            return
