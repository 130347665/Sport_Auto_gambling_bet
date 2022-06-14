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
LineWindow = dm.FindWindow("Qt5152QWindowIcon", "LINE")
print("Line窗口句柄:", LineWindow)
for i in range(1,3+1):
    print("第",i,"次")
    LineBinding = dm.BindWindow(LineWindow, "gdi", "windows3", "windows", 0)  # 綁定搜尋到的小號那欄
    if LineBinding == 1:
        if i >= 2:  # 如果大於第二輪
            dm.KeyPress(40)
        if i == 1: #第一輪先點一下測試
            dm.MoveTo(190, 141)
            dm.LeftDoubleClick()
        dm.SetWindowState(LineWindow, 1)
        dm.SetWindowState(LineWindow, 8)
        dm.SetWindowState(LineWindow, 7)
        dm.SetWindowState(LineWindow, 12)
        time.sleep(3)
        dm.MoveTo(423,615)#點及輸入訊息
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
    LineBinding = dm.UnBindWindow()

    time.sleep(1)

    # 綁定開啟窗口
    # ComboBoxEx32
    Line_Select_file = dm.FindWindow("#32770", "")
    print(Line_Select_file)
    time.sleep(5)
    Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file, "ComboBoxEx32", "")
    print("ComboBoxEx32:" + str(Line_Select_file_Edit))
    Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file_Edit, "ComboBox", "")
    print("ComboBox:" + str(Line_Select_file_Edit))
    Line_Select_file_Edit = dm.FindWindowEx(Line_Select_file_Edit, "Edit", "")
    Line_Select_file_Button = dm.FindWindowEx(Line_Select_file, "Button", "")
    print("Edit路徑句柄:" + str(Line_Select_file_Edit))
    # 發送文字
    dm.SendString2(Line_Select_file_Edit, os.path.dirname(os.path.abspath(__file__)) + "\\" + "abdc.png")
    print(os.path.dirname(os.path.abspath(__file__)))
    # 案開啟
    time.sleep(2)
    LineBinding = dm.BindWindow(Line_Select_file, "normal", "windows3", "windows", 0)  # 按下enter
    if LineBinding == 1:
        dm.KeyPressChar("enter")
        # dm.MoveTo(409,682)
        # dm.LeftDoubleClick()
    else:
        print("綁定失敗")
    LineBinding = dm.UnBindWindow()


