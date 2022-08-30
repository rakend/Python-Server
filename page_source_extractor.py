import time

from urllib.parse import urlparse

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

class getPageSource:

    def __init__(self):
        self.delay = 5
        self.timeout = 30
        self.implicit_wait_time = 10
        self.set_chrome_driver()

    def set_chrome_options(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    def set_chrome_driver(self):
        self.set_chrome_options()
        self.chrome_driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        self.chrome_driver.implicitly_wait(self.implicit_wait_time)

    def open_url(self, url):
        self.chrome_driver.set_page_load_timeout(self.timeout)
        self.chrome_driver.get(url)
        time.sleep(self.delay)

    def end_of_page(self):
        self.chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(self.delay)

    def get_html(self):
        html = self.chrome_driver.page_source
        time.sleep(self.delay)
        return html

    def get_url_scheme_and_netlock(self, url):
        url_result = urlparse(url)
        url_scheme = url_result.scheme
        url_netlock = url_result.netloc
        return url_scheme, url_netlock

    def get_html_base_tag(self, url):
        url_scheme, url_netlock = self.get_url_scheme_and_netlock(url)
        html_base_tag = f'<base href="{url_scheme}://{url_netlock}"/>'
        return html_base_tag

    def quit_chrome_driver(self):
        self.chrome_driver.quit()

    def get_page_source(self, url):
        self.open_url(url)
        self.end_of_page()
        page_source = self.get_html()
        html_base_tag = self.get_html_base_tag(url)
        page_source = html_base_tag + page_source
        self.quit_chrome_driver()
        return page_source