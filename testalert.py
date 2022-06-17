import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(6)
driver.get('https://www.baidu.com')
time.sleep(1)
driver.execute_script("window.confirm('彈跳視窗想要顯示的文字');")
time.sleep(2)

try:
    WebDriverWait(driver, 6).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = driver.switch_to.alert
    alert.accept()
    print("確認繼續下注")
except TimeoutException:
    print("沒有繼續下注")

time.sleep(500)
