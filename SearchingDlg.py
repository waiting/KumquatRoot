#!/usr/bin/python
#coding:utf-8

#-------------------------------------------------------------------------------
# Name:        SearchingDlg.py
# Purpose:
#
# Author:      Mr.Wid
#
# Created:     22-07-2012
# Copyright:   (c) Mr.Wid 2012
# Licence:
#-------------------------------------------------------------------------------

import wx

class PressPauseButton(Exception):
    pass

class PressStopButton(Exception):
    pass

class SearchingDlg(wx.Dialog):
    #-----------------------初始化进度条窗口-----------------------------
    def __init__(
        self,
        parent = None,
    ):
        wx.Dialog.__init__(
            self,
            parent,
            title = u'正在搜索...',
            size = (500, 240),
            style = wx.CAPTION
        )
        self.CreateProgressBar()    #创建进度条

        '''
        #-------------封装测试-------------
        self.setProgressLength(80)      #设置进度条进度测试
        sclab=ur'D:\Aevelop\bython\Yourse\jython基础教程\Zython Socket编程.txt'
        self.setScarchingFileName(sclab)     #设置正在搜索的容测试
        self.setTotalFileNumber(u'12345')    #设置文件总计测试
        self.setSearchedFileNumber(u'99999')   #设置已扫描数总计测试
        self.setSurplusFileNumber(u'23654')      #设置剩余文件总计测试
        self.setUsedTime(u'24秒')        #设置已用时长测试
        self.setSurplusTime(u'8765秒')   #设置剩余时长测试
        self.setConformNumber(u'0')
        '''

    #------------------------创建进度条-----------------------------------------
    def CreateProgressBar(self):
        self.count = 0      #进度条计数
        self.gauge = wx.Gauge(self, -1, 100, (25, 25), (370, 30))
        self.gauge.SetBezelFace(2)
        self.gauge.SetShadowWidth(2)

        self.CreateStopPauseButton()    #创建终止、暂停按钮
        self.CreateStatusLabel()    #创建任务状态标签

    #------------------------创建终止、暂停按钮-------------------------
    def CreateStopPauseButton(self):
        self.StopSearchButton = wx.Button(
            self,
            label = u'终止',
            pos = (410, 40),
        )
        self.Bind(wx.EVT_BUTTON, self.ClickStopButton, self.StopSearchButton)

        self.PauseSearchButton = wx.Button(
            self ,
            label = u'暂停',
            pos = (410, 10),
        )
        self.Bind(wx.EVT_BUTTON, self.ClickPauseButton, self.PauseSearchButton)

    #-------------------------文件状态标签-------------------------
    def CreateStatusLabel(self):
        self.CurrentSearchStatusLabel = wx.StaticText(
            self,
            label = u'正在搜索:',
            pos = (25, 85)
        )

        self.CurrentTotalFileLabel = wx.StaticText(
            self,
            label = u'文件总计:',
            pos = (30, 130)
        )
        self.CurrentPassedFileLabel = wx.StaticText(
            self,
            label = u'已扫描数:',
            pos = (180, 130)
        )
        self.CurrentLastFileLabel = wx.StaticText(
            self,
            label = u'剩余文件:',
            pos = (330, 130)
        )

        #-------------------------时间状态标签-------------------------
        self.CurrentUsedTimeStatusLabel = wx.StaticText(
            self,
            label = u'已用时长:',
            pos = (30, 160)
        )
        self.CurrentLastTimeStatusLabel = wx.StaticText(
            self,
            label = u'剩余时长:',
            pos = (180, 160)
        )
        self.CurrentConformStatusLabel = wx.StaticText(
            self,
            label = u'符合条件:',
            pos = (330, 160)
        )

        groupBox = wx.StaticBox(
            self,
            label = u'任务状态',
            pos = (15, 105),
            size = (465, 90)
        )

    #-------------------------总事件方法-------------------------#

    #-------------------------任务状态方法开始-------------------
    '''
    从'任务状态方法开始'到'任务状态方法结束'部分为面板上'任务状态'框架内的各个标签的内容设置方法
    '''

    #设置进度条已完成进度
    def setProgressLength(self , percent = 0):
        '''
        方法名称:setProgressLength
        原型:setProgressLength(self, int percent)
        调用示例:SearchingDlg.setProgressLength(80)
        '''
        if percent >= 100:
            MissionDoneDlg = wx.MessageDialog(
                parent = None ,
                message = u'任务完成!共找到符合条件的结果%d条!'%0 ,
                caption = u'任务完成' ,
                style = wx.OK|wx.ICON_INFORMATION
            )
            MissionDoneDlg.ShowModal()
            MissionDoneDlg.Destroy()
            self.Destroy()
        self.gauge.SetValue(percent)

    #设置"正在搜索"标签内容
    def setScarchingFileName(self, content = None):
        '''
        #方法名称:setScarchingFileName
        原型:setScarchingFileName(self, string content)
        调用示例:SearchingDlg.setScarchingFileName('wxPython')
        '''
        self.CurrentSearchStatusLabel.SetLabel(u'正在搜索:' + str(content))

    #设置"文件总计"标签内容
    def setTotalFileNumber(self, number = None):
        '''
        #方法名称:setTotalFileNumber
        原型:setTotalFileNumber(self, string number)
        调用示例:SearchingDlg.setTotalFileNumber(u'12345')
        '''
        self.CurrentTotalFileLabel.SetLabel(u'文件总计:' + str(number))

    #设置"已扫面数"标签内容
    def setSearchedFileNumber(self, number = None):
        '''
        #方法名称:setSearchedFileNumber
        原型:setSearchedFileNumber(self, string number)
        调用示例:SearchingDlg.setSearchedFileNumber(u'12345')
        '''
        self.CurrentPassedFileLabel.SetLabel(u'已扫描数:' + str(number))

    #设置"剩余文件"标签内容
    def setSurplusFileNumber(self, number = None):
        '''
        #方法名称:setSurplusFileNumber
        原型:setSurplusFileNumber(self, string number)
        调用示例:SearchingDlg.setSurplusFileNumber(u'12345')
        '''
        self.CurrentLastFileLabel.SetLabel(u'剩余文件:' + str(number))

    #设置"已用时长"标签内容
    def setUsedTime(self, number = None):
        '''
        #方法名称:setUsedTime
        原型:setUsedTime(self, string number)
        调用示例:SearchingDlg.setUsedTime(u'24秒')
        '''
        self.CurrentUsedTimeStatusLabel.SetLabel(u'已用时长:' + str(number))

    #设置"剩余时长"标签内容
    def setSurplusTime(self, number = None):
        '''
        #方法名称:setSurplusTime
        原型:setSurplusTime(self, string number)
        调用示例:SearchingDlg.setSurplusTime(u'12345')
        '''
        self.CurrentLastTimeStatusLabel.SetLabel(u'剩余时长:' + str(number))

    #设置"符合条件"标签内容
    def setConformNumber(self, number = None):
        '''
        #方法名称:setConformNumber
        原型:setConformNumber(self, string number)
        调用示例:SearchingDlg.setConformNumber(u'12345')
        '''
        self.CurrentConformStatusLabel.SetLabel(u'符合条件:' + str(number))
    #-------------------------任务状态方法结束-------------------

    #-------------------------按钮方法开始-----------------------
    '''
    从'按钮方法开始'到'按钮方法结束'部分为面板上'暂停'、'终止'两个按钮的方法
    '''

    def ClickPauseButton(self, event):  #点击"暂停"按钮时引发暂停异常
        raise PressPauseButton

    def ClickStopButton(self, event):   #点击"终止"按钮时引发终止异常
        raise PressStopButton
    #-------------------------按钮方法结束-----------------------


def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg()
    dlg.ShowModal()

if __name__ == '__main__':
    test()
