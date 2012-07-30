#!/usr/bin/python
#coding=utf8

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
    import threading
    import Queue
    import os
    import re
    import KumquatRoot
    import MainDlg
except ImportError, e:
    pass


# 搜索线程
def cb_searching( *args, **kwargs ):
    "cb_searching( SearchingDlg searchDlg, MainDlg mainDlg, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue

    while True:
        filePath = queue.get()
        if None == filePath:
            searchDlg.isFinish = True
            break

        #searchDlg.setCurrentSearch(filePath)
        searchDlg.currentSearch = filePath

        # 进行搜索
        isConform = False
        if params and params['IsSearchWords']:
            pass #isConform = True
        else:
            searchDlg._conformFiles += 1
            isConform = True

        searchDlg._scanFiles += 1
        searchDlg._surplusFiles = searchDlg._totalFiles - searchDlg._scanFiles

        #if isConform:
            #searchDlg.setConformFiles(searchDlg._conformFiles)

        #searchDlg.setScanFiles(searchDlg._scanFiles)
        #searchDlg.setSurplusFiles(searchDlg._surplusFiles)

        #searchDlg.setGaugeValue(searchDlg._scanFiles)

        #if mainDlg and isConform:
            #mainDlg.notifyAddResult( os.path.basename(filePath), os.path.dirname(filePath), u'None' )

        if searchDlg.isAbort:
            break


