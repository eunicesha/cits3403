import multiprocessing
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import TestCase

localHost = "http://127.0.0.1:5000/login"

class LoginFormSeleniumTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(localHost)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        # Wait until the login form is loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Find the login elements
        username_element = self.driver.find_element(By.ID, "username")
        password_element = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "submit")

        # Fill in the login form
        username_element.send_keys("tas")
        password_element.send_keys("tas@2024")
        
        # Scroll the submit button into view and ensure it is clickable
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )

        # Submit the form
        try:
            submit_button.click()
        except Exception as e:
            print(f"Click intercepted, retrying with JavaScript click: {e}")
            self.driver.execute_script("arguments[0].click();", submit_button)

        # Wait for the login process to complete
        WebDriverWait(self.driver, 10).until(
            EC.url_changes(localHost)  # Ensure to wait for the URL to change
        )

        # User is redirected to the expected page after login
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:5000/index")

if __name__ == "__main__":
    unittest.main()