import os
import random
import platform
import requests
import time
import unittest
import warnings
from loguru import logger
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert

from faker import Faker

from driver.view import MenuViewDriver


class SearchBarTests(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        self.driver = MenuViewDriver().driver

        # data
        fake = Faker('id-ID')

        self.first_category_name = 'Nasi Goreng'
        self.second_category_name = 'Desserts'

        self.valid_first_menu_name = 'Nasi Goreng Ayam'
        self.valid_second_menu_name = 'Singkong Goreng'
        self.invalid_menu_name = fake.user_name()
        self.valid_account_phone_number = '087741331517'

        self.valid_menu_description = 'Nasi Goreng Ayam terbaik di Indonesia'
        self.invalid_menu_description = fake.user_name()

        self.valid_new_account_name = fake.first_name()
        self.valid_new_account_phone_number = '08'+fake.aba()
        self.valid_new_account_email = '{name}@mailnesia.com'.format(
            name=self.valid_new_account_name
        )

        self.ep_register = 'https://staging.flick.id/v1/users/auth/verifikasi-token?hp={phonenum}&tipe=registrasi&tipeUser=user'.format(
            phonenum=self.valid_new_account_phone_number
        )

        self.ep_login = 'https://staging.flick.id/v1/users/auth/verifikasi-token/login?hp={valid_phone_num}&tipeUser=user'.format(
            valid_phone_num=self.valid_account_phone_number
        )

        self.page_text_error = 'Yah, yang kamu cari belum ada'

        # id
        self.valid_first_category_id = 'nasi-goreng'
        self.valid_second_category_id = 'desserts'

        # Xpath
        self.first_menu_row_xpath = '//*[@id="{id_category}"]/div[2]/div'.format(
            id_category=self.valid_first_category_id
        )
        self.second_menu_row_xpath = '//*[@id="{id_category}"]/div[2]/div'.format(
            id_category=self.valid_second_category_id
        )

        self.category_row_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[2]/div[3]/div/button'
        self.modal_menu_detail_xpath = '/html/body/div[2]/div[3]'
        self.payment_method_row_xpath = '//*[@id="root"]/div/div/div/div[4]/div'
        self.order_success_page_xpath = '//*[@id="root"]/div/div[1]/div'
        self.payment_method_list_xpath = '//*[@id="root"]/div/div/div/div[4]'
        self.note_field_xpath = '/html/body/div[2]/div[3]/div/form/div[2]/div/textarea'
        self.search_menu_list_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[2]/div/div/div'
        self.search_menu_field_xpath = '/html/body/div/div/div/div[2]/div[2]/div[1]/header/div[1]/div/div/div/div/div[1]/div/input'
        self.search_bar_menu_row_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[2]/div/div/div/div[1]/div/div/div/div/div'
        self.page_text_error_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[2]/div/div/div/div[1]/div/div/div/div'
        self.search_bar_header_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[1]'

        self.button_add_menu_shopping_cart_xpath = '/html/body/div[2]/div[3]/div/div/button'
        self.button_cart_order_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[3]/div/span/div'
        self.button_login_xpath = '/html/body/div/div/div/div/div[1]/div[2]/div[1]/button[2]'
        self.button_register_xpath = '//*[@id="root"]/div/div/div/div[1]/div[2]/div[1]/button[1]'
        self.button_login_account_xpath = '//*[@id="root"]/div/div/div/div[1]/form/div[4]/button'
        self.button_continue_register_xpath = '//*[@id="root"]/div/div/div/div[1]/form/div[7]/button'
        self.button_order_and_pay_xpath = '//*[@id="root"]/div/div/div/button'
        self.button_save_note_xpath = '/html/body/div[2]/div[3]/div/form/div[3]/button'
        self.button_search_bar_xpath = '//*[@id="root"]/div/div/div[1]/div[2]/div[1]/a/button'
        self.button_order_after_search_menu_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[2]/div/div/div/div[3]/div/span/div'
        self.button_cancelling_search_bar_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/header/div[1]/div/div/div/div/div[2]'
        # etc
        self.context = {}

    def test_ordering_menu_with_search_menu_name(self):
        with self.driver as driver:

            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_first_menu_name)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            menu_row_elements = driver.find_elements(By.XPATH, self.search_bar_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_after_search_menu_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_login_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'hp').send_keys(self.valid_account_phone_number)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            data = requests.post(self.ep_login).json()
            token = data['data']['token']

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'otp'))
                ).send_keys(token)
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # if we use webdriverwait, cant click button payment method
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="Cash"]').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_and_pay_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                return

            # for handle alert prompts
            alert = Alert(driver)
            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Name Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Ordering Menu With Search Menu Name Test Case has been Tested")

    def test_ordering_menu_with_search_menu_description(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_menu_description)

            try:
                _ = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            menu_row_elements = driver.find_element(By.XPATH, self.search_bar_menu_row_xpath)
            for row_element in menu_row_elements.find_elements(By.TAG_NAME, 'span'):
                if row_element.text == 'Tambah':
                    row_element.click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_after_search_menu_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.button_login_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'hp').send_keys(self.valid_account_phone_number)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            data = requests.post(self.ep_login).json()
            token = data['data']['token']

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'otp'))
                ).send_keys(token)
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # if we use webdriverwait, cant click button payment method
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="Cash"]').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_and_pay_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                return

            # for handle alert prompts
            alert = Alert(driver)
            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Ordering Menu With Search Menu Description Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Ordering Menu With Search Menu Description Test Case has been Tested")

    def test_ordering_menu_register_first_with_search_menu_name(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_first_menu_name)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            menu_row_elements = driver.find_elements(By.XPATH, self.search_bar_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_after_search_menu_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_register_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'nama').send_keys(self.valid_new_account_name)
            driver.find_element(By.ID, 'hp').send_keys(self.valid_new_account_phone_number)
            driver.find_element(By.ID, 'email').send_keys(self.valid_new_account_email)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            data = requests.post(self.ep_register).json()
            token = data['data']['token']

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'otp'))
                ).send_keys(token)
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'konfirmasiPassword'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # if we use webdriverwait, cant click button payment method
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="Cash"]').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_and_pay_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                return

            alert = Alert(driver)

            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Ordering Menu Register First With Search Menu Name Test Case Resulted Error")

    def test_ordering_menu_register_first_with_search_menu_description(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_menu_description)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            menu_row_elements = driver.find_element(By.XPATH, self.search_bar_menu_row_xpath)
            for row_element in menu_row_elements.find_elements(By.TAG_NAME, 'span'):
                if row_element.text == 'Tambah':
                    row_element.click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_after_search_menu_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_register_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'nama').send_keys(self.valid_new_account_name)
            driver.find_element(By.ID, 'hp').send_keys(self.valid_new_account_phone_number)
            driver.find_element(By.ID, 'email').send_keys(self.valid_new_account_email)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            data = requests.post(self.ep_register).json()
            token = data['data']['token']

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'otp'))
                ).send_keys(token)
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'konfirmasiPassword'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # if we use webdriverwait, cant click button payment method
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="Cash"]').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_and_pay_xpath))
                ).click()
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                return

            alert = Alert(driver)

            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Ordering Menu Register First With Search Menu Description Test Case Resulted Error")

    def test_search_menu_name_without_ordering(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Search Menu Name Without Ordering Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Search Menu Name Without Ordering Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_first_menu_name)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Search Menu Name Without Ordering Test Case Resulted Error")
                return

            assert self.page_text_error not in driver.page_source
            logger.success("Search Menu Name Without Ordering Test Case has been Tested")

    def test_search_menu_description_without_ordering(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Search Menu Description Without Ordering Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Search Menu Description Without Ordering Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_menu_description)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Search Menu Description Without Ordering Test Case Resulted Error")
                return

            assert self.page_text_error not in driver.page_source
            logger.success("Search Menu Description Without Ordering Test Case has been Tested")

    def test_cancelling_search_menu_name(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Cancelling Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Cancelling Search Menu Name Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_first_menu_name)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Cancelling Search Menu Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cancelling_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Cancelling Search Menu Name Test Case Resulted Error")
                return

            assert self.search_bar_header_xpath not in driver.page_source
            logger.success("Cancelling Search Menu Name Test Case has been Tested")

    def test_cancelling_search_menu_description(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Cancelling Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Cancelling Search Menu Description Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.valid_menu_description)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_bar_menu_row_xpath))
                )
            except TimeoutException:
                logger.error("Cancelling Search Menu Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cancelling_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Cancelling Search Menu Description Test Case Resulted Error")
                return

            assert self.search_bar_header_xpath not in driver.page_source
            logger.success("Cancelling Search Menu Description Test Case has been Tested")

    def test_search_menu_with_invalid_name(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Search Menu With Invalid Name Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Search Menu With Invalid Name Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.invalid_menu_name)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.XPATH, self.page_text_error_xpath), self.page_text_error)
                )
            except TimeoutException:
                logger.error("Search Menu With Invalid Name Test Case Resulted Error")
                return

            assert self.page_text_error in driver.page_source
            assert self.search_bar_menu_row_xpath not in driver.page_source
            logger.success("Search Menu With Invalid Name Test Case has been Tested")

    def test_search_menu_with_invalid_description(self):
        with self.driver as driver:
            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_search_bar_xpath))
                ).click()
            except TimeoutException:
                logger.error("Search Menu With Invalid Description Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, self.search_menu_list_xpath))
                )
            except TimeoutException:
                logger.error("Search Menu With Invalid Description Test Case Resulted Error")
                return

            driver.find_element(By.XPATH, self.search_menu_field_xpath).send_keys(self.invalid_menu_description)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.XPATH, self.page_text_error_xpath), self.page_text_error)
                )
            except TimeoutException:
                logger.error("Search Menu With Invalid Description Test Case Resulted Error")
                return

            assert self.page_text_error in driver.page_source
            assert self.search_bar_menu_row_xpath not in driver.page_source
            logger.success("Search Menu With Invalid Description Test Case has been Tested")

    @classmethod
    def as_suite(cls, test_suite: unittest.TestSuite) -> unittest.TestSuite:
        test_suite.addTest(cls('test_search_menu_name_without_ordering'))
        test_suite.addTest(cls('test_search_menu_description_without_ordering'))
        test_suite.addTest(cls('test_ordering_menu_with_search_menu_name'))
        test_suite.addTest(cls('test_ordering_menu_with_search_menu_description'))
        test_suite.addTest(cls('test_cancelling_search_menu_name'))
        test_suite.addTest(cls('test_cancelling_search_menu_description'))
        test_suite.addTest(cls('test_search_menu_with_invalid_name'))
        test_suite.addTest(cls('test_search_menu_with_invalid_description'))
        return test_suite

    def tearDown(self) -> None:
        pass