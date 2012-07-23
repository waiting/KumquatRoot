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
            pos = (410, 10),
        )
        self.Bind(wx.EVT_BUTTON, self.OnClickStopButton, self.StopSearchButton)

        self.PauseSearchButton = wx.Button(
            self ,
            label = u'暂停',
            pos = (410, 40),
        )

    #-------------------------文件状态标签-------------------------
    def CreateStatusLabel(self):
        self.CurrentSearchStatusLabel = wx.StaticText(
            self,
            label = u'正在搜索:%s'%ur'D:\Develop\Python\Course\Python基础教程\Python Socket编程.txt' ,
            pos = (25, 85)
        )

        self.CurrentTotalFileLabel = wx.StaticText(
            self,
            label = u'文件总计:%s'%999999,
            pos = (30, 130)
        )
        self.CurrentPassFileLabel = wx.StaticText(
            self,
            label = u'已扫描数:%s'%999999,
            pos = (180, 130)
        )
        self.CurrentLastFileLabel = wx.StaticText(
            self,
            label = u'剩余文件:%s'%999999,
            pos = (330, 130)
        )

        #-------------------------时间状态标签-------------------------
        self.CurrentUsedTimeStatusLabel = wx.StaticText(
            self,
            label = u'已用时长:%s'%999999,
            pos = (30, 160)
        )
        self.CurrentLastTimeStatusLabel = wx.StaticText(
            self,
            label = u'剩余时长:%s'%999999,
            pos = (180, 160)
        )
        self.CurrentConformStatusLabel = wx.StaticText(
            self,
            label = u'符合条件:%s'%999999,
            pos = (330, 160)
        )

        GroupBox = wx.StaticBox(
            self,
            label = u'任务状态',
            pos = (15, 105),
            size = (465, 90)
        )

    #-------------------------事件方法-------------------------
    def OnClickStopButton(self , event):
        self.count += 1
        if self.count >= 100:
            MissionDoneDlg = wx.MessageDialog(
                parent = None ,
                message = u'任务完成!共找到符合条件的结果%d条!'%0 ,
                caption = u'任务完成' ,
                style = wx.OK|wx.ICON_INFORMATION
            )
            MissionDoneDlg.ShowModal()
            MissionDoneDlg.Destroy()
            self.Destroy()
        self.gauge.SetValue(self.count)

def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg()
    dlg.ShowModal()

if __name__ == '__main__':
    test()
