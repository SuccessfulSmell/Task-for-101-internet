# -- coding: utf-8 --
import datetime
import unittest
from selenium import webdriver


class AmazonTestCase(unittest.TestCase):
    def setUp(self):
        '''
        SetUp method to open https://www.amazon.com.au/
        :return:
        '''
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.amazon.com.au/")

    def all_links_pass(self):
        '''
        Method that follows the links from the task.
        Pet supplies -> Cats -> Clothing
        '''
        browser = self.browser
        browser.find_elements_by_css_selector(".gw-icon.feed-arrow")[1].click()
        browser.find_elements_by_class_name("a-list-item")[8].click()
        browser.find_element_by_link_text("CATS").click()
        browser.find_element_by_link_text("Clothing").click()
        browser.find_element_by_class_name("a-link-normal").click()

    def date_chech(self, date_first_available, day, month):
        '''
        Method that compares date and month
        :param date_first_available: day, month and year for
        :param day, month:
        :return: 0 or 1 depending on pass checks
        '''
        month_dict = {"January": 1, "Febuary": 2, "March": 3, "April": 4,
                      "May": 5, "June": 6, "July": 7, "August": 8,
                      "September": 9, "October": 10, "November": 11, "December": 12}
        av_month = month_dict[date_first_available[1]]
        if av_month < month:
            return 0
        else:
            if av_month == month and \
                    date_first_available[0] <= day:
                return 0
            else:
                return 1

    def test_asin_in_page(self):
        '''
        Check 'ASIN' word in page source
        '''
        self.all_links_pass()
        assert "ASIN" in self.browser.page_source

    def test_text_in_title(self):
        '''
        Check title in tag
        '''
        self.all_links_pass()
        text = self.browser.find_element_by_id("productTitle").text
        if len(text) > 0:
            result = 0
        self.assertEqual(result, 0)

    def test_available_date(self):
        '''
        Check validation of date
        '''
        self.all_links_pass()
        text = str(self.browser.page_source)
        start = "Date first available at Amazon.com.au:</b> "
        end = "</li>"
        date_first_available = ((text.split(start))[1].split(end)[0]).split()
        date = datetime.date.today()
        if int(date_first_available[2]) < date.year:
            result = 0
        else:
            result = self.date_chech(date_first_available, date.day, date.month)
        self.assertEqual(result, 0)

    def tearDown(self):
        '''
        Browser close
        '''
        self.browser.close()
        self.browser.quit()


if __name__ == '__main__':
    unittest.main()
