import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from GUI.Sport import *
from PyQt5.QtCore import QThread, pyqtSignal,QDateTime
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
import os
#大漠初始化
dm = win32com.client.Dispatch('dm.dmsoft')
print(dm.ver())
website = "https://www.bl568.net/new_home2.php"
LoginUrl = "https://www.bl568.net/op/new_home2_op.php?pdisplay=login"
sportWebsite = 'https://www.bl568.net/index.php?show_game=sport'
login_session = requests.Session()
體育賽事 = []
Account = "ra62158"
Password = "a888"

class BackQthread(QThread):
    #當前餘額信號為int參數類型
    current_balance = pyqtSignal(str)
    #cookie信号为dict参数类型
    cookie_dict=pyqtSignal(dict)
    #賽事名稱信號 為 str參數类型
    sport_name = pyqtSignal(str)
    #下注的場次名稱信號為str參數類型
    sport_league_name = pyqtSignal(str)
    #當前循環為int參數類型
    now_loop = pyqtSignal(str)
    def __init__(self,parent1,parent2,parent3,account,password):
        super(BackQthread, self).__init__()
        self.parent1 = parent1
        self.parent2 = parent2
        self.parent3 = parent3
        self.account = account
        self.password = password
    def run(self):
        for num in range(0,self.parent1):
            當前循環 = num+1
            self.now_loop.emit(str(當前循環))
            print("當前循環第{0}輪".format(當前循環))
            LoginData = {'userid': self.account,
                         'passwd': self.password,
                         'lang': 'TW'}
            '''拿到登入時的Cookie'''
            login_session.post(LoginUrl, data=LoginData)
            login_session_cookie = login_session.cookies
            cookies_dictionary = login_session_cookie.get_dict()  # 登入時的COOKIE
            print(cookies_dictionary)
            #发射cookie_dict信号
            self.cookie_dict.emit(cookies_dictionary)

            '''開始進入運彩網'''
            driver = webdriver.Chrome()  # 打開Chrome
            driver.get(website)
            driver.implicitly_wait(6)  # 等待加載完成 最多6秒
            driver.add_cookie({
                'name': 'PHPSESSID',
                'value': cookies_dictionary['PHPSESSID']
            })  # 加入登入時的Cookie
            driver.get(sportWebsite)
            driver.implicitly_wait(6)  # 等待加載完成 最多6秒
            #拿到當前餘額 '//*[@id="use-credit-15"]'
            now_money = driver.find_element(By.XPATH, '//*[@id="use-credit-15"]').text
            print(now_money)
            self.current_balance.emit(now_money)

            test1 = driver.find_elements(By.XPATH, '//*[@id="left-menu"]/ul/li[@class=""]')  # li下 不等於hide的元素

            '//*[@id="gc-1"]'
            for i, good in enumerate(test1):
                體育賽事.append([good.text.splitlines()[0], good.get_attribute("id"), good.text.splitlines()[1]])  # 賽事名稱-編號-
            print(體育賽事)
            隨機選擇體育賽事 = 體育賽事[random.randint(0, len(體育賽事) - 1)]
            賽事名稱 = 隨機選擇體育賽事[0]
            print(賽事名稱)
            賽事編號 = 隨機選擇體育賽事[1]
            driver.find_element(By.XPATH, '//*[@id="{0}"]/div'.format(賽事編號)).click()  # 隨機點選賽事
            self.sport_name.emit(str(賽事名稱))#傳回賽事名稱堤共UI更新


            #''下注類型''
            #''//*[@id="top-bar"]/div[2]/div[@class="sub-btn " and not(contains(text(),"過關"))]/font[text() != "(0)"]''
            #選擇sunbtn 和 不包含過關的字 and <font>的text 不為0
            要下注什麼場 = driver.find_elements(By.XPATH, '//*[@id="top-bar"]/div[2]/div[contains(@class,"sub") and not(contains(text(),"過關"))]/font[text() != "(0)"]')
            要下注什麼場總共按鈕 = len(要下注什麼場)
            隨機下注場次按鈕遍號 = random.randint(1, 要下注什麼場總共按鈕)
            要下注什麼場[隨機下注場次按鈕遍號 - 1].click()
            #driver.find_element(By.XPATH, '//*[@id="top-bar"]/div[2]/div[{0}]'.format(隨機下注場次按鈕遍號)).click()

            #開始下注
            # odds
            time.sleep(1)  # 休息3秒
            下注按鈕總數 = driver.find_elements(By.CLASS_NAME, 'odds')
            print("總共有{0}個按鈕可以下注".format(len(下注按鈕總數)))
            try:
                隨機數 = random.randint(0, len(下注按鈕總數) - 1)
            except ValueError as e:
                print("目前無賽事可以下")
                exit()
            下注按鈕總數[隨機數].click()  ##隨機點擊一個下注

            #下注場次名稱取得
            #//*[@id="betting-div"]/div[2]/div/div[1]
            下注場次名稱 = driver.find_element(By.XPATH,'//*[@id="betting-div"]/div[2]/div/div[1]').text
            print(下注場次名稱)
            self.sport_league_name.emit(str(下注場次名稱))#傳回下注場次名稱堤共UI更新


            #下注金額
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="betting-form"]/table/tbody/tr[6]/td[2]/a[1]').click()  # 點擊投注1000塊的按鈕

            '//*[@id="betting-confirm"]'  # Xpath定位下注的按鈕
            driver.find_element(By.XPATH, '//*[@id="betting-confirm"]').click()  # 點擊下注\
            # 截圖下注成功
            # class ="content"
            time.sleep(10)
            driver.find_element(By.CLASS_NAME, 'content').screenshot(r'abdc.png')

            time.sleep(1)


            LineWindow = dm.FindWindow("Qt5152QWindowIcon", "LINE")
            # 發送到LINE
            for i in range(0, self.parent2):
                print("LINE發送這是第{0}次".format(i + 1))
                print("Line窗口句柄:", LineWindow)
                LineBinding = dm.BindWindow(LineWindow, "normal", "windows", "windows", 0)  # 綁定搜尋到的小號那欄
                if LineBinding == 1:
                    if i >= 1:  # 如果大於第二輪
                        dm.KeyPress(40)
                    if i == 0:  # 第一輪先點一下測試
                        dm.MoveTo(190, 141)
                        dm.LeftDoubleClick()
                    dm.SetWindowState(LineWindow, 1)
                    dm.SetWindowState(LineWindow, 8)
                    dm.SetWindowState(LineWindow, 7)
                    dm.SetWindowState(LineWindow, 12)
                    time.sleep(0.2)
                    dm.MoveTo(423, 615)  # 點及輸入訊息
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()

                    dm.MoveTo(409, 682)
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    time.sleep(2)
                    dm.SetWindowState(LineWindow, 9)
                else:
                    print("綁定失敗")
                dm.UnBindWindow()
                time.sleep(1)

                # 綁定開啟窗口
                # ComboBoxEx32
                Line_Select_file = dm.FindWindow("#32770", "")
                print(Line_Select_file)
                time.sleep(0.2)
                Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file, "ComboBoxEx32", "")
                print("ComboBoxEx32:" + str(Line_Select_file_Edit))
                Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file_Edit, "ComboBox", "")
                print("ComboBox:" + str(Line_Select_file_Edit))
                Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file_Edit, "Edit", "")
                Line_Select_file_Button = dm.FindWindowEx(Line_Select_file, "Button", "")
                print("Edit路徑句柄:" + str(Line_Select_file_Edit))
                # 發送文字
                dm.SendString2(Line_Select_file_Edit, os.path.dirname(os.path.abspath(__file__)) + "\\" + "abdc.png")
                # 案開啟
                time.sleep(0.5)
                LineBinding = dm.BindWindow(Line_Select_file, "normal", "windows", "windows", 0)  # 按下enter
                if LineBinding == 1:
                    dm.KeyPressChar("enter")
                    # dm.MoveTo(409,682)
                    # dm.LeftDoubleClick()
                else:
                    print("綁定失敗")
                dm.UnBindWindow()

        #睡眠一秒
        time.sleep(self.parent2 * 1000)
