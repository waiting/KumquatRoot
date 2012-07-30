#--------------------------------------------
#coding=utf8
#author=WT
#date=2012-07-21
#主程序脚本
#--------------------------------------------
import wx
import threading
import MainDlg

# 全局锁
GlobalLock = threading.Lock()
# 文档编码
Encoding = u'utf8'
# 本地编码
LocalEncoding = u'gbk'

class Limit:
	# 队列空间限制 0为不限制
	QueueCount = 0
	# 限制文件总数 0为不限制
	TotalFiles = 0
	# 限制文件大小，超过这个大小则不搜索 0为不限制
	FileSize = 0 #1024 * 1024 * 5 # 5MB

class App(wx.App):
    def OnInit( self ):
        dlg = MainDlg.MainDlg()
        dlg.ShowModal()
        return True

def do_events():
    pass#wx.GetApp().ProcessPendingEvents()

def main():
    app = App(False)
    return

if __name__ == '__main__':
    main()
