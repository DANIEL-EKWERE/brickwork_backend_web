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
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 20)
        driver.implicitly_wait(10)
        html = driver.page_source
        print(f"page source {html}")
        # driver.find_element(By.ID, "frmUsername").send_keys(BRICKLINK_EMAIL)
        # driver.find_element(By.ID, "frmPassword").send_keys(BRICKLINK_PASSWORD)
        # driver.find_element(By.ID, "blbtnLogin").send_keys(Keys.RETURN)
        # username = driver.find_element(By.ID, "username")
        # password = driver.find_element(By.ID, "password")
        # login_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='loginBtn']")

        
        # --- Step 1: Enter username/email ---
        username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username.clear()
        username.send_keys(BRICKLINK_EMAIL)

        # Wait and click the "Continue" button
        continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="loginBtn"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", continue_btn)

        # --- Step 2: Wait for the password field to appear ---
        password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password.clear()
        password.send_keys(BRICKLINK_PASSWORD)

        # --- Step 3: Wait for the *new* button (Sign in) ---
        signin_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="loginBtn"]')))

        # Confirm it's the right one (text says \u201cSign in\u201d)
        if "Sign in" in signin_btn.text:
            driver.execute_script("arguments[0].scrollIntoView(true);", signin_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", signin_btn)
        else:
            print("\u26a0\ufe0f The button didn\u2019t update \u2014 maybe invalid email?")

        print("\u2705 Sign in button clicked successfully")

        delete_login_cookies(COOKIES_FILE_NAME)
        save_login_cookies(driver.get_cookies(), COOKIES_FILE_NAME)
        # driver.add_cookie({"blckSessionStarted":"1"})

        # stay_logged_in = driver.find_element(By.ID, 'frmStayLoggedIn').send_keys

        for link, download_filename in LINKS_TO_DOWNLOAD:
            print("downloader(): Downloading from " + link)
            file: Path = ROOT_DIR / "data" / download_filename
            if file.exists():
                file.unlink()
            print(download_filename)
            # backup_file((ROOT_DIR / "data" / download_filename))
            download_file(driver, link, download_filename)

    except Exception as e:
        print(e)
    finally:
        print("Stopping driver")
        driver.stop_client()
        driver.close()
        driver.quit()
        driver.service.stop()


if __name__ == "__main__":
    print("downloader(): Running downloader manually...")
    main()
    print("downloader(): Finished running downloader manually...")