class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_config)  # 發射信號給Thread1
        self.pushButton.clicked.connect(self.Thread1) #發射信號給Thread1

    def Thread1(self):
        # 实例化对象
        self.backend = BackQthread(self.參_下注幾場,self.參_有幾個群組,self.參_一輪休息時間,self.參_帳號,self.參_密碼)
        # 信号连接到界面显示槽函数
        #self.backend.cookie_dict.connect(self.set_cookie_edit)
        self.backend.current_balance.connect(self.set_current_balance)
        self.backend.sport_name.connect(self.set_sport_name_label)
        self.backend.sport_league_name.connect(self.set_sport_league_name_label)
        self.backend.now_loop.connect(self.set_now_loop_label)
        # 多线程开始
        self.backend.start()

    def get_config(self):
        self.參_下注幾場 = int(self.lineEdit.text())
        self.參_有幾個群組 = int(self.lineEdit_2.text())
        self.參_一輪休息時間 = int(self.lineEdit_3.text())
        self.參_帳號 = str(self.lineEdit_4.text())
        self.參_密碼 = str(self.lineEdit_5.text())
    # def set_cookie_edit(self, data):
    #     # 设置单行文本框的文本
    #     self.lineEdit_2.setText(str(data['PHPSESSID']))
    def set_sport_name_label(self, sport_name):
        # 設置賽事名稱
        self.label_9.setText(sport_name)
    def set_sport_league_name_label(self, sport_league_name):
        # 下注的場次名稱
        self.label_4.setText(sport_league_name)
    def set_now_loop_label(self,loop_num):
        # 設置當前輪數
        self.label_11.setText(str(loop_num))
    def set_current_balance(self, current_balance):
        self.label_2.setText(current_balance)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())