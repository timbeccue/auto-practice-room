from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

USERNAME = os.getenv('ARTSVISION_USERNAME')
PASS = os.getenv('ARTSVISION_PASSWORD')

START_RESERVATION = "8:00 AM"
END_RESERVATION = "11:00 AM"

driver = webdriver.Chrome()

driver.get("https://us.artsvision.net/peabody/login")
#driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")

title = driver.title
driver.implicitly_wait(5)

username_field = driver.find_element(by=By.ID, value="UserName")
password_field = driver.find_element(By.ID, "Password")
submit_button = driver.find_element(By.ID, "directLogin")

username_field.send_keys(USERNAME)
password_field.send_keys(PASS)
submit_button.click()

driver.implicitly_wait(10)
time.sleep(5)

room_requests_link = driver.find_element(By.CSS_SELECTOR, "#itm1_10 div a")
room_requests_link.click()

driver.implicitly_wait(10)
time.sleep(5)

forward_day_button = driver.find_element(By.CSS_SELECTOR, "div.av-date + div")
print(forward_day_button.text)
time.sleep(5)


#driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")
for i in range(7): 
    forward_day_button.click()
    time.sleep(2)

#driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")

driver.implicitly_wait(5)
time.sleep(5)
time.sleep(5)

room_255 = driver.find_element(By.XPATH, "//span[text()='AH255 (LoLa)']")
room_241 = driver.find_element(By.XPATH, "//span[text()='AH241 (LoLa)']")
room_262 = driver.find_element(By.XPATH, "//span[text()='AH262 (LoLa)']")
room_258 = driver.find_element(By.XPATH, "//span[text()='AH258 (LoLa)']")

#driver.save_screenshot(f"./Screenshots/{int(time.time())}-screenshot.PNG")

time.sleep(5)
room_255.click()

driver.implicitly_wait(10)

try:
    location = driver.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(1) div.av-rr-field-val a span").text
    print("location: ", location)
except:
    print("failed to get location text")
    pass

try: 
    date = driver.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(2) div.av-date input").text
    print("date: ", date)
except:
    print("failed to get date data")
    pass

time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(3) input").send_keys(START_RESERVATION)
driver.find_element(By.CSS_SELECTOR, "div.av-rr-field:nth-child(4) input").send_keys(END_RESERVATION)
confirm_button = driver.find_element(By.CSS_SELECTOR, "#buttonOk")
confirm_button.click()

driver.implicitly_wait(10)
time.sleep(5)

reservation_failed = False

select_error_modal_title = ".jqx-rc-all.jqx-rc-all-arctic.jqx-window.jqx-popup.jqx-widget.jqx-widget-content-arctic > div > div > div:not(:has(*)):not([class])"
select_error_content = f"div.jqx-widget .jqx-widget-header + .jqx-widget-content #content div"
error_title = driver.find_elements(By.CSS_SELECTOR, select_error_modal_title)
error_content = driver.find_elements(By.CSS_SELECTOR, select_error_content)

for e in error_content:
    try:
        print('error title: ', error_title)
        print('error content: ', e.text)
    except:
        print('failed to retrieve error')
    


failure_modal = driver.find_elements(By.CSS_SELECTOR, "#content div")
if failure_modal:
    reservation_failed = True
    for element in failure_modal:
        print(f"Reservation failed: {element.text}")
    

#driver.get_screenshot_as_file(f"./Screenshots/{int(time.time())}-screenshot.PNG")
time.sleep(15)

# TODO: error handling if reservation fails
# TODO: auto run with github actions cron: https://github.com/jsoma/selenium-github-actions



