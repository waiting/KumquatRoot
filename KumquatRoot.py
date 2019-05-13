#--------------------------------------------
#coding:  utf8
#author:  WT
#date:    2012-07-21
#主程序脚本
#--------------------------------------------
import wx
import threading
import os
import sys
import MainDlg

reload(sys)

# 全局锁
GlobalLock = threading.Lock()

if sys.platform == 'win32':
    # 本地编码
    LocalEncoding = u'gb18030'
else:
    LocalEncoding = u'utf8'

sys.setdefaultencoding(LocalEncoding)

class Limit:
        # 队列空间限制 0为不限制
        QueueCount = 0
        # 限制文件总数 0为不限制
        TotalFiles = 0
        # 限制文件大小，超过这个大小则不搜索 0为不限制
        FileSize = 1024 * 1024 * 5 # 5MB
        # 搜索结果分页，0为不分页
        SplitPage = 500
        # 查询间隔(ms)
        QueryInterval = 100


def main():
    app = wx.PySimpleApp()
    dlg = MainDlg.MainDlg()
    dlg.ShowModal()


if __name__ == '__main__':
    main()
