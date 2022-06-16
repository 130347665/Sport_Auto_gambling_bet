import sys
from PyQt5 import sip
import PyQt5.QtWidgets
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime

nowtime = datetime.date.today()
second_date = datetime.date(2022, 6, 18)
if nowtime < second_date:
    print("可以用")
else:
    quit()
print(nowtime)
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
    #下注場次名稱為str參數類型
    betting_name = pyqtSignal(str)
    # 以下注過的信息_標題為str參數類型
    betting_title = pyqtSignal(str)
    # 以下注過的信息_下注隊伍為str參數類型
    betting_team = pyqtSignal(str)
    # 以下注過的信息_隊伍信息為str參數類型
    betting_team_inf = pyqtSignal(str)
    # 以下注過的信息_list信息為list參數類型
    betting_inf = pyqtSignal(list)
    def __init__(self,parent1,parent2,parent3,account,password):
        super(BackQthread, self).__init__()
        self.parent1 = parent1
        self.parent2 = parent2
        self.parent3 = parent3
        self.account = account
        self.password = password
    def run(self):
        以下注過的信息 = []
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
            tonow = datetime.datetime.now()
            now_money = driver.find_element(By.XPATH, '//*[@id="use-credit-{0}"]'.format(tonow.day+1)).text
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

            #0616

            while True:
                下注場次名稱 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[1]').text
                print(下注場次名稱)
                以下注過的信息_標題 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[1]').text
                print(以下注過的信息_標題)
                以下注過的信息_下注隊伍 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[3]').text
                print(以下注過的信息_下注隊伍)
                以下注過的信息_隊伍信息 = driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute(
                    'innerText')
                for i in range(0, len(以下注過的信息)):
                    if 以下注過的信息_標題 == 以下注過的信息[i][0]:
                        if 下注場次名稱 == 以下注過的信息[i][1]:
                            if 以下注過的信息_隊伍信息 == 以下注過的信息[i][3]:
                                print("已經下過了 即將結束")
                                driver.get(sportWebsite)
                                driver.implicitly_wait(6)  # 等待加載完成 最多6秒
                                test1 = driver.find_elements(By.XPATH,
                                                             '//*[@id="left-menu"]/ul/li[@class=""]')  # li下 不等於hide的元素
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
                    以下注過的信息_隊伍信息 = driver.find_element(By.XPATH,
                                                       '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute(
                        'innerText')
                    break
            以下注過的信息.append([以下注過的信息_標題, 下注場次名稱, 以下注過的信息_下注隊伍, 以下注過的信息_隊伍信息])
            print(以下注過的信息)
            #回傳給tablewidge更新ui
            self.betting_inf.emit([以下注過的信息[num][0],以下注過的信息[num][1],以下注過的信息[num][2],以下注過的信息[num][3]])
            # self.betting_title.emit(以下注過的信息[num][0])
            # self.betting_name.emit(以下注過的信息[num][1])
            # self.betting_team.emit(以下注過的信息[num][2])
            # self.betting_team_inf.emit(以下注過的信息[num][3])
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
                        dm.MoveTo(160, 141)
                        dm.LeftDoubleClick()
                    dm.SetWindowState(LineWindow, 1)
                    dm.SetWindowState(LineWindow, 8)
                    dm.SetWindowState(LineWindow, 7)
                    dm.SetWindowState(LineWindow, 12)
                    time.sleep(0.2)
                    dm.MoveTo(402, 648)  # 點及輸入訊息
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()

                    dm.MoveTo(383, 722)
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    time.sleep(2)
                    dm.SetWindowState(LineWindow, 9)
                else:
                    print("綁定失敗")

                time.sleep(1)

                # 綁定開啟窗口
                # ComboBoxEx32
                Line_Select_file = dm.FindWindow("#32770", "")
                if Line_Select_file ==0:
                    dm.SetWindowState(LineWindow, 1)
                    dm.SetWindowState(LineWindow, 8)
                    dm.SetWindowState(LineWindow, 7)
                    dm.SetWindowState(LineWindow, 12)
                    time.sleep(0.5)
                    dm.MoveTo(402, 648)  # 點及輸入訊息
                    dm.LeftDoubleClick()
                    time.sleep(0.1)
                    dm.LeftDoubleClick()
                    time.sleep(0.1)
                    dm.LeftDoubleClick()
                    time.sleep(0.1)
                    dm.LeftDoubleClick()
                    time.sleep(0.1)
                    dm.LeftDoubleClick()
                    time.sleep(0.1)
                    dm.LeftDoubleClick()
                    time.sleep(0.1)
                    dm.LeftDoubleClick()
                    time.sleep(0.1)

                    dm.MoveTo(383, 722)
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    dm.LeftDoubleClick()
                    time.sleep(2)
                    dm.SetWindowState(LineWindow, 9)
                    print("進來了")
                else:
                    print("綁定失敗")
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
                LineBinding = dm.UnBindWindow()
                dm.SendString2(Line_Select_file_Edit, os.getcwd() + "\\" + "abdc.png")
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
        #tablewidge更新UI
        # self.backend.betting_title.connect(self.update_tablewidget_ui)
        # self.backend.betting_name.connect(self.update_tablewidget_ui)
        # self.backend.betting_team.connect(self.update_tablewidget_ui)
        # self.backend.betting_team_inf.connect(self.update_tablewidget_ui)
        self.backend.betting_inf.connect(self.update_tablewidget_ui)
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
    def update_tablewidget_ui(self,list):
        row = self.tableWidget.rowCount()

        self.tableWidget.insertRow(row)

        betting_title = PyQt5.QtWidgets.QTableWidgetItem(list[0])
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        betting_name = PyQt5.QtWidgets.QTableWidgetItem(list[1])  # 我们要求它可以修改，所以使用默认的状态即可

        betting_team = PyQt5.QtWidgets.QTableWidgetItem(list[2])
        betting_inf = PyQt5.QtWidgets.QTableWidgetItem(list[3])
        #item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择

        self.tableWidget.setItem(row, 0, betting_title)
        self.tableWidget.setItem(row, 1, betting_name)
        self.tableWidget.setItem(row, 2, betting_team)
        self.tableWidget.setItem(row, 3, betting_inf)
        # 以下可以加入保存数据到数据的操作

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())