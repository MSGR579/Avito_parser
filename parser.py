from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from rand_delay import RandDelay
from database import Database

class Parser(RandDelay):
    """
    Класс, в котором реализованы методы для парсинга ссылок на объявления. Реализовано
    При помощи библиотеки для динамического парсинга - Selenium. В отличии от BeautifulSoup,
    Selenim больше подходит для сложных и динамеческих Web-приложений.

    """
    def __init__(self, url_base, req_value):
        self.url_base = url_base
        self.req_value = req_value
        self.url = self.url_base + self.req_value
        self.parsed_links = [] 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.db_manager = Database()
        self.parse_links()



    def parse_links(self):
        page = 1
        while page <= 5:
            # Автоматическое переключение, на заданное програмно число страниц
            self.urlpage = self.url + f"&p={page}"
            self.driver.get(self.urlpage)

            try:
                # Поиск ссылок на объявление по тегу "item-title"
                links_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item-title"]')
                for link_element in links_elements:
                    href = link_element.get_attribute("href") 
                    if href: 
                        self.parsed_links.append(href)

            except Exception as e:
                print(f"Ошибка при парсинге: {e}")



            self.slepper() 
            page += 1

        self.driver.quit()  