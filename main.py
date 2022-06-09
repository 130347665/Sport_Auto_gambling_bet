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
    隨機選擇體育賽事 = 體育賽事[random.randint(0, len(體育賽事) - 1)][1]

    '//*[@id="top-bar"]/div[2]/div[3]'
    #driver.refresh() #網站刷新
    print(隨機選擇體育賽事)
    driver.find_element(By.XPATH,'//*[@id="{0}"]/div'.format(隨機選擇體育賽事)).click() #隨機點選賽事
    # '''這裡可以不用 選場次的 直接使用下面下注'''
    要下注什麼場 = driver.find_element(By.XPATH,'//*[@id="top-bar"]/div[2]')
    要下注什麼場 = 要下注什麼場.find_elements(By.XPATH,'div')
    要下注什麼場總共按鈕 = len(要下注什麼場)-2
    隨機下注場次按鈕遍號 = random.randint(1,要下注什麼場總共按鈕)
    driver.find_element(By.XPATH,'//*[@id="top-bar"]/div[2]/div[{0}]'.format(隨機下注場次按鈕遍號)).click()
    # # print("總共有{0}按鈕提選擇場次".format(要下注什麼場總共按鈕))
    '''點擊下注按鈕'''
    #odds
    '//*[@id="events-div"]/table/tbody/tr[3]/td[3]/div[3]/div[1]/a'
    '//*[@id="events-div"]/table/tbody/tr[3]/td[5]/div/div[2]/a'
    time.sleep(1)  # 休息3秒
    下注按鈕總數 = driver.find_elements(By.CLASS_NAME,'odds')
    print("總共有{0}個按鈕可以下注".format(len(下注按鈕總數)))
    try:
        隨機數 = random.randint(0, len(下注按鈕總數) - 1)
    except ValueError as e:
        print("目前無賽事可以下")
        exit()
    下注按鈕總數[隨機數].click() ##隨機點擊一個下注
    '''開始下注'''
    '//*[@id="betting-form"]/table/tbody/tr[6]/td[2]/a[1]' #Xpath定位投注1000塊的按鈕

    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="betting-form"]/table/tbody/tr[6]/td[2]/a[1]').click()  #點擊投注1000塊的按鈕

    '//*[@id="betting-confirm"]'#Xpath定位下注的按鈕
    driver.find_element(By.XPATH,'//*[@id="betting-confirm"]').click()#點擊下注\
    #截圖下注成功
    # class ="content"
    time.sleep(10)
    driver.find_element(By.CLASS_NAME, 'content').screenshot(r'abdc.png')

    time.sleep(1)
    # #------------------------Test 0608
    # #將擷取到的圖片放入剪貼簿
    # image = Image.open('abdc.png')
    # output = BytesIO()
    # image.convert('RGB').save(output, 'BMP')
    # data = output.getvalue()[14:]
    # output.close()
    # clip.OpenClipboard()
    # clip.EmptyClipboard()
    # clip.SetClipboardData(win32con.CF_DIB, data)
    # clip.CloseClipboard()

    #發送到LINE
    for i in range(1,10):
        print("這是第{0}次".format(i))
        LineWindow = dm.FindWindow("Qt5152QWindowIcon", "LINE")
        print("Line窗口句柄:", LineWindow)
        LineBinding = dm.BindWindow(LineWindow, "normal", "windows3", "windows", 0)  # 綁定搜尋到的小號那欄
        if LineBinding == 1:
            if i >= 2: #如果大於第二輪
                dm.KeyPress(40)
            dm.SetWindowState(LineWindow, 1)
            dm.SetWindowState(LineWindow, 8)
            time.sleep(1)
            dm.MoveTo(409, 682)
            dm.LeftDoubleClick()
            dm.LeftDoubleClick()
            dm.LeftDoubleClick()
            dm.LeftDoubleClick()
            time.sleep(2)
            dm.SetWindowState(LineWindow, 9)
        else:
            print("綁定失敗")
        LineBinding = dm.UnBindWindow()
        time.sleep(1)

        # 綁定開啟窗口
        # ComboBoxEx32
        Line_Select_file = dm.FindWindow("#32770", "")
        print(Line_Select_file)
        time.sleep(5)
        Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file, "ComboBoxEx32", "")
        print("ComboBoxEx32:"+str(Line_Select_file_Edit))
        Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file_Edit, "ComboBox", "")
        print("ComboBox:"+str(Line_Select_file_Edit))
        Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file_Edit, "Edit", "")
        Line_Select_file_Button = dm.FindWindowEx(Line_Select_file, "Button", "")
        print("Edit路徑句柄:"+str(Line_Select_file_Edit))
        #發送文字
        dm.SendString2(Line_Select_file_Edit, r"C:\Users\user\PycharmProjects\Sport_auto\abdc.png")
        #案開啟
        time.sleep(2)
        LineBinding = dm.BindWindow(Line_Select_file, "normal", "windows3", "windows", 0)  # 按下enter
        if LineBinding == 1:
            dm.KeyPressChar("enter")
            # dm.MoveTo(409,682)
            # dm.LeftDoubleClick()
        else:
            print("綁定失敗")
        LineBinding = dm.UnBindWindow()


    time.sleep(500)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
