import os
import random
import platform
import time
import unittest
import warnings
from loguru import logger
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from faker import Faker
from faker.providers import misc


class MenuViewTests(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        if platform.system() == "Darwin":
            self.driver = webdriver.Safari()
        else:
            self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER"))

        # Data
        fake = Faker()
        fake.add_provider(misc)

        self.menu_url = "https://flicksilvi-webview-develop.netlify.app/webview/menu"
        self.valid_table_id = '0763b36b-a0b1-4f05-bfee-c1126c07a35c'
        self.valid_merchant_name = 'Samsan Tech Restoran!!'
        self.valid_table_number = 1

        self.invalid_table_id = fake.uuid4()

        self.valid_merchant_url = "{base_url}?silvi_table:{id}".format(
            base_url=self.menu_url,
            id=self.valid_table_id
        )

        self.invalid_merchant_url = "{base_url}?silvi_table:{id}".format(
            base_url=self.menu_url,
            id=self.invalid_table_id
        )

        # xPaths
        self.header_text_error_xpath = "//*[@id=\"root\"]/div/div/div/div/div/h2"
        self.merchant_title_xpath = "//*[@id=\"root\"]/div/div/div[2]/div[1]/div[1]/div"
        self.merchant_table_number_xpath = "//*[@id=\"root\"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div/h1"

        # Data
        self.context = {}
        self.header_text_error = "Hmm... keliatannya ada sesuatu di QR-nya"

    def test_invalid_view_menu(self):
        with self.driver as driver:
            driver.maximize_window()

            driver.get(self.invalid_merchant_url)

            try:
                _ = WebDriverWait(driver, 3).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, self.header_text_error_xpath), self.header_text_error
                    )
                )
            except TimeoutException:
                logger.error("Menu Invalid View Test Case resulted Error")
                return

            assert self.header_text_error in driver.page_source
            assert self.valid_merchant_name not in driver.page_source
            logger.success("Menu Invalid View Test Case has been Tested")

    def test_valid_view_menu(self):
        with self.driver as driver:
            driver.maximize_window()

            driver.get(self.valid_merchant_url)

            try:
                _ = WebDriverWait(driver, 3).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, self.merchant_title_xpath), self.valid_merchant_name
                    )
                )
            except TimeoutException:
                logger.error("Menu Valid View Test Case resulted Error")
                return

            merchant_name_text = driver.find_element(By.XPATH, self.merchant_title_xpath).text
            merchant_table_text = driver.find_element(By.XPATH, self.merchant_table_number_xpath).text

            assert merchant_name_text == self.valid_merchant_name
            assert merchant_table_text == str(self.valid_table_number)
            logger.success("Menu Valid View Test Case has been Tested")

    @classmethod
    def as_suite(cls, test_suite: unittest.TestSuite) -> unittest.TestSuite:
        test_suite.addTest(cls("test_invalid_view_menu"))
        test_suite.addTest(cls("test_valid_view_menu"))
        return test_suite

    def tearDown(self) -> None:
        pass


