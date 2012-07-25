#--------------------------------------------
#coding=utf8
#author=WT
#date=2012-07-21
#主程序脚本
#--------------------------------------------
import wx

from MainDlg import *

class App(wx.App):
    def OnInit(self):
        dlg = MainDlg()
        dlg.ShowModal()
        return True # 模态对话框，不需要进入主消息循环，直接返回False


def main():
    app = App(False)
    return



if __name__ == '__main__':
    main()
