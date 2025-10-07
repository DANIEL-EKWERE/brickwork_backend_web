# """ Download file """

# import datetime
# import json
# import os
# import time
# from pathlib import Path
# from typing import Any

# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By

# from .constants import BRICKLINK_EMAIL, BRICKLINK_PASSWORD, COOKIES_FILE_NAME, LINKS_TO_DOWNLOAD, LOGIN_URL, ROOT_DIR
# from .driver import configure_driver



# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys


# def get_non_temp_len(download_dir):
#     non_temp_files = [i for i in os.listdir(download_dir) if (i.endswith(".xml"))]
#     print(non_temp_files)
#     return len(non_temp_files)


# def backup_file(file_path: Path):
#     if file_path.exists():
#         backup_file_path = file_path.with_suffix(file_path.suffix + ".bak")
#         if backup_file_path.exists():
#             # Delete the existing backup
#             backup_file_path.unlink()
#         file_path.rename(backup_file_path)
#         print(f"Backup created: {backup_file_path}")
#     else:
#         print("File does not exist, no backup created.")


# def delete_login_cookies(filename: str):
#     if (file := (ROOT_DIR / filename)).exists() and (ROOT_DIR / filename).is_file():
#         file.unlink(missing_ok=True)
#         print("downloader(): ##### Cookies successfully deleted #####")


# def save_login_cookies(cookies: dict[str, Any], filename: str):
#     (ROOT_DIR / filename).write_text(json.dumps(cookies))
#     print("downloader(): ##### Cookies successfully saved #####")


# def get_login_cookies_if_not_expired(filename: str):
#     cookies = []

#     if (ROOT_DIR / filename).exists() and (ROOT_DIR / filename).is_file():
#         expiry = float("inf")

#         cookies = json.loads((ROOT_DIR / filename).read_text())
#         for cookie in cookies:
#             expiry = min(cookie.get("expiry", float("inf")), expiry)

#         if datetime.datetime.fromtimestamp(expiry) < (datetime.datetime.now() + datetime.timedelta(hours=6)):
#             return []
#     return cookies


# def is_file_downloading(filename: str):
#     return (ROOT_DIR / "data" / f"{filename}.crdownload").exists() or (
#         (ROOT_DIR / "data" / filename).exists()
#         and (
#             datetime.datetime.now() - datetime.datetime.fromtimestamp((ROOT_DIR / "data" / filename).stat().st_mtime)
#         ).seconds
#         < 120
#     )


# def is_file_downloaded(filename: str):
#     return (ROOT_DIR / "data" / filename).exists() and (
#         datetime.datetime.now() - datetime.datetime.fromtimestamp((ROOT_DIR / "data" / filename).stat().st_mtime)
#     ).seconds < 120


# def download_file(driver, link, filename):
#     driver.implicitly_wait(5)
#     driver.get(link)
#     while True:
#         if is_file_downloaded(filename):
#             print(f"Downloaded {filename}")
#             break
#         time.sleep(1)

#         if is_file_downloading(filename) is False:
#             print(f"File {filename} is not downloading, retrying...")
#             driver.get(link)
#             time.sleep(1)
#         else:
#             print(f"File {filename} is downloading")


# # def main():
# #     """
# #         TODO:
# #         1. Login into bricklink using headless chrome.
# #         2. Download the following xml files using the direct link below and save in S3 bucket
# #         A (refer to excalidraw diagram)
# #     Note: You would have to login and save your session, use the saved session to query this url
# #     """
# #     driver = configure_driver()

# #     try:
# #         driver.get(LOGIN_URL)
# #         driver.implicitly_wait(10)
# #         driver.find_element(By.ID, "frmUsername").send_keys(BRICKLINK_EMAIL)
# #         driver.find_element(By.ID, "frmPassword").send_keys(BRICKLINK_PASSWORD)
# #         driver.find_element(By.ID, "blbtnLogin").send_keys(Keys.RETURN)
# #         delete_login_cookies(COOKIES_FILE_NAME)
# #         save_login_cookies(driver.get_cookies(), COOKIES_FILE_NAME)
# #         # driver.add_cookie({"blckSessionStarted":"1"})

# #         # stay_logged_in = driver.find_element(By.ID, 'frmStayLoggedIn').send_keys

# #         for link, download_filename in LINKS_TO_DOWNLOAD:
# #             print("downloader(): Downloading from " + link)
# #             file: Path = ROOT_DIR / "data" / download_filename
# #             if file.exists():
# #                 file.unlink()
# #             print(download_filename)
# #             # backup_file((ROOT_DIR / "data" / download_filename))
# #             download_file(driver, link, download_filename)

# #     except Exception as e:
# #         print(e)
# #     finally:
# #         print("Stopping driver")
# #         driver.stop_client()
# #         driver.close()
# #         driver.quit()
# #         driver.service.stop()

