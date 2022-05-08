import time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from chromeDriver.auth_data import email, password
from params import URL, DRIVER_PATH


URL_PARSE = f"https://www.linkedin.com/search/results/people/?keywords=it%20recruiter%2F%20it%20acquisition%20specialist&origin=CLUSTER_EXPANSION&page=1&sid=zZd"


def register(driver) -> None:
    email_input = driver.find_element(by=By.ID, value="username")
    email_input.clear()
    email_input.send_keys(email)

    password_input = driver.find_element(by=By.ID, value="password")
    password_input.clear()
    password_input.send_keys(password)

    login_button = driver.find_element(
        by=By.CLASS_NAME,
        value="from__button--floating"
    )
    login_button.click()


def connect_to_hr(connect_buttons: List, driver, connected) -> int:
    for btn in connect_buttons:
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

        send = driver.find_element(by=By.XPATH, value="//button[@aria-label='Send now']")
        driver.execute_script("arguments[0].click();", send)
        connected += 1
        time.sleep(1)
    return connected


def run(driver):
    try:
        driver.get(url=URL)
        register(driver)

        connected = 0
        page = 1

        while True:
            if connected == 80:
                break

            driver.get(url=f"https://www.linkedin.com/search/results/people/?"
                           f"keywords=it%20recruiter%2F%20it%20acquisition%20specialist&origin=CLUSTER_EXPANSION&page={page}&sid=zZd")

            all_buttons = driver.find_elements(by=By.TAG_NAME, value="button")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

            connected = connect_to_hr(connect_buttons=connect_buttons, driver=driver, connected=connected)

            page += 1
        print(f"{connected} HR's connected")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == "main":
    chrome_driver = webdriver.Chrome(DRIVER_PATH)

    run(driver=chrome_driver)
