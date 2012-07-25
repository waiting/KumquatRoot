#!/usr/bin/python
#coding:utf-8

#-------------------------------------------------------------------------------
# Name:        SearchingDlg.py
# Purpose:
#
# Author:      Mr.Wid
# Modify:      WT
# Created:     22-07-2012
# Copyright:   (c) Mr.Wid 2012
# Licence:
#-------------------------------------------------------------------------------

import wx
from threading import *


class SearchingDlg(wx.Dialog):
    def __init__( self, parent, params, mainDlg ):
        wx.Dialog.__init__(
            self,
            parent,
            title = u'正在搜索...',
            size = ( 500, 240 ),
            style = wx.CAPTION
        )
        self._params = params
        self._mainDlg = mainDlg
        self.initUIs()

    def initUIs( self ):
        "初始化UI"
        self._gauge = wx.Gauge(
            self,
            range = 100,
            pos = ( 25, 25 ),
            size = ( 370, 30 )
        )
        self._gauge.BezelFace = 2    #在多数平台上都无效果
        self._gauge.ShadowWidth = 2  #在多数平台上都无效果

        self._btnPause = wx.Button(
            self,
            label = u'暂停',
            pos = ( 410, 10 )
        )
        self.Bind( wx.EVT_BUTTON, self.onBtnPause, self._btnPause )

        self._btnAbort = wx.Button(
            self,
            label = u'终止',
            pos = ( 410, 40 )
        )
        self.Bind( wx.EVT_BUTTON, self.onBtnAbort, self._btnAbort )

        #-------------------------状态标签-------------------------
        self._lblCurrentSearch = wx.StaticText(
            self,
            label = u'正在搜索:',
            pos = ( 25, 85 )
        )

        self._lblTotalFiles = wx.StaticText(
            self,
            label = u'文件总计:',
            pos = ( 30, 130 )
        )
        self._lblScanFiles = wx.StaticText(
            self,
            label = u'已扫描数:',
            pos = ( 180, 130 )
        )
        self._lblSurplusFiles = wx.StaticText(
            self,
            label = u'剩余文件:',
            pos = ( 330, 130 )
        )

        self._lblUsedTime = wx.StaticText(
            self,
            label = u'已用时长:',
            pos = ( 30, 160 )
        )
        self._lblSurplusTime = wx.StaticText(
            self,
            label = u'剩余时长:',
            pos = (180, 160)
        )
        self._lblConformFiles = wx.StaticText(
            self,
            label = u'符合条件:',
            pos = ( 330, 160 )
        )

        groupBox = wx.StaticBox(
            self,
            label = u'任务状态',
            pos = (15, 105),
            size = (465, 90)
        )

    #设置进度条范围
    def setGaugeRange( self, range ):
        self._gauge.Range = range
    #设置进度条值
    def setGaugeValue( self, value ):
        self._gauge.Value = value
    #设置"正在搜索"标签内容
    def setCurrentSearch( self, content = None ):
        self._lblCurrentSearch.Label = u'正在搜索:' + unicode(content)

    #设置"文件总计"标签内容
    def setTotalFiles( self, number = None ):
        self._lblTotalFiles.Label = u'文件总计:' + unicode(number)

    #设置"已扫面数"标签内容
    def setScanFiles( self, number = None ):
        self._lblScanFiles.Label = u'已扫描数:' + unicode(number)

    #设置"剩余文件"标签内容
    def setSurplusFiles( self, number = None ):
        self._lblSurplusFiles.Label = u'剩余文件:' + unicode(number)

    #设置"已用时长"标签内容
    def setUsedTime( self, number = None ):
        self._lblUsedTime.Label = u'已用时长:' + unicode(number)

    #设置"剩余时长"标签内容
    def setSurplusTime( self, number = None ):
        self._lblSurplusTime.Label = u'剩余时长:' + unicode(number)

    #设置"符合条件"标签内容
    def setConformFiles( self, number = None ):
        self._lblConformFiles.Label = u'符合条件:' + unicode(number)


    def onBtnPause( self, event ):  #点击"暂停"按钮时引发暂停异常
        print u'暂停'

    def onBtnAbort( self, event ):   #点击"终止"按钮时引发终止异常
        print u'终止'
        self.EndModal(wx.ID_ABORT)


def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg( None, {}, None )
    if dlg.ShowModal() == wx.ID_ABORT:
        wx.MessageBox(u'终止')

if __name__ == '__main__':
    test()
