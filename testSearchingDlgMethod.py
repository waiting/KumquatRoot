#-------------------------------------------------------------------------------
# Name:        ģ��1
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

    parent.setTotalFileNumber(str(totalFileNumber))  #���ļ���

    for i in fileName:
        time.sleep(0.1)
        searchedCount += 1
        progressLength = int((float(searchedCount)/totalFileNumber)*100)
        usedTime += 0.1     #����ʱ
        totalTime -= 0.1   #ʣ��ʱ��

        parent.setProgressLength(progressLength)    #������״̬
        parent.setScarchingFileName(path + '\\'+str(i))    #����ɨ����ļ���
        parent.setSearchedFileNumber(str(searchedCount)) #��ɨ���ļ���
        parent.setSurplusFileNumber(str(totalFileNumber-searchedCount))  #ʣ���ļ�����
        parent.setUsedTime(str(usedTime)+'��')    #����ʱ��
        parent.setSurplusTime(str(totalTime)+'��')    #ʣ��ʱ��
        parent.setConformNumber(str(searchedCount))  #������������

def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg.SearchingDlg()
    thread.start_new_thread(testMethod,(dlg,))
    time.sleep(0.01)
    dlg.ShowModal()

if __name__ == '__main__':
    test()