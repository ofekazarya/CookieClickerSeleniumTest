from time import sleep
from typing import List
from contextlib import suppress

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException
)


URL = "https://orteil.dashnet.org/cookieclicker/"
Locators = {
    "cookie": (By.ID, "bigCookie"),
    "enabled_product": (By.CSS_SELECTOR, "div.product.enabled"),
    "store_bulk_1": (By.ID, "storeBulk1"),
    "enabled_crate_upgrade": (By.CSS_SELECTOR, "div.crate.upgrade.enabled"),
    "bakery_name": {
        "start_change": (By.ID, "bakeryName"),
        "name_field": (By.ID, "bakeryNameInput"),
        "confirm_change": (By.ID, "promptOption0")
    }
}


class CookieDriverHandler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(URL)

        # Wait until the cookie exists before starting the program
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(Locators["cookie"])
        )
        
        # If selenium starts clicking just as the cookie is available it will sometimes fail.
        # Wait a couple of seconds to avoid it
        sleep(2)

        self.cookie = self.driver.find_element(*Locators["cookie"])

    def __del__(self):
        self.driver.quit()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def click_cookie(self):
        """
        Clicks the big cookie to create more cookies. Ignores
        ElementClickInterceptedException
        """
        try:
            self.cookie.click()
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException ignored, doesn't effects gameplay")
    
    def spend_all_money(self):
        self.buy_upgrades()
        self.buy_buildings()

    def buy_upgrades(self):
        """
        Buys available upgrades from chipest to most expensive
        """
        with suppress(StaleElementReferenceException):
            while upgrade := self.get_enabled_upgrade():
                upgrade.click()

    def get_enabled_upgrade(self) -> WebElement:
        """
        :return (WebElement): The WebElement of the chipest enabled upgrade.
            Returns 'None' if none are enabled.
        """
        try:
            return self.driver.find_element(*Locators["enabled_crate_upgrade"])
        except NoSuchElementException:
            return None
        

    def get_enabled_upgrades(self) -> List[WebElement]:
        """
        :returns (List[WebElement]): A list of all enabled upgrades.
            Returns an empty list if none are enabled.
        """
        return self.driver.find_elements(*Locators["enabled_crate_upgrade"])

    def buy_buildings(self):
        """
        Buys available buildings from most expensive to chipest
        """
        self.driver.find_element(*Locators["store_bulk_1"]).click()
        while products := self.get_enabled_products():
            products[-1].click()
    
    def get_enabled_products(self) -> List[WebElement]:
        """
        :returns (List[WebElements]): A list of all enabled products elements.
            Returns an empty list if none are enabled.
        """
        return self.driver.find_elements(*Locators["enabled_product"])

    def change_bakery_name(self, new_name: str):
        """
        Changes the bakery name to <new_name>

        :param (str) new_name: The new bakery name.
        """
        bakery_name_locators = Locators["bakery_name"]

        # Click the bakery name and start the change proccess
        self.driver.find_element(*bakery_name_locators["start_change"]).click()

        # Send the new name to the input field
        input_field = self.driver.find_element(*bakery_name_locators["name_field"])
        input_field.clear()
        input_field.send_keys(new_name)

        # Confirm name change
        self.driver.find_element(*bakery_name_locators["confirm_change"]).click()
