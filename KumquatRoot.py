#--------------------------------------------
#coding=utf8
#author=WT
#date=2012-07-21
#主程序脚本
#--------------------------------------------
import wx
import thread
from MainDlg import *

# 文档编码
Encoding = u'utf8'
# 本地编码
LocalEncoding = u'gbk'
# 全局锁
GlobalLock = thread.allocate_lock()
# 队列空间限制 0为不限制
QueueCount = 0

class App(wx.App):
    def OnInit(self):
        dlg = MainDlg()
        dlg.ShowModal()
        return True


def main():
    app = App(False)
    return

if __name__ == '__main__':
    main()