# def main():
#     """
#     TODO:
#     1. Login into bricklink using headless chrome.
#     2. Download the following xml files using the direct link below and save in S3 bucket
#     A (refer to excalidraw diagram)
#     """
#     driver = configure_driver()

#     try:
#         driver.get(LOGIN_URL)

#         wait = WebDriverWait(driver, 15)  # up to 15s wait

#         # Wait for username field
#         username_input = wait.until(EC.presence_of_element_located((By.ID, "frmUsername")))
#         username_input.send_keys(BRICKLINK_EMAIL)

#         # Wait for password field
#         print("Waiting for password field...")
#         password_input = wait.until(EC.presence_of_element_located((By.ID, "frmPassword")))
#         print("Filling password field...")
#         password_input.send_keys(BRICKLINK_PASSWORD)

#         # Wait for login button, then press Enter
#         login_button = wait.until(EC.element_to_be_clickable((By.ID, "blbtnLogin")))
#         login_button.send_keys(Keys.RETURN)

#         # save cookies for reuse
#         delete_login_cookies(COOKIES_FILE_NAME)
#         save_login_cookies(driver.get_cookies(), COOKIES_FILE_NAME)

#         # Now process your links
#         for link, download_filename in LINKS_TO_DOWNLOAD:
#             print("downloader(): Downloading from " + link)
#             file: Path = ROOT_DIR / "data" / download_filename
#             if file.exists():
#                 file.unlink()
#             print(download_filename)
#             download_file(driver, link, download_filename)

#     except Exception as e:
#         print("❌ Error:", e)
#     finally:
#         print("Stopping driver")
#         driver.stop_client()
#         driver.close()
#         driver.quit()
#         driver.service.stop()


# if __name__ == "__main__":
#     print("downloader(): Running downloader manually...")
#     main()
#     print("downloader(): Finished running downloader manually...")







""" Download file """






import os
import time
import random
import pickle
import traceback
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException


import datetime
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from pathlib import Path
from typing import Any

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .constants import BRICKLINK_EMAIL, BRICKLINK_PASSWORD, COOKIES_FILE_NAME, LINKS_TO_DOWNLOAD, LOGIN_URL, ROOT_DIR
from .driver import configure_driver


def get_non_temp_len(download_dir):
    non_temp_files = [i for i in os.listdir(download_dir) if (i.endswith(".xml"))]
    print(non_temp_files)
    return len(non_temp_files)


def backup_file(file_path: Path):
    if file_path.exists():
        backup_file_path = file_path.with_suffix(file_path.suffix + ".bak")
        if backup_file_path.exists():
            # Delete the existing backup
            backup_file_path.unlink()
        file_path.rename(backup_file_path)
        print(f"Backup created: {backup_file_path}")
    else:
        print("File does not exist, no backup created.")


def delete_login_cookies(filename: str):
    if (file := (ROOT_DIR / filename)).exists() and (ROOT_DIR / filename).is_file():
        file.unlink(missing_ok=True)
        print("downloader(): ##### Cookies successfully deleted #####")


def save_login_cookies(cookies: dict[str, Any], filename: str):
    (ROOT_DIR / filename).write_text(json.dumps(cookies))
    print("downloader(): ##### Cookies successfully saved #####")


def get_login_cookies_if_not_expired(filename: str):
    cookies = []

    if (ROOT_DIR / filename).exists() and (ROOT_DIR / filename).is_file():
        expiry = float("inf")

        cookies = json.loads((ROOT_DIR / filename).read_text())
        for cookie in cookies:
            expiry = min(cookie.get("expiry", float("inf")), expiry)

        if datetime.datetime.fromtimestamp(expiry) < (datetime.datetime.now() + datetime.timedelta(hours=6)):
            return []
    return cookies


def is_file_downloading(filename: str):
    return (ROOT_DIR / "data" / f"{filename}.crdownload").exists() or (
        (ROOT_DIR / "data" / filename).exists()
        and (
            datetime.datetime.now() - datetime.datetime.fromtimestamp((ROOT_DIR / "data" / filename).stat().st_mtime)
        ).seconds
        < 120
    )


def is_file_downloaded(filename: str):
    return (ROOT_DIR / "data" / filename).exists() and (
        datetime.datetime.now() - datetime.datetime.fromtimestamp((ROOT_DIR / "data" / filename).stat().st_mtime)
    ).seconds < 120


def download_file(driver, link, filename):
    driver.implicitly_wait(5)
    driver.get(link)
    while True:
        if is_file_downloaded(filename):
            print(f"Downloaded {filename}")
            break
        time.sleep(1)

        if is_file_downloading(filename) is False:
            print(f"File {filename} is not downloading, retrying...")
            driver.get(link)
            time.sleep(1)
        else:
            print(f"File {filename} is downloading")


