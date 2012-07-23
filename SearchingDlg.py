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
    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent,
            title = u'搜索中...',
            size = (500, 240),
            style = wx.DEFAULT_DIALOG_STYLE
        )
        self.CreateProgressBar() #创建进度条
        self.count = 0 #进度条计数

    #------------------------创建进度条-----------------------------------------
    def CreateProgressBar(self):
        self.count = 0
        self.gauge = wx.Gauge(self, -1, 100, (25, 25), (370, 30))
        self.gauge.SetBezelFace(2)
        self.gauge.SetShadowWidth(2)

        self.CreateStopPauseButton()                                            #创建终止、暂停按钮
        self.CreateStatusLabel()

    def CreateStopPauseButton(self):
        self.StopToSearchButton = wx.Button(
			self,
            label = u'终止',
            pos = (410, 10)
        )
        self.Bind(wx.EVT_BUTTON, self.OnClickStopButton, self.StopToSearchButton)

        self.PauseSearchButton = wx.Button(
			self,
            label = u'暂停',
            pos = (410, 40),
        )

    def CreateStatusLabel(self):
        self.CurrentSearchStatusLabel = wx.StaticText(
            self,
            label = u'正在搜索:%s' % ur'D:\Develop\Python\Course\Python基础教程\Python Socket编程.txt',
            pos = (25, 85)
        )

        self.CurrentFileStatusLabel = wx.StaticText(
            self,
            label = u'%10s:%-10s%10s:%-10s%10s:%-10s' % (u'文件总计', 9999, u'已完成', 9999, u'剩余', 9999),
            pos = (25, 130)
        )

        self.CurrentTimeStatusLabel = wx.StaticText(
            self,
            label = u'%10s:%-10s%10s:%-10s%10s:%-10s' % (u'已用时', 9999, u'剩余用时', 9999, u'符合条件数量', 9999),
            pos = (25, 160)
        )

        groupbox = wx.StaticBox(
            self,
            label = u'任务状态',
            pos = (15, 105),
            size = (465, 90)
        )


    #-------------------------事件方法------------------------------------------
    def OnClickStopButton(self, event):
        self.count += 1
        if self.count >= 100:
            MissionDoneDlg = wx.MessageDialog(
                None,
                message = u'任务完成!共找到符合条件的结果%d条!' % 0,
                caption = u'任务完成',
                style = wx.OK | wx.ICON_INFORMATION
            )
            MissionDoneDlg.ShowModal()
            MissionDoneDlg.Destroy()
        self.gauge.SetValue(self.count)


def test():
    app = wx.PySimpleApp()
    frame = SearchingDlg(None)
    frame.ShowModal()

if __name__ == '__main__':
    test()
