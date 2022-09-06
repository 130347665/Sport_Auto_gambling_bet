import sys

import selenium.common.exceptions
from selenium.common.exceptions import NoSuchElementException,ElementNotSelectableException
from PyQt5 import sip
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox
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
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime
import re
#大漠初始化
dm = win32com.client.Dispatch('dm.dmsoft')
print(dm.ver())
website = "https://www.bl868.net/new_home2.php"
LoginUrl = "https://www.bl868.net/op/new_home2_op.php?pdisplay=login"
sportWebsite = 'https://www.bl868.net/index.php?show_game=sport'
login_session = requests.Session()
login_session.mount('http://', HTTPAdapter(max_retries=5))
login_session.mount('https://', HTTPAdapter(max_retries=5))
體育賽事 = []
Account = "ra71500"
Password = "sss123"
driver = None
#進入運彩網
class gambling(object):
    def __init__(self,account,password):
        self.account = account
        self.password = password
    def speak(self):
        print("我的帳號是:%s   我的密碼是:%s",{self.account,self.password})

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
    # 剩餘時間信息為int參數類型
    remaining_time = pyqtSignal(int)
    def __init__(self,parent1,parent2,parent3,account,password):
        super(BackQthread, self).__init__()
        self.parent1 = parent1
        self.parent2 = parent2
        self.parent3 = parent3
        self.account = account
        self.password = password

        self.driver = driver
    def LoginGetCookie(self):
        LoginData = {'userid': self.account,
                     'passwd': self.password,
                     'lang': 'TW'}
        '''拿到登入時的Cookie'''
        try:
            login_session.post(LoginUrl, data=LoginData, timeout=10)  # 重連四次
        except requests.exceptions.RequestException as e:
            print(e)

        login_session_cookie = login_session.cookies
        cookies_dictionary = login_session_cookie.get_dict()  # 登入時的COOKIE
        print("您登入的cookie是:" + cookies_dictionary['PHPSESSID'])
        return cookies_dictionary['PHPSESSID']
    def WenDriver_Open_ChromeDriver(self,DebugMode):
        self.DebugMode = DebugMode
        '''開始進入運彩網'''
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # 啟動無頭模式
        chrome_options.add_argument('--disable-gpu')  # windowsd必須加入此行
        if self.DebugMode == True:
            self.driver = webdriver.Chrome()
        if self.DebugMode == False:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
    def WenDriver_Go_WebSite(self):
        self.loginCookie = self.LoginGetCookie()
        self.driver.get(website)
        self.driver.implicitly_wait(6)  # 等待加載完成 最多6秒
        self.driver.add_cookie({
            'name': 'PHPSESSID',
            'value': self.loginCookie
        })  # 加入登入時的Cookie
        self.driver.get(sportWebsite)
        self.driver.implicitly_wait(6)  # 等待加載完成 最多6秒
    def UI_update_balance(self):
        tonowaddone = datetime.date.today() + datetime.timedelta(days=1)
        try:
            now_money = self.driver.find_element(By.XPATH, '//*[@id="use-credit-{0:02d}"]'.format(tonowaddone.day)).text
            print("當前餘額" + str(now_money))
            self.current_balance.emit(now_money)  # 對UI更新當前餘額
        except NoSuchElementException as exc:
            time.sleep(5)
            self.WenDriver_Go_WebSite()
            self.UI_update_balance()
    def UI_Update_sport_name(self):
        time.sleep(3)
        #//*[@id="left-menu"]/ul/li[@class=""]/div/span[@class="game-count"][text()>10] 數量大於10的
        #//*[@id="left-menu"]/ul/li[@class=""]
        test1 = self.driver.find_elements(By.XPATH, '//*[@id="left-menu"]/ul/li[@class=""]')  # li下 不等於hide的元素
        weight = []
        '//*[@id="gc-1"]'
        for i, good in enumerate(test1):
            if(int(good.text.splitlines()[1]) > 10):
                print(good.text.splitlines()[1])
                體育賽事.append([good.text.splitlines()[0], good.get_attribute("id"), good.text.splitlines()[1]])  # 賽事名稱-編號-
        #print(體育賽事)
        #計算機率 含有棒 關鍵字 機率是90
        for i in 體育賽事:
            if '棒' in i[0]:
                weight.append(90)
            else:
                weight.append(20)
        隨機選擇體育賽事 = random.choices(體育賽事, weights=weight)
        賽事名稱 = 隨機選擇體育賽事[0][0]
        #print(賽事名稱)
        賽事編號 = 隨機選擇體育賽事[0][1]
        self.driver.find_element(By.XPATH, '//*[@id="{0}"]/div'.format(賽事編號)).click()  # 隨機點選賽事
        time.sleep(3)
        while True:
            if(self.driver.find_elements(By.XPATH,'//*[@id="temp-title-tr-area"]/table/tbody/tr/td[text()= "全場讓分" ]')):
                self.sport_name.emit(str(賽事名稱))  # 傳回賽事名稱堤共UI更新
                print("已找到包含全場讓分的賽事")
                break
            else:
                print("未找到包含全場讓分的賽事 即將再選一次賽事")
                weight=[]
                time.sleep(3)
                for i in 體育賽事:
                    if '棒' in i[0]:
                        weight.append(90)
                    else:
                        weight.append(20)
                隨機選擇體育賽事 = random.choices(體育賽事, weights=weight)
                賽事名稱 = 隨機選擇體育賽事[0][0]
                print(賽事名稱)
                賽事編號 = 隨機選擇體育賽事[0][1]
                self.driver.find_element(By.XPATH, '//*[@id="{0}"]/div'.format(賽事編號)).click()  # 隨機點選賽事
    def Click_Random_Rule(self):
        try:
            下注規則 = self.driver.find_elements(By.XPATH,
                                          '//*[@id="top-bar"]/div[2]/div[(contains(text(),"全場"))]/font[text()!= "(0)"]')
            隨機規則按鈕遍號 = random.randint(0, len(下注規則)-1)
            下注規則[隨機規則按鈕遍號].click()
            time.sleep(2)  # 休息3秒
        except ValueError as e:
            print("沒有全場可以按")
            time.sleep(3)
            self.WenDriver_Go_WebSite()
            self.UI_update_balance()
            self.UI_Update_sport_name()
            self.Click_Random_Rule()
        except ElementNotSelectableException as ea:
            print("沒有全場可以按")
            time.sleep(3)
            self.WenDriver_Go_WebSite()
            self.UI_update_balance()
            self.UI_Update_sport_name()
            self.Click_Random_Rule()
    def Click_Random_bet(self):
        下注按鈕總數 = self.driver.find_elements(By.XPATH,
                                      '//*[@class="event-tr "]/td[@class=" al-left"]/div[@class="odds-div"]/div/a[@btype=1]')
        print("總共有{0}個按鈕可以下注".format(len(下注按鈕總數)))
        try:
            隨機數 = random.randint(0, len(下注按鈕總數) - 1)
        except ValueError as e:
            print("目前無賽事可以下! 即將關閉 開始新的一輪")
            self.WenDriver_Go_WebSite()
            self.UI_update_balance()
            self.UI_Update_sport_name()
            self.Click_Random_Rule()
            self.Click_Random_bet()
        下注按鈕總數[隨機數].click()  ##隨機點擊一個下注
    def bet_repeated_check(self):
        #if(self.count ==0):
            #self.以下注過的信息= [['美棒 - 全場 讓分投注', 'MLB-美國職棒-美國聯盟', 'CLE-克里夫蘭守護者 0.950', 'CLE-克里夫蘭守護者 1+70 BOS-波士頓紅襪(主)'], ['美棒 - 全場 讓分投注', 'MLB-美國職棒-美國聯盟', 'TOR-多倫多藍鳥 0.950', 'TOR-多倫多藍鳥(主) 2+95 DET-底特律老虎'], ['美棒 - 全場 讓分投注', 'MLB-美國職棒-國家聯盟', 'PHI-費城費城人 0.950', 'PHI-費城費城人 2+70 PIT-匹茲堡海盜(主)'], ['美棒 - 全場 讓分投注', 'MLB-美國職棒-國家聯盟', 'COL-科羅拉多落磯 0.950', 'LAD-洛杉磯道奇 2-20 COL-科羅拉多落磯(主)'], ['美棒 - 全場 讓分投注', 'MLB-美國職棒-美國聯盟', 'LAA-洛杉磯安那罕天使 0.950', 'LAA-洛杉磯安那罕天使(主) 1-85 TEX-德州遊騎兵'], ['美棒 - 全場 讓分投注', 'MLB-美國職棒-美國聯盟', 'LAA-洛杉磯安那罕天使 0.950', 'LAA-洛杉磯安那罕天使(主) 1-85 TEX-德州遊騎兵'], ['美棒 - 全場 讓分投注', 'MLB-美國職棒-美國聯盟', 'LAA-洛杉磯安那罕天使 0.950', 'LAA-洛杉磯安那罕天使(主) 1-85 TEX-德州遊騎兵']]
        element = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="betting-div"]/div[@class="content"]'))
        )
        下注場次名稱 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[1]').text
        #print(下注場次名稱)
        下注信息_標題 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[1]').text
        #print(下注信息_標題)
        下注信息_下注隊伍 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[3]').text
        #print(下注信息_下注隊伍)
        下注信息_隊伍信息 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute(
            'innerText')
        #print(下注信息_隊伍信息)
        #print(下注場次名稱,以下注過的信息_標題,以下注過的信息_下注隊伍,以下注過的信息_隊伍信息)
        下注信息_下注隊伍 = re.sub(r'[\s\d，。？?！“”‘’\[\]…：；:（）《》、—.．*~～＿－]', '', 下注信息_下注隊伍)
        while True:
            for i in self.以下注過的信息:
                if i[3].count(下注信息_下注隊伍):
                    print(下注信息_下注隊伍 + ":以下注過 or 反下")
                    time.sleep(10)
                    self.WenDriver_Go_WebSite()
                    self.UI_update_balance()
                    self.UI_Update_sport_name()
                    self.Click_Random_Rule()
                    self.Click_Random_bet()
                    element = WebDriverWait(self.driver, 40).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="betting-div"]/div[@class="content"]'))
                    )
                    下注場次名稱 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[1]').text
                    # print(下注場次名稱)
                    下注信息_標題 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[1]').text
                    # print(下注信息_標題)
                    下注信息_下注隊伍 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[3]').text
                    # print(下注信息_下注隊伍)
                    下注信息_隊伍信息 = self.driver.find_element(By.XPATH,
                                                         '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute(
                        'innerText')
                    # print(下注信息_隊伍信息)
                    # print(下注場次名稱,以下注過的信息_標題,以下注過的信息_下注隊伍,以下注過的信息_隊伍信息)
                    下注信息_下注隊伍 = re.sub(r'[\s\d，。？?！“”‘’\[\]…：；:（）《》、—.．*~～＿－]', '', 下注信息_下注隊伍)
            else:
                break

        print("沒有下注過的 成功跳出!")
        下注場次名稱 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[1]').text
        #print(下注場次名稱)
        下注信息_標題 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[1]').text
        #print(下注信息_標題)
        下注信息_下注隊伍 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[3]').text
        #print(下注信息_下注隊伍)
        下注信息_隊伍信息 = self.driver.find_element(By.XPATH, '//*[@id="betting-div"]/div[2]/div/div[2]').get_attribute(
            'innerText')
        #print(下注信息_隊伍信息)
        self.以下注過的信息.append([下注信息_標題, 下注場次名稱, 下注信息_下注隊伍, 下注信息_隊伍信息])
        print(self.以下注過的信息)

        self.sport_league_name.emit(str(下注場次名稱))  # 傳回下注場次名稱堤共UI更新

        time.sleep(1)
    def Click_betting_button(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="betting-form"]/table/tbody/tr[6]/td[2]/a[1]').click()  # 點擊投注1000塊的按鈕

            '//*[@id="betting-confirm"]'  # Xpath定位下注的按鈕
            self.driver.find_element(By.XPATH, '//*[@id="betting-confirm"]').click()  # 點擊下注\
        # 彈出賠率變動 是否繼續下注
        # try:
        #     WebDriverWait(self.driver, 20).until(EC.alert_is_present(),
        #                                     'Timed out waiting for PA creation ' +
        #                                     'confirmation popup to appear.')
        #
        #     alert = self.driver.switch_to.alert
        #     print("alert警告內容:" + alert.text)
        #     alert.accept()
        #     print("確認繼續下注")
        # except TimeoutException:
        #     print("沒有繼續下注")
        # 截圖下注成功
        # class ="content"

            element = WebDriverWait(self.driver, 40).until(
                EC.text_to_be_present_in_element((By.XPATH, '//*[@id="result-message"]'), "下注成功!")
            )
            print('下注成功')
            self.driver.find_element(By.ID, 'betting-div-inner-mask2').screenshot(r'abdc.png')
        except TimeoutException as e:
            print("下注失敗 即將關閉")
            self.WenDriver_Go_WebSite()
            self.UI_update_balance()
            self.UI_Update_sport_name()
            self.Click_Random_Rule()
            self.Click_Random_bet()
            self.bet_repeated_check()
            self.Click_betting_button()
        except Exception as e:
            print("發現未知錯誤 即將關閉!開始新的一輪")
            self.WenDriver_Go_WebSite()
            self.UI_update_balance()
            self.UI_Update_sport_name()
            self.Click_Random_Rule()
            self.Click_Random_bet()
            self.bet_repeated_check()
            self.Click_betting_button()
        # 回傳給tablewidge更新ui
        print("當前循環輪數:"+str(self.count))
        print(self.以下注過的信息[len(self.以下注過的信息)-1][0])
        print(self.以下注過的信息[len(self.以下注過的信息)-1][1])
        print(self.以下注過的信息[len(self.以下注過的信息)-1][2])
        print(self.以下注過的信息[len(self.以下注過的信息)-1][3])
        self.betting_inf.emit([self.以下注過的信息[len(self.以下注過的信息)-1][0], self.以下注過的信息[len(self.以下注過的信息)-1][1], self.以下注過的信息[len(self.以下注過的信息)-1][2],
                               self.以下注過的信息[len(self.以下注過的信息)-1][3]])
        time.sleep(10)
    def Line_find_window(self):
        LineWindow = dm.FindWindow("Qt5152QWindowIcon", "LINE")
        # 發送到LINE
        for i in range(0, self.parent2):
            print("LINE發送這是第{0}次".format(i + 1))
            print("Line窗口句柄:", LineWindow)
            LineBinding = dm.BindWindow(LineWindow, "gdi", "windows", "windows", 0)  # 綁定搜尋到的小號那欄
            if LineBinding == 1:
                if i >= 1:  # 如果大於第二輪
                    dm.KeyPress(40)
                if i == 0:  # 第一輪先點一下測試
                    dm.MoveTo(125, 135)
                    dm.LeftDoubleClick()
                # 重複點擊直到
                dm_ret = dm.FindPic(0, 0, 2000, 2000, r"image/line.bmp", "000000", 0.9, 0)
                if (dm_ret[1] >= 0 and dm_ret[2] >= 0):
                    while True:
                        dm.MoveToEx(0, 0, 2000, 2000)
                        dm.MoveTo(dm_ret[1], dm_ret[2])
                        dm.LeftClick()
                        time.sleep(2)
                        if dm.FindWindow("#32770", "開啟") != 0:
                            # dm.SetWindowState(LineWindow, 1)

                            Line_Select_file = dm.FindWindow("#32770", "開啟")  # 如果把傳送檔案點開就把句炳復職
                            print(Line_Select_file)
                            dm.SetWindowState(Line_Select_file, 9)
                            print("點到了")
                            break
                else:
                    print("綁定失敗")
                time.sleep(1)
                while True:
                    if dm.FindWindowEx(Line_Select_file, "ComboBoxEx32", "") != 0:  # 如果有窗口 直接輸出
                        # dm.SetWindowState(LineWindow, 1)
                        Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file, "ComboBoxEx32", "")  # 如果把傳送檔案點開就把句炳復職
                        print(Line_Select_file_Edit)
                        print("ComboBoxEx32出來了")
                        break
                    else:  # 如果沒找到句柄就點到有
                        dm.MoveToEx(0, 0, 2000, 2000)
                        dm.MoveTo(dm_ret[1], dm_ret[2])
                        dm.LeftClick()
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

        self.driver.quit()
        time.sleep(3)
    def UI_update_sleep_time(self):
        for nowsleeptime in range(self.parent3, 0, -1):
            time.sleep(1)
            self.remaining_time.emit(nowsleeptime)


    def run(self):
        self.以下注過的信息 = []
        self.count = 0
        while True:
            while self.count < self.parent1:
                當前循環 = self.count + 1
                try:
                    self.now_loop.emit(str(當前循環))
                    self.WenDriver_Open_ChromeDriver(True)
                    self.WenDriver_Go_WebSite()
                    self.UI_update_balance()
                    self.UI_Update_sport_name()
                    self.Click_Random_Rule()
                    self.Click_Random_bet()
                    self.bet_repeated_check()
                    self.Click_betting_button()
                    self.Line_find_window()
                    self.count = self.count+1
                except Exception as b:
                    with open('./日誌.txt', 'a') as f:
                        print("發生最外層錯誤")
                        errorInfo = sys.exc_info()
                        f.write(
                            "ErrorTime[{0}]-----ErrorMsg[{1}]-----ErrorRow[{2}]\n".format(str(datetime.datetime.now()),
                                                                                          str(b),
                                                                                          errorInfo[2].tb_lineno))
            self.UI_update_sleep_time()
            self.count = 0
class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_config)  # 發射信號給Thread1
        self.pushButton.clicked.connect(self.Thread1) #發射信號給Thread1
    def Thread1(self):
        #關閉botton按下
        self.pushButton.setEnabled(False)
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
        #更新剩餘時間UI
        self.backend.remaining_time.connect(self.update_remaining_time)
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
    def update_remaining_time(self,retime):
        self.label_15.setText(str(retime))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())