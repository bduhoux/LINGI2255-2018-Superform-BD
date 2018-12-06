import time
from datetime import datetime
from datetime import timedelta
from superform.models import db, Publishing


from selenium.webdriver.common.by import By

def get_time_string(date):
    if date.month < 10:
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = "0" + str(date.day)
    else:
        day = str(date.day)
    year = str(date.year)
    return month + day + year

def login(driver):
    driver.get('http://localhost:5000/login')
    driver.maximize_window()
    driver.find_element_by_name("j_username").send_keys("myself")
    driver.find_element_by_name("j_password").send_keys("myself")
    driver.find_element(By.XPATH, "//input[@value='Login']").click()
    time.sleep(1)

def create_post(driver, title, description):
    driver.find_element(By.XPATH, "//a[@href='/new']").click()
    driver.find_element(By.XPATH, "//input[@id='titlepost']").send_keys(title)
    driver.find_element(By.XPATH, "//textarea[@id='descriptionpost']").send_keys(description)
    driver.find_element(By.XPATH, "//input[@data-module='superform.plugins.facebook']").click()

    now = datetime.now()
    driver.find_element(By.XPATH, "//input[@id='datefrompost']").click()
    driver.find_element(By.XPATH, "//input[@id='datefrompost']").send_keys(get_time_string(now))
    then = now + timedelta(days=3)
    driver.find_element(By.XPATH, "//input[@id='dateuntilpost']").click()
    driver.find_element(By.XPATH, "//input[@id='dateuntilpost']").send_keys(get_time_string(then))
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@id='publish-button']").click()

def publish_fb(driver):
    pub_id = db.session.query(Publishing).order_by(Publishing.post_id.desc()).first().post_id
    driver.get('http://localhost:5000/moderate/' + str(pub_id) +'/1')
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@id='pub-button']").click()
    login_fb(driver)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@id='pub-button']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@id='pub-button']").click()
    time.sleep(2)
    return pub_id

def login_fb(driver):
    window_before = driver.window_handles[0]
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "fb_iframe_widget").click()
    time.sleep(2)
    try:
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        driver.find_element(By.XPATH, "//input[@id='email']").send_keys("guiste10@hotmail.be")
        driver.find_element(By.XPATH, "//input[@id='pass']").send_keys("soft@123")
        driver.find_element(By.XPATH, "//input[@value='Log In']").click()
    except(IndexError):
        pass

    time.sleep(1)
    driver.switch_to.window(window_before)