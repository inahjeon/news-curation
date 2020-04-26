from selenium import webdriver


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    return chrome_driver
