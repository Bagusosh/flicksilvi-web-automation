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


class OrderTests(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        self.driver = MenuViewDriver().driver

        # data
        fake = Faker('id-ID')

        self.first_category_name = 'Nasi Goreng'
        self.second_category_name = 'Desserts'

        self.valid_first_menu_name = 'Nasi Goreng Ikan Teri Asin'
        self.valid_second_menu_name = 'Singkong Goreng'

        self.valid_new_account_name = fake.first_name()
        self.valid_new_account_phone_number = '08'+fake.aba()
        self.valid_new_account_email = '{name}@mailnesia.com'.format(
            name=self.valid_new_account_name
        )

        self.ep_register = 'https://staging.flick.id/v1/users/auth/verifikasi-token?hp={phonenum}&tipe=registrasi&tipeUser=user'.format(
            phonenum=self.valid_new_account_phone_number
        )

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
        self.order_status_row_xpath = '//*[@id="root"]/div/div/div[1]'

        self.button_add_menu_shopping_cart_xpath = '/html/body/div[2]/div[3]/div/div/button'
        self.button_cart_order_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div[3]/div/span/div'
        self.button_login_xpath = '/html/body/div/div/div/div/div[1]/div[2]/div[1]/button[2]'
        self.button_register_xpath = '//*[@id="root"]/div/div/div/div[1]/div[2]/div[1]/button[1]'
        self.button_login_account_xpath = '//*[@id="root"]/div/div/div/div[1]/form/div[4]/button'
        self.button_continue_register_xpath = '//*[@id="root"]/div/div/div/div[1]/form/div[7]/button'
        self.button_order_and_pay_xpath = '//*[@id="root"]/div/div/div/button/span'
        self.button_save_note_xpath = '/html/body/div[2]/div[3]/div/form/div[3]/button'
        self.button_check_order_status_xpath = '//*[@id="root"]/div/div[1]/div/div[2]/button[1]'
        self.button_check_order_status_navbar_xpath = '//*[@id="root"]/div/div/div[2]/div/button[2]'

        # etc
        self.context = {}

    def test_order_menu_with_flick_pay(self):
        with self.driver as driver:

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.first_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.first_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()
                    break

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.second_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.second_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_second_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cart_order_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_login_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'hp').send_keys('087741331517')

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            data = requests.post('https://staging.flick.id/v1/users/auth/verifikasi-token/login?hp=087741331517&tipeUser=user').json()
            # for make easy to get data from json

            # for key, value in data.items():
            #     print(key, ":", value)
            token = data['data']['token']

            driver.find_element(By.ID, 'otp').send_keys(token)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                return

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # if we use webdriverwait, cant click button payment method
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="Flick Pay"]').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_and_pay_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
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
                logger.error("Order Menu With Flick Pay Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Order Menu With Flick Pay Test Case has been Tested")

    def test_order_menu_with_cash(self):
        with self.driver as driver:

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.first_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.first_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()
                    break

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.second_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.second_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_second_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cart_order_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_login_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'hp').send_keys('087741331517')

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            data = requests.post(
                'https://staging.flick.id/v1/users/auth/verifikasi-token/login?hp=087741331517&tipeUser=user').json()
            token = data['data']['token']

            driver.find_element(By.ID, 'otp').send_keys(token)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
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
                logger.error("Order Menu With Cash Test Case Resulted Error")
                return

            alert = Alert(driver)

            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Order Menu With Cash Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Order Menu With Cash Test Case has been Tested")

    def test_order_menu_with_debit(self):
        with self.driver as driver:

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.first_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.first_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()
                    break

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.second_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.second_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_second_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cart_order_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_login_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'hp').send_keys('087741331517')

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            data = requests.post(
                'https://staging.flick.id/v1/users/auth/verifikasi-token/login?hp=087741331517&tipeUser=user').json()
            token = data['data']['token']

            driver.find_element(By.ID, 'otp').send_keys(token)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # if we use webdriverwait, cant click button payment method
            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="Debit"]').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_order_and_pay_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                return

            alert = Alert(driver)

            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Order Menu With Debit Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Order Menu With Debit Test Case has been Tested")

    def test_order_menu_register_first(self):
        with self.driver as driver:

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.first_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.first_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()
                    break

            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.second_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.second_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_second_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cart_order_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_register_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'nama').send_keys(self.valid_new_account_name)
            driver.find_element(By.ID, 'hp').send_keys(self.valid_new_account_phone_number)
            driver.find_element(By.ID, 'email').send_keys(self.valid_new_account_email)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Register First Case Resulted Error")
                return

            data = requests.post(self.ep_register).json()
            token = data['data']['token']
            # for key, value in data.items():
            #     print(key, ":", value)
            # print(token)
            driver.find_element(By.ID, 'otp').send_keys(token)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'konfirmasiPassword'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_continue_register_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
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
                logger.error("Order Menu Register First Test Case Resulted Error")
                return

            alert = Alert(driver)

            alert.accept()

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                )
                page_exist = True
            except TimeoutException:
                logger.error("Order Menu Register First Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Order Menu Register First Test Case has been Tested")

    def test_order_menu_add_notes(self):
        with self.driver as driver:
            # filter category
            category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
            for row_element in category_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == self.first_category_name:
                    row_element.click()

            # add menu
            menu_row_elements = driver.find_elements(By.XPATH, self.first_menu_row_xpath)
            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                    row_element.find_element(By.TAG_NAME, 'span').click()
                    break

            for row_element in menu_row_elements:
                if row_element.find_element(By.TAG_NAME, 'span').text == 'Catatan':
                    row_element.find_element(By.TAG_NAME, 'button').click()

            driver.find_element(By.XPATH, self.note_field_xpath).send_keys('Pakai cabai 10 biji')

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_save_note_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_cart_order_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                )
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            # if we not use time.sleep, element for button login cant be clicked, because the element has animation
            time.sleep(2)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.button_login_xpath)),
                    EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            driver.find_element(By.ID, 'hp').send_keys('087741331517')

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            data = requests.post('https://staging.flick.id/v1/users/auth/verifikasi-token/login?hp=087741331517&tipeUser=user').json()
            token = data['data']['token']

            driver.find_element(By.ID, 'otp').send_keys(token)

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'password'))
                ).send_keys(150600)
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                return

            try:
                _ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                ).click()
            except TimeoutException:
                logger.error("Order Menu Add Notes Test Case Resulted Error")
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
                logger.error("Order Menu Add Notes Test Case Resulted Error")
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
                logger.error("Order Menu Add Notes Test Case Resulted Error")
                page_exist = False
                return

            assert page_exist is True
            logger.success("Order Menu Add Notes Test Case has been Tested")

    def test_check_order_status_after_ordering(self):
        with self.driver as driver:
            with self.driver as driver:

                # filter category
                category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
                for row_element in category_row_elements:
                    if row_element.find_element(By.TAG_NAME, 'span').text == self.first_category_name:
                        row_element.click()

                # add menu
                menu_row_elements = driver.find_elements(By.XPATH, self.first_menu_row_xpath)
                for row_element in menu_row_elements:
                    if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_first_menu_name:
                        row_element.find_element(By.TAG_NAME, 'span').click()
                        break

                # filter category
                category_row_elements = driver.find_elements(By.XPATH, self.category_row_xpath)
                for row_element in category_row_elements:
                    if row_element.find_element(By.TAG_NAME, 'span').text == self.second_category_name:
                        row_element.click()

                # add menu
                menu_row_elements = driver.find_elements(By.XPATH, self.second_menu_row_xpath)
                for row_element in menu_row_elements:
                    if row_element.find_element(By.TAG_NAME, 'h5').text == self.valid_second_menu_name:
                        row_element.find_element(By.TAG_NAME, 'span').click()

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.button_cart_order_xpath))
                    ).click()
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.text_to_be_present_in_element((By.TAG_NAME, 'h3'), 'Konfirmasi Order')
                    )
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                # if we not use time.sleep, element for button login cant be clicked, because the element has animation
                time.sleep(2)

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.button_login_xpath)),
                        EC.element_to_be_clickable((By.XPATH, self.button_login_xpath))
                    ).click()
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                driver.find_element(By.ID, 'hp').send_keys('087741331517')

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                    ).click()
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                data = requests.post(
                    'https://staging.flick.id/v1/users/auth/verifikasi-token/login?hp=087741331517&tipeUser=user').json()
                token = data['data']['token']

                driver.find_element(By.ID, 'otp').send_keys(token)

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                    ).click()
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, 'password'))
                    ).send_keys(150600)
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.button_login_account_xpath))
                    ).click()
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
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
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    return

                alert = Alert(driver)

                alert.accept()

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.order_success_page_xpath))
                    )
                    page_exist = True
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")
                    page_exist = False
                    return

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.button_check_order_status_xpath))
                    ).click()
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")

                try:
                    _ = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.order_status_row_xpath))
                    )
                except TimeoutException:
                    logger.error("Check Order Status After Ordering Test Case Resulted Error")

                assert page_exist is True
                assert self.order_status_row_xpath in driver.page_source
                logger.success("Order Menu With Cash Test Case has been Tested")

    @classmethod
    def as_suite(cls, test_suite: unittest.TestSuite) -> unittest.TestSuite:
        test_suite.addTest(cls('test_order_menu_register_first'))
        test_suite.addTest(cls('test_order_menu_with_flick_pay'))
        test_suite.addTest(cls('test_order_menu_with_cash'))
        test_suite.addTest(cls('test_order_menu_with_debit'))
        test_suite.addTest(cls('test_order_menu_add_notes'))
        test_suite.addTest(cls('test_check_order_status_after_ordering'))
        return test_suite

    def tearDown(self) -> None:
        pass
