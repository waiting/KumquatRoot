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
try:
    import wx
    import thread
    import Queue
    import os
    from MainDlg import MainDlg
except ImportError:
    pass

# 搜索线程
def cb_searching( *args, **kwargs ):
    "cb_searching( SearchingDlg searchDlg, MainDlg mainDlg, Queue queue, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue
    while True:
        filePath = queue.get()
        if None == filePath:
            break
        # 进行搜索
        if mainDlg:
            mainDlg.addResult( os.path.basename(filePath), os.path.dirname(filePath), None )

# 统计线程
def cb_statistic( *args, **kwargs ):
    "cb_statistic( SearchingDlg searchDlg, MainDlg mainDlg, Queue queue, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue

    if params and params['RootPath']:
        for rootPath, dirNames, fileNames in os.walk(params['RootPath']):
            #queue.put(rootPath)
            for fileName in fileNames:
                queue.put(rootPath + os.path.sep + fileName)

    queue.put(None)



class SearchingDlg(wx.Dialog):
    def __init__( self, parent, params, mainDlg ):
        wx.Dialog.__init__(
            self,
            parent,
            title = u'正在搜索...',
            size = ( 500, 240 ),
            style = wx.CAPTION
        )
        self._params = params # 主界面上的各项参数
        self._mainDlg = mainDlg # 控制主界面
        self._queue = Queue.Queue() # 待搜索文件队列

        thread.start_new_thread( cb_statistic, ( self, mainDlg, params ) )
        thread.start_new_thread( cb_searching, ( self, mainDlg, params ) )

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

        self._btnControl = wx.Button(
            self,
            label = u'暂停',
            pos = ( 410, 10 )
        )
        self.Bind( wx.EVT_BUTTON, self.onBtnControl, self._btnControl )

        self._btnExit = wx.Button(
            self,
            label = u'终止',
            pos = ( 410, 40 )
        )
        self.Bind( wx.EVT_BUTTON, self.onBtnExit, self._btnExit )

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


    def onBtnControl( self, evt ):
        print u'暂停'

    def onBtnExit( self, evt ):
        print u'终止'
        self.EndModal(wx.ID_ABORT)


def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg( None, {}, None )
    if dlg.ShowModal() == wx.ID_ABORT:
        pass

if __name__ == '__main__':
    test()
