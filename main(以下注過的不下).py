import time
import win32clipboard as clip
import win32con
import win32com
import win32com.client
from io import BytesIO
from PIL import ImageGrab,Image
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#大漠初始化
dm = win32com.client.Dispatch('dm.dmsoft')
print(dm.ver())
website = "https://www.bl568.net/new_home2.php"
LoginUrl = "https://www.bl568.net/op/new_home2_op.php?pdisplay=login"
Account = "ra62158"
Password = "a888"
LoginData = {'userid': Account,
         'passwd':Password,
         'lang':'TW'}
sportWebsite = 'https://www.bl568.net/index.php?show_game=sport'
login_session = requests.Session()
體育賽事 = []

if __name__ == '__main__':
    '''拿到登入時的Cookie'''
    login_session.post(LoginUrl,data=LoginData)
    login_session_cookie = login_session.cookies
    cookies_dictionary = login_session_cookie.get_dict() #登入時的COOKIE
    #print(cookies_dictionary)
    '''開始進入運彩網'''
    driver = webdriver.Chrome() #打開Chrome
    driver.get(website)
    driver.implicitly_wait(6)  # 等待加載完成 最多6秒
    driver.add_cookie({
        'name': 'PHPSESSID',
        'value': cookies_dictionary['PHPSESSID']
    }) # 加入登入時的Cookie
    driver.get(sportWebsite)
    driver.implicitly_wait(6)# 等待加載完成 最多6秒
    test1 = driver.find_elements(By.XPATH,'//*[@id="left-menu"]/ul/li[@class=""]')#li下 不等於hide的元素
    print(test1)
    '//*[@id="gc-1"]'
    for i,good in enumerate(test1):
        體育賽事.append([good.text.splitlines()[0],good.get_attribute("id"),good.text.splitlines()[1]])#賽事名稱-編號-
        print(體育賽事)
    print(體育賽事)
    隨機選擇體育賽事 = 體育賽事[random.randint(0, len(體育賽事) - 1)]
    賽事名稱 = 隨機選擇體育賽事[0]
    print(賽事名稱)
    賽事編號 = 隨機選擇體育賽事[1]
    driver.find_element(By.XPATH, '//*[@id="{0}"]/div'.format(賽事編號)).click()  # 隨機點選賽事

    #''下注類型''
    #''//*[@id="top-bar"]/div[2]/div[@class="sub-btn " and not(contains(text(),"過關"))]/font[text() != "(0)"]''
    #選擇sunbtn 和 不包含過關的字 and <font>的text 不為0
    要下注什麼場 = driver.find_elements(By.XPATH, '//*[@id="top-bar"]/div[2]/div[contains(@class,"sub") and not(contains(text(),"過關"))]/font[text() != "(0)"]')
    要下注什麼場總共按鈕 = len(要下注什麼場)
    隨機下注場次按鈕遍號 = random.randint(0, 要下注什麼場總共按鈕-1)
    要下注什麼場[隨機下注場次按鈕遍號].click()
    #driver.find_element(By.XPATH, '//*[@id="top-bar"]/div[2]/div[{0}]'.format(隨機下注場次按鈕遍號)).click()
    '''點擊下注按鈕'''
    #odds
    '//*[@id="events-div"]/table/tbody/tr[3]/td[3]/div[3]/div[1]/a'
    '//*[@id="events-div"]/table/tbody/tr[3]/td[5]/div/div[2]/a'
    time.sleep(1)  # 休息3秒
    下注按鈕總數 = driver.find_elements(By.CLASS_NAME,'odds')
    print("總共有{0}個按鈕可以下注".format(len(下注按鈕總數)))
    try:
        隨機數 = random.randint(0, len(下注按鈕總數)-1)
    except ValueError as e:
        print("目前無賽事可以下")
        #重新選擇賽事
        driver.get(website)
    下注按鈕總數[隨機數].click() ##隨機點擊一個下注


    以下注過的信息 = []
    以下注過的信息.append(['其他冰球 - 全場 大小投注', 'AHL 美國冰球聯盟-不包括加時賽與點球賽', '6+85 小 0.880', '拉瓦勒火箭 VS 斯普林菲爾德雷鳥(主)'])

    while True:
        下注場次名稱 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[1]').text
        print(下注場次名稱)
        以下注過的信息_標題 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[1]').text
        print(以下注過的信息_標題)
        以下注過的信息_下注隊伍 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[3]').text
        print(以下注過的信息_下注隊伍)
        以下注過的信息_隊伍信息 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute('innerText')
        for i in range(0, len(以下注過的信息)):
             if 以下注過的信息_標題 == 以下注過的信息[i][0]:
                 if 下注場次名稱 == 以下注過的信息[i][1]:
                     if 以下注過的信息_隊伍信息 == 以下注過的信息[i][3]:
                        print("已經下過了 即將結束")
                        driver.get(sportWebsite)
                        driver.implicitly_wait(6)  # 等待加載完成 最多6秒
                        test1 = driver.find_elements(By.XPATH, '//*[@id="left-menu"]/ul/li[@class=""]')  # li下 不等於hide的元素
                        print(test1)
                        '//*[@id="gc-1"]'
                        for i, good in enumerate(test1):
                            體育賽事.append([good.text.splitlines()[0], good.get_attribute("id"),
                                         good.text.splitlines()[1]])  # 賽事名稱-編號-
                            print(體育賽事)
                        print(體育賽事)
                        隨機選擇體育賽事 = 體育賽事[random.randint(0, len(體育賽事) - 1)]
                        賽事名稱 = 隨機選擇體育賽事[0]
                        print(賽事名稱)
                        賽事編號 = 隨機選擇體育賽事[1]
                        driver.find_element(By.XPATH, '//*[@id="{0}"]/div'.format(賽事編號)).click()  # 隨機點選賽事

                        # ''下注類型''
                        # ''//*[@id="top-bar"]/div[2]/div[@class="sub-btn " and not(contains(text(),"過關"))]/font[text() != "(0)"]''
                        # 選擇sunbtn 和 不包含過關的字 and <font>的text 不為0
                        要下注什麼場 = driver.find_elements(By.XPATH,
                                                      '//*[@id="top-bar"]/div[2]/div[contains(@class,"sub") and not(contains(text(),"過關"))]/font[text() != "(0)"]')
                        要下注什麼場總共按鈕 = len(要下注什麼場)
                        隨機下注場次按鈕遍號 = random.randint(1, 要下注什麼場總共按鈕)
                        要下注什麼場[隨機下注場次按鈕遍號 - 1].click()
                        # driver.find_element(By.XPATH, '//*[@id="top-bar"]/div[2]/div[{0}]'.format(隨機下注場次按鈕遍號)).click()
                        '''點擊下注按鈕'''
                        # odds
                        '//*[@id="events-div"]/table/tbody/tr[3]/td[3]/div[3]/div[1]/a'
                        '//*[@id="events-div"]/table/tbody/tr[3]/td[5]/div/div[2]/a'
                        time.sleep(1)  # 休息3秒
                        下注按鈕總數 = driver.find_elements(By.CLASS_NAME, 'odds')
                        print("總共有{0}個按鈕可以下注".format(len(下注按鈕總數)))
                        try:
                            隨機數 = random.randint(0, len(下注按鈕總數) - 1)
                        except ValueError as e:
                            print("目前無賽事可以下")
                            # 重新選擇賽事
                            driver.get(website)
                        下注按鈕總數[隨機數].click()  ##隨機點擊一個下注
        else:
            print("成功跳出 沒有重複隊伍")
            下注場次名稱 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[1]').text
            print(下注場次名稱)
            以下注過的信息_標題 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[1]').text
            print(以下注過的信息_標題)
            以下注過的信息_下注隊伍 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[3]').text
            print(以下注過的信息_下注隊伍)
            以下注過的信息_隊伍信息 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute(
                'innerText')
            break
    以下注過的信息.append([以下注過的信息_標題, 下注場次名稱, 以下注過的信息_下注隊伍,以下注過的信息_隊伍信息])
    print(以下注過的信息)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="betting-form"]/table/tbody/tr[6]/td[2]/a[1]').click()  #點擊投注1000塊的按鈕

    '//*[@id="betting-confirm"]'#Xpath定位下注的按鈕
    driver.find_element(By.XPATH,'//*[@id="betting-confirm"]').click()#點擊下注\
    #截圖下注成功
    #Xpath下注成功 '//*[@id="result-message"]'
    # class ="content"
    try:
        element = WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="result-message"]'), "下注成功!")
        )
    except TimeoutException as e:
        print("下注失敗 即將關閉")
        driver.quit()
    finally:
        print('下注成功')
        driver.find_element(By.CLASS_NAME, 'content').screenshot(r'abdc.png')




    time.sleep(1)

    time.sleep(500)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
