from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from constants import ROOT_DIR

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, X-Requested-With",
}


def configure_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # disable sanbox
    options.add_argument("disable-infobars")  # This flag dialog/ information Dialog
    options.add_argument("--disable-dev-shm-usage")  # For linux based machines
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(ROOT_DIR / "data"),
            # 'download.prompt_for_download': False,
            "download.directory_upgrade": True,
            # 'safebrowsing.enabled': False
        },
    )
    # options.add_argument('disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=service, options=options)
    return driver
