#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Mr.Miao
#
# Created:     23-07-2012
# Copyright:   (c) Mr.Miao 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import SearchingDlg
import wx
import os
import time
import thread

def testMethod(parent):
    path = r'D:\Kugou'
    fileName = os.listdir(path)
    totalFileNumber = len(fileName)
    totalTime = totalFileNumber * 0.1
    usedTime = 0
    searchedCount = 0

    parent.setTotalFileNumber(str(totalFileNumber))  #总文件数

    for i in fileName:
        time.sleep(0.1)
        searchedCount += 1
        progressLength = int((float(searchedCount)/totalFileNumber)*100)
        usedTime += 0.1     #已用时
        totalTime -= 0.1   #剩余时间

        parent.setProgressLength(progressLength)    #进度条状态
        parent.setScarchingFileName(path + '\\'+str(i))    #正在扫描的文件名
        parent.setSearchedFileNumber(str(searchedCount)) #已扫描文件数
        parent.setSurplusFileNumber(str(totalFileNumber-searchedCount))  #剩余文件总数
        parent.setUsedTime(str(usedTime)+'秒')    #已用时长
        parent.setSurplusTime(str(totalTime)+'秒')    #剩余时长
        parent.setConformNumber(str(searchedCount))  #符合条件数量

def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg.SearchingDlg()
    thread.start_new_thread(testMethod,(dlg,))
    time.sleep(0.01)
    dlg.ShowModal()

if __name__ == '__main__':
    test()