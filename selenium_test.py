#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


import unittest
import time
import random

class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://demo.opencart.com/")

    def test_scenario(self):
        driver = self.driver

        #change currency ------------------------------------------------------------

        currencyButtonXpath = "//*[@id='currency']/div/button"
        currencyGBPXpath    = "//*[@id='currency']/div/ul/li[2]/button"

        currencyButtonElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(currencyButtonXpath))
        currencyButtonElement.click()

        currencyGBPElement    = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(currencyGBPXpath))
        currencyGBPElement.click()


        #search Ipods ----------------------------------------------------------------

        searchFieldXpath  = "//*[@id='search']/input"
        searchButtonXpath = "//*[@id='search']/span"
        searchValue   = "iPod"

        searchFieldElement =  driver.find_element_by_xpath(searchFieldXpath)
        searchButtonElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(searchButtonXpath))

        searchFieldElement.clear()
        searchFieldElement.send_keys(searchValue)

        searchButtonElement.click()

        #comapre products ----------------------------------------------------------------

        compareButtonXpath = "//*[@data-original-title='Compare this Product']"
        compareButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath(compareButtonXpath))
        for x in range(0,len(compareButtonElement)):
            if compareButtonElement[x].is_displayed():
                compareButtonElement[x].click()

        productCompareButtonId = 'compare-total'
        productCompareButtonElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_id(productCompareButtonId))

        productCompareButtonElement.click()

        #remove not available products---------------------------------------------------

        removeProductButtonXpath = "//*[@class='btn btn-danger btn-block']"
        removeProductButtonElements = WebDriverWait(driver, 5).until(lambda driver: driver.find_elements_by_xpath(removeProductButtonXpath))

        amountOfColumns = len(removeProductButtonElements)
        column = 2
        while column < amountOfColumns+2:
            productAvailabilityXpath = ("//*[@id='content']/table/tbody[1]/tr[6]/td[%s]" %column)
            productAvailabilityElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(productAvailabilityXpath))

            removeProductXpath       = "//*[@id='content']/table/tbody[2]/tr[1]/td[%s]/a" % column
            removeProductElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(removeProductXpath))

            column=column+1

            if productAvailabilityElement.text == 'Out Of Stock':
                removeProductElement.click()
                column=column-1
                amountOfColumns=amountOfColumns-1

        #add random product------------------------------------------------------------

        randomColumn = random.randint(2,amountOfColumns+1)
        priceProductXpath  = "/html/body/div[2]/div/div/table/tbody[1]/tr[3]/td[%s]" %randomColumn
        priceProductElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(priceProductXpath))
        priceProduct = priceProductElement.text
        addProductXpath   = "//*[@id='content']/table/tbody[2]/tr[1]/td[%s]/input" %randomColumn
        addProductElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(addProductXpath))
        addProductElement.click()


        #compare prices----------------------------------------------------------------

        shoppingCartXpath = "/html/body/div[2]/div[1]/a[2]"
        shoppingCartElement = WebDriverWait(driver, 5).until(lambda driver: driver.find_element_by_xpath(shoppingCartXpath))
        shoppingCartElement.click()

        totalPriceXpath = ".//*[@id='content']/div[2]/div/table/tbody/tr[4]/td[2]"
        totalPriceElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(totalPriceXpath))

        self.assertEqual(totalPriceElement.text, priceProduct)

        time.sleep(5)

    def tearDown(self):
        self.driver.quit()

if __name__=='__main__':
    unittest.main()