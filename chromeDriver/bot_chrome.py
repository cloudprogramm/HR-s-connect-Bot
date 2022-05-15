import time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from chromeDriver import _auth_data
from params import Params


class LinkedinBot:

    def __init__(self, driver):
        self.__driver = driver

    def __register(self) -> None:
        # Initializing account data
        __account_data = _auth_data.AccountData()

        # Connecting to account
        email_input = self.__driver.find_element(by=By.ID, value="username")
        email_input.clear()
        email_input.send_keys(__account_data.EMAIL)

        password_input = self.__driver.find_element(by=By.ID, value="password")
        password_input.clear()
        password_input.send_keys(__account_data.PASSWORD)

        login_button = self.__driver.find_element(
            by=By.CLASS_NAME,
            value="from__button--floating"
        )
        login_button.click()

    def __connect_to_hr(self, connect_buttons: List, connected: int) -> int or dict:
        for btn in connect_buttons:
            self.__driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.6)

            send = self.__driver.find_element(by=By.XPATH, value="//button[@aria-label='Send now']")
            self.__driver.execute_script("arguments[0].click();", send)
            time.sleep(0.6)

            try:
                # If we got an alert - stopping the program
                if self.__driver.find_element(by=By.ID, value="ip-fuse-limit-alert__header"):
                    return {"connected": connected, "stop_function": True}
            except Exception as ex:
                print(ex)

            connected += 1
        return connected

    def run(self) -> None:
        try:
            __parameters = Params()
            self.__driver.get(url=__parameters.URL)
            self.__register()

            _connected = 0
            _page = 60

            while _connected != __parameters.amount_connects:
                self.__driver.get(url=f"https://www.linkedin.com/search/results/people/?"
                                      f"keywords=it%20recruiter%2F%20it%20acquisition%20"
                                      f"specialist&origin=CLUSTER_EXPANSION&page={_page}&sid=zZd")

                __all_buttons = self.__driver.find_elements(by=By.TAG_NAME, value="button")
                __connect_buttons = [btn for btn in __all_buttons if btn.text == "Connect"]

                _connected = self.__connect_to_hr(connect_buttons=__connect_buttons, connected=_connected)

                if type(_connected) is dict:
                    print(f"{_connected['connected']} HR's connected")
                    break

                _page += 1
        except Exception as ex:
            print(ex)
        finally:
            self.__driver.close()
            self.__driver.quit()


if __name__ == "__main__":
    __parameters = Params()
    chrome_driver = webdriver.Chrome(__parameters.DRIVER_PATH)
    bot = LinkedinBot(chrome_driver)

    bot.run()