# Typing and sleep tuning
TYPING_MIN_DELAY = 0.03
TYPING_MAX_DELAY = 0.12
STEP_MIN_DELAY = 0.6
STEP_MAX_DELAY = 2.0

# Optional proxy (None to disable)
PROXY = None  # e.g. "http://username:password@1.2.3.4:8000"

# ---------- helpers ----------
def human_sleep(min_delay=STEP_MIN_DELAY, max_delay=STEP_MAX_DELAY):
    time.sleep(random.uniform(min_delay, max_delay))

def human_typing(element, text, min_delay=TYPING_MIN_DELAY, max_delay=TYPING_MAX_DELAY):
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(min_delay, max_delay))

# def save_cookies(driver, path=COOKIES_PATH):
#     with open(path, "wb") as f:
#         pickle.dump(driver.get_cookies(), f)

# def load_cookies(driver, path=COOKIES_PATH):
#     if not os.path.exists(path):
#         return False
#     with open(path, "rb") as f:
#         cookies = pickle.load(f)
#     for c in cookies:
#         # some cookies require domain to be set and expiry cast to int; keep as-is usually works
#         try:
#             driver.add_cookie(c)
#         except Exception:
#             pass
#     return True

def js_stealth(driver):
    # Basic stealth patches (not exhaustive)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        "Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});"
        "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});"
    )


def main():
    """
        TODO:
        1. Login into bricklink using headless chrome.
        2. Download the following xml files using the direct link below and save in S3 bucket
        A (refer to excalidraw diagram)
    Note: You would have to login and save your session, use the saved session to query this url
    """
    driver = configure_driver()

    try:
        print("Launching undetected Chrome...")
        # driver = uc.Chrome(options=options, service=service)
        wait = WebDriverWait(driver, 100)

        # Go to site
        driver.get(LOGIN_URL)
        js_stealth(driver)
        print("Loaded:", driver.title)
        human_sleep(1.0, 2.0)

       
       
        # --- Step 1: Enter username/email ---
        username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username.clear()
        human_typing(username, BRICKLINK_EMAIL)
        print("Entered username")
        human_sleep(0.6, 1.5)

        # Click Continue (first button)
        continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="loginBtn"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        human_sleep(0.3, 0.8)
        driver.execute_script("arguments[0].click();", continue_btn)
        print("Clicked Continue")
        human_sleep(0.8, 1.8)

        # --- Step 2: Enter password when field appears ---
        password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password.clear()
        human_typing(password, BRICKLINK_PASSWORD)
        print("Entered password")
        human_sleep(0.5, 1.2)

        # --- Step 3: Click Sign in (re-find button) ---
        signin_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="loginBtn"]')))
        print("Sign-in button text:", signin_btn.text)
        driver.execute_script("arguments[0].scrollIntoView(true);", signin_btn)
        human_sleep(0.3, 0.8)
        driver.execute_script("arguments[0].click();", signin_btn)
        print("Clicked Sign in")
        human_sleep(2.0, 4.0)

        # After login, save cookies for reuse
        # save cookies for reuse
        delete_login_cookies(COOKIES_FILE_NAME)
        save_login_cookies(driver.get_cookies(), COOKIES_FILE_NAME)

        # Now process your links
        for link, download_filename in LINKS_TO_DOWNLOAD:
            print("downloader(): Downloading from " + link)
            file: Path = ROOT_DIR / "data" / download_filename
            if file.exists():
                file.unlink()
            print(download_filename)
            download_file(driver, link, download_filename)

        

            # ---------- Post-login: check success and proceed ----------
            print("Post-login URL:", driver.current_url)
            # Example: wait for a logged-in-only element or URL change
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "selector_visible_only_when_logged_in")))

            # ... add your scraping/download logic here ...

            human_sleep(0.6, 1.5)
            print("Done. Closing soon.")

    except TimeoutException as e:
        print("Timeout waiting for element:", e)
        traceback.print_exc()

    except WebDriverException as e:
        print("WebDriver error:", e)
        traceback.print_exc()

    except Exception as e:
        print("Unexpected error:", e)
        traceback.print_exc()

    finally:
        print("Closing driver...")
        try:
            if driver:
                print("Stopping driver")
                driver.stop_client()
                driver.close()
                driver.quit()
                driver.service.stop()

        except Exception as e:
            print("Error while closing driver:", e)
    # finally:
    #     print("Stopping driver")
    #     driver.stop_client()
    #     driver.close()
    #     driver.quit()
    #     driver.service.stop()


if __name__ == "__main__":
    print("downloader(): Running downloader manually...")
    main()
    print("downloader(): Finished running downloader manually...")