# 统计线程
def cb_statistic( *args, **kwargs ):
    "cb_statistic( SearchingDlg searchDlg, MainDlg mainDlg, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue
    if params:
        for rootPath, dirNames, fileNames in os.walk(params['RootPath']):
            if KumquatRoot.Limit.TotalFiles > 0 and searchDlg._totalFiles == KumquatRoot.Limit.TotalFiles:
                break

            if searchDlg.isAbort:
                break

            for fileName in fileNames:
                # 判断根目录的情况
                if re.match( '^\\w:\\\\$', rootPath ):
                    filePath = rootPath + fileName
                elif re.match( '^/$', rootPath ):
                    filePath = rootPath + fileName
                else:
                    filePath = rootPath + os.path.sep + fileName
                # 文件大小限制
                if KumquatRoot.Limit.FileSize > 0 and os.path.getsize(filePath) > KumquatRoot.Limit.FileSize:
                    continue
                #进行名单过滤
                pats = []
                for pat in params['FilterExtList']:
                    if not pat:
                        pats.append(r'^[^\.]+$')
                    else:
                        pats.append( r'\.' + pat + '$' )
                patStr = '|'.join(pats)
                if patStr:
                    if params['UseListMode'] == 0: # 黑名单
                        if re.search( patStr, fileName, re.IGNORECASE ):
                            continue
                    elif params['UseListMode'] == 1: # 白名单
                        if not re.search( patStr, fileName, re.IGNORECASE ):
                            continue

                #进行文件名过滤
                if params['IsUseMatchName']:
                    if params['MatchName']:
                        print `params['MatchName']`
                        if not re.search( params['MatchName'], fileName, re.IGNORECASE ):
                            continue

                searchDlg._totalFiles += 1
                #searchDlg.setTotalFiles(searchDlg._totalFiles)
                #searchDlg.setGaugeRange(searchDlg._totalFiles)

                queue.put(filePath)

                if KumquatRoot.Limit.TotalFiles > 0 and searchDlg._totalFiles == KumquatRoot.Limit.TotalFiles:
                    break

                if searchDlg.isAbort:
                    break

    #放入一个None，让搜索线程退出
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
        self.initUIs()

        self._params = params # 主界面上的各项参数
        self._mainDlg = mainDlg # 控制主界面
        self._queue = Queue.Queue(KumquatRoot.Limit.QueueCount) # 待搜索文件队列

        self.isFinish = False
        self.isAbort = False

        self._totalFiles = 0
        self._scanFiles = 0
        self._surplusFiles = 0
        self._conformFiles = 0
        self._usedTime = 0
        self._surplusTime = 0

        self._statistic = threading.Thread( None, cb_statistic, None, ( self, mainDlg, params ) )
        self._searching = threading.Thread( None, cb_searching, None, ( self, mainDlg, params ) )
        self._statistic.start()
        self._searching.start()

        self._timer = wx.Timer(self)
        self._timer.Start(10)
        self.Bind( wx.EVT_TIMER, self.onTimer )

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
        self._gauge.Range = 100

        self._btnControl = wx.Button(
            self,
            label = u'暂停',
            pos = ( 410, 10 )
        )

        self._btnExit = wx.Button(
            self,
            label = u'终止',
            pos = ( 410, 40 )
        )

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

        self.Bind( wx.EVT_BUTTON, self.onBtnControl, self._btnControl )
        self.Bind( wx.EVT_BUTTON, self.onBtnExit, self._btnExit )
        self.Bind( MainDlg.UpdateUiEvent.EVT_UPDATEUI, self.onUpdateUi )


    def notifyGaugeRange( self, range ):
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_gauge', 'Range', range ) )
        KumquatRoot.do_events()

    def notifyGaugeValue( self, value ):
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_gauge', 'Value', value ) )
        KumquatRoot.do_events()
    def setCurrentSearch( self, content ):
        with KumquatRoot.GlobalLock:
            self._currentSearch = unicode( str(content), KumquatRoot.LocalEncoding, u'ignore' )
            self._lblCurrentSearch.Label = u'正在搜索:' + self._currentSearch


    def notifyCurrentSearch( self, content = None ):
        try:
            content = u'正在搜索:' + unicode( str(content), KumquatRoot.LocalEncoding, u'ignore' )
        except UnicodeEncodeError, e:
            content = u'正在搜索:' + content
        except UnicodeDecodeError, e:
            content = u'正在搜索:'
            print 'DecodeError:', (content)
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblCurrentSearch', 'Label', content ) )
        KumquatRoot.do_events()

    def notifyTotalFiles( self, number = None ):
        content = u'文件总计:' + unicode( str(number), KumquatRoot.LocalEncoding, u'ignore' )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblTotalFiles', 'Label', content ) )
        KumquatRoot.do_events()

    def notifyScanFiles( self, number = None ):
        content = u'已扫描数:' + unicode( str(number), KumquatRoot.LocalEncoding, u'ignore' )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblScanFiles', 'Label', content ) )
        KumquatRoot.do_events()

    def notifySurplusFiles( self, number = None ):
        content = u'剩余文件:' + unicode( str(number), KumquatRoot.LocalEncoding, u'ignore' )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblSurplusFiles', 'Label', content ) )
        KumquatRoot.do_events()

    def notifyUsedTime( self, number = None ):
        content = u'已用时长:' + unicode( str(number), KumquatRoot.LocalEncoding, u'ignore' )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblUsedTime', 'Label', content ) )
        KumquatRoot.do_events()

    def notifySurplusTime( self, number = None ):
        content = u'剩余时长:' + unicode( str(number), KumquatRoot.LocalEncoding, u'ignore' )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblSurplusTime', 'Label', content ) )
        KumquatRoot.do_events()

    def notifyConformFiles( self, number = None ):
        content = u'符合条件:' + unicode( str(number), KumquatRoot.LocalEncoding, u'ignore' )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_lblConformFiles', 'Label', content ) )
        KumquatRoot.do_events()

    def getIsFinish( self ):
        with KumquatRoot.GlobalLock:
            isFinish = self._isFinish
        return isFinish

    def setIsFinish( self, value ):
        with KumquatRoot.GlobalLock:
            self._isFinish = value
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_btnExit', 'Label', u'退出' if value else u'终止' ) )

    isFinish = property( getIsFinish, setIsFinish, doc = "是否完成搜索" )

    def getIsAbort( self ):
        with KumquatRoot.GlobalLock:
            isAbort = self._isAbort
        return isAbort

    def setIsAbort( self, value ):
        with KumquatRoot.GlobalLock:
            self._isAbort = value

    isAbort = property( getIsAbort, setIsAbort, doc = "是否终止" )

    def onTimer( self, evt ):
        if evt.Id == self._timer.Id:
            self._usedTime += self._timer.Interval
            #print self._usedTime
            self._gauge.Range = self._totalFiles
            self._gauge.Value = self._scanFiles

    # 更新UI控件的自定义事件
    def onUpdateUi( self, evt ):
        ctrlName, propName, value = evt._args
        control = self.__getattribute__(ctrlName)
        control.__setattr__( propName, value )

    def onBtnControl( self, evt ):
        print u'暂停'

    def onBtnExit( self, evt ):
        if self.isFinish:
            self.EndModal(wx.ID_EXIT)
        else:
            self.isAbort = True
            self.EndModal(wx.ID_ABORT)


def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg( None, { 'RootPath':'F:\\', 'FilterExtList':[], 'IsUseMatchName':False, 'IsSearchWords':False }, None )
    if dlg.ShowModal() == wx.ID_ABORT:
        pass

if __name__ == '__main__':
    test()
