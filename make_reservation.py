from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import time
import os
import random

USERNAME = os.getenv('ARTSVISION_USERNAME')
PASS = os.getenv('ARTSVISION_PASSWORD')

START_RESERVATION = "8:00 AM"
END_RESERVATION = "11:00 AM"


def reserve_room(driver):

    driver.get("https://us.artsvision.net/peabody/login")
    #driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")

    username_field = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="UserName"))
    password_field = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="Password"))
    submit_button = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value="directLogin"))

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASS)
    submit_button.click()

    room_requests_link = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "#itm1_10 div a"))
    room_requests_link.click()

    forward_day_button = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.av-date + div"))
    print(forward_day_button.text)


    for i in range(7): 
        print(f"Click #{i} incoming")
        time.sleep(2)
        forward_day_button.click()
        print(f"clicked {i}")

    #driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")

    time.sleep(5)

    room_255 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//span[text()='AH255 (LoLa)']"))
    room_258 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//span[text()='AH258 (LoLa)']"))
    room_260 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//span[text()='AH260 (LoLa)']"))
    room_262 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//span[text()='AH262 (LoLa)']"))

    rooms = [room_255, room_258, room_260, room_262]

    #driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")

    chosen_room = random.choice(rooms)
    chosen_room.click()

    try:
        location = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(1) div.av-rr-field-val a span")).text
        print("location: ", location)
    except:
        print("failed to get location text")
        pass

    try: 
        date = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(2) div.av-date input")).text
        print("date: ", date)
    except:
        print("failed to get date data")
        pass

    start_box = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(3) input"))
    start_box.send_keys(START_RESERVATION)
    end_box = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(4) input"))
    end_box.send_keys(END_RESERVATION)
    confirm_button = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, "#buttonOk"))
    confirm_button.click()

    reservation_failed = False

    try: 
        select_error_modal_title = ".jqx-rc-all.jqx-rc-all-arctic.jqx-window.jqx-popup.jqx-widget.jqx-widget-content-arctic > div > div > div:not(:has(*)):not([class])"
        select_error_content = f"div.jqx-widget .jqx-widget-header + .jqx-widget-content #content div"
        error_title = WebDriverWait(driver, timeout=10).until(lambda d: d.find_elements(By.CSS_SELECTOR, select_error_modal_title))
        error_content = WebDriverWait(driver, timeout=10).until(lambda d: d.find_elements(By.CSS_SELECTOR, select_error_content))
        

        for e in error_content:
            try:
                print('error title: ', error_title)
                print('error content: ', e.text)
            except:
                print('failed to retrieve error')
            


        failure_modal = WebDriverWait(driver, timeout=10).until(lambda d: d.find_elements(By.CSS_SELECTOR, "#content div"))
        if failure_modal:
            reservation_failed = True
            for element in failure_modal:
                print(f"Reservation failed: {element.text}")
    except:
        print('failed to do error handling routine')
        

#driver.get_screenshot_as_file(f"./Screenshots/{int(time.time())}-screenshot.PNG")

# TODO: error handling if reservation fails
# TODO: auto run with github actions cron: https://github.com/jsoma/selenium-github-actions

if __name__=="__main__":
    driver = webdriver.Chrome()
    reserve_room(driver)


