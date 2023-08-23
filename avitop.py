import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

class AvitoParse:
    def __init__ (self, url:str, items:list,count=5, version_main=None):
        self.url = url
        self.items = items
        self.count = count
        self.version_main = version_main
        
    def __set_up(self):
        self.driver = uc.Chrome(version_main = self.version_main)

    def __get_url(self):
        self.driver.get(self.url)


    def __paginator(self):
        while self.driver.find_element(By.CSS.SELECTOR, "[data-marker='pagination-button/nextPage']")and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS.SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.count -= 1

    def __parse_page(self):
        titles = self.driver.find_element(By.CSS.SELECTOR, "[data-marker='item']")
        for title in titles:
            name = title.find_element(By.CSS.SELECTOR, "[itemprop = 'name']").text
            description = title.find_element(By.CSS.SELECTOR, "[class* = 'styles-module']").text
            url = title.find_element(By.CSS.SELECTOR, "['data-marker=item-title']").get_attribute('href')
            price = title.find_element(By.CSS.SELECTOR, "[itemprop='price']").get_attribute('content')
            print(name, description, url, price)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()

if __name__ =="__main__":
    AvitoParse(url='https://www.avito.ru/moskva/audio_i_video/videokamery-ASgBAgICAUSIAroJ?cd=1&q=gopro+hero'
        count=1,
        )
    
