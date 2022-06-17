import win32con
import win32com
import win32com.client
from io import BytesIO
dm = win32com.client.Dispatch('dm.dmsoft')
print(dm.ver())
intX = -1
intY = -1
LineWindow = dm.FindWindow("Qt5152QWindowIcon", "LINE")
print(LineWindow)
LineBinding = dm.BindWindow(LineWindow, "gdi", "windows", "windows", 0)  # 綁定搜尋到的小號那欄
print(LineBinding)
dm_ret = dm.FindPic(0, 0, 2000, 2000, r"C:\Users\user\PycharmProjects\Sport_Auto_gambling_bet\image\line.bmp", "000000", 0.9, 0)
print(dm_ret[1])
if(dm_ret[1] >= 0 and dm_ret[2] >= 0):
    while True:
        dm.MoveTo(dm_ret[1], dm_ret[2])
        dm.LeftClick()
        if dm.FindWindow("#32770", "開啟") != 0:
            print("點到了")
            break
dm.UnBindWindow()