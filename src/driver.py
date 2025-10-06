# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# from .constants import ROOT_DIR

# headers = {
#     "Access-Control-Allow-Origin": "*",
#     "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
#     "Access-Control-Allow-Headers": "Content-Type, Accept, X-Requested-With",
# }


# def configure_driver():
#     service = Service(ChromeDriverManager().install())

#     # service = Service(ChromeDriverManager(driver_version="129.0.6668.89").install())
    
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")  # disable sanbox
#     options.add_argument("disable-infobars")  # This flag dialog/ information Dialog
#     options.add_argument("--disable-dev-shm-usage")  # For linux based machines
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-extensions")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
#     options.add_experimental_option(
#         "prefs",
#         {
#             "download.default_directory": str(ROOT_DIR / "data"),
#             # 'download.prompt_for_download': False,
#             "download.directory_upgrade": True,
#             # 'safebrowsing.enabled': False
#         },
#     )
#     # options.add_argument('disable-blink-features=AutomationControlled')
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .constants import ROOT_DIR

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, X-Requested-With",
}

def configure_driver():
    # Always grabs the correct driver for the installed Chrome version
    # service = Service(ChromeDriverManager().install())
    # If you ever want to lock it to Chrome 129 explicitly:
    service = Service(ChromeDriverManager(driver_version="141.0.7390.54").install())
    # service = Service("/usr/local/bin/chromedriver")

    options = Options()
    options.add_argument("--headless=new")  # use modern headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.page_load_timeout = 300  # 5 minutes
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(ROOT_DIR / "data"),
            "download.directory_upgrade": True,
        },
    )

    driver = webdriver.Chrome(service=service, options=options)
    return driver
