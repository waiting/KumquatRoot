#!/usr/bin/python
#coding=utf8

#-------------------------------------------------------------------------------
# Name:        SearchingDlg.py
# Purpose:
#
# Author:      Mr.Wid
# Modify:      WT
# Created:     2012-07-22
# LastModify:  2012-07-31
# Copyright:   (c) Mr.Wid 2012
# Licence:
#-------------------------------------------------------------------------------
try:
    import wx
    import threading
    import time
    import math
    import Queue
    import os
    import re
    import KumquatRoot
    import MainDlg
except ImportError, e:
    pass

def bytes_unit( size ):
	if size < 1024:
		return unicode(size) + u'B'
	elif size < 1024 * 1024:
		return unicode( math.ceil( float(size) * 100 / 1024 ) / 100 ) + u'KB'
	else:
		return unicode( math.ceil( float(size) * 100 / ( 1024 * 1024 ) ) / 100 ) + u'MB'

# 搜索线程
def cb_searching( *args, **kwargs ):
    "cb_searching( SearchingDlg searchDlg, MainDlg mainDlg, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue

    while True:
        searchDlg._pause.wait() # 暂停事件锁

        filePath = queue.get()
        if None == filePath:
            searchDlg.isFinish = True
            break

        searchDlg._scanFiles += 1
        searchDlg.currentSearch = filePath

        fileName = os.path.basename(filePath)

        isDoSearch = True #是否要搜索这个文件
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
                    isDoSearch = False
            elif params['UseListMode'] == 1: # 白名单
                if not re.search( patStr, fileName, re.IGNORECASE ):
                    isDoSearch = False

        #进行文件名过滤
        if params['IsUseMatchName'] and params['MatchName']:
            if not re.search( params['MatchName'], fileName, re.IGNORECASE ):
                isDoSearch = False

        # 计算大小，判断可访问性
        try:
            fileSize = os.path.getsize(filePath)
        except:
            fileSize = None

        # 进行搜索
        isConform = False
        if isDoSearch:
            if params['IsSearchWords']:
                if fileSize != None:
                    if not ( KumquatRoot.Limit.FileSize > 0 and fileSize > KumquatRoot.Limit.FileSize ):
                        searchDlg._conformFiles += 1
                        isConform = True
                    else: # 超过大小就不搜索词组
                        pass
            else: # 不打开搜词开关
                searchDlg._conformFiles += 1
                isConform = True

            if isConform:
                try:
                    tup = ( os.path.basename(filePath), os.path.dirname(filePath), u'Size:%s' % ( bytes_unit(fileSize) if fileSize != None else u'Error' ) )
                except:
                    tup = ( 'Failed', 'Failed', 'Failed' )
                if mainDlg: mainDlg._resultItems.append(tup)

        if searchDlg.isAbort:
            break


# 统计线程
def cb_statistic( *args, **kwargs ):
    "cb_statistic( SearchingDlg searchDlg, MainDlg mainDlg, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue
    for rootPath, dirNames, fileNames in os.walk(params['RootPath']):
        searchDlg._pause.wait() # 暂停事件锁
        if KumquatRoot.Limit.TotalFiles > 0 and searchDlg._totalFiles == KumquatRoot.Limit.TotalFiles:
            break

        if searchDlg.isAbort:
            break

        for fileName in fileNames:
            searchDlg._pause.wait() # 暂停事件锁
            # 判断根目录的情况
            if re.match( '^\\w:\\\\$', rootPath ):
                filePath = rootPath + fileName
            elif re.match( '^/$', rootPath ):
                filePath = rootPath + fileName
            else:
                filePath = rootPath + os.path.sep + fileName

            searchDlg._totalFiles += 1

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
            size = ( 500, 230 ),
            style = wx.CAPTION
        )
        self.initUIs()

        self._params = params # 主界面上的各项参数
        self._mainDlg = mainDlg # 控制主界面
        self._queue = Queue.Queue(KumquatRoot.Limit.QueueCount) # 待搜索文件队列

        self.isFinish = False
        self.isAbort = False

        self._currentSearch = u''
        self._totalFiles = 0
        self._scanFiles = 0
        self._surplusFiles = 0
        self._conformFiles = 0
        self._usedTime = 0
        self._surplusTime = 0

        self._pauseFlag = False
        self._pause = threading.Event()

        if self._pauseFlag == False:
            self._pause.set()

        self._statistic = threading.Thread( None, cb_statistic, None, ( self, mainDlg, params ) )
        self._searching = threading.Thread( None, cb_searching, None, ( self, mainDlg, params ) )
        self._statistic.start()
        self._searching.start()

        self._timer = wx.Timer(self) # 定时器
        self._timer.Start(KumquatRoot.Limit.QueryInterval) # 每隔100ms更新一次UI
        self._startTime = time.time() # 计算耗时用
        self.Bind( wx.EVT_TIMER, self.onTimer )

    def initUIs( self ):
        "初始化UI"

        wx.StaticText(
            self,
            label = u'进度显示:',
            pos = ( 10, 15 )
        )
        self._gauge = wx.Gauge(
            self,
            range = 100,
            pos = ( 10, 35 ),
            size = ( 390, 28 )
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

        self._gauge.Position = ( self._gauge.Position[0], self._btnExit.Position[1] )
        self._gauge.Size = ( self._gauge.Size[0], self._btnExit.Size[1] )

        #-------------------------状态标签-------------------------
        self._lblCurrentSearch = wx.StaticText(
            self,
            label = u'当前搜索:',
            pos = ( 12, 77 )
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
            pos = ( 10, 105 ),
            size = ( 475, 90 )
        )

        self.Bind( wx.EVT_BUTTON, self.onBtnControl, self._btnControl )
        self.Bind( wx.EVT_BUTTON, self.onBtnExit, self._btnExit )

        self.Bind( MainDlg.UpdateUiEvent.EVT_UPDATEUI, self.onUpdateUi )

    def setGaugeRange( self, range ):
        self._gauge.Range = range

    def setGaugeValue( self, value ):
        self._gauge.Value = value

    def setCurrentSearchLabel( self, content ):
        self._lblCurrentSearch.Label = u'正在搜索:' + content

    def setCurrentSearch( self, content ):
        with KumquatRoot.GlobalLock:
            try:
                self._currentSearch = unicode( str(content), KumquatRoot.LocalEncoding, u'ignore' )
            except UnicodeEncodeError, e:
                self._currentSearch = content
            except UnicodeDecodeError, e:
                self._currentSearch = u''

    def getCurrentSearch( self ):
        with KumquatRoot.GlobalLock:
            currentSearch = self._currentSearch
        return currentSearch

    currentSearch = property( getCurrentSearch, setCurrentSearch )

    def setTotalFilesLabel( self, count ):
        self._lblTotalFiles.Label = u'文件总计:' + unicode( str(count), KumquatRoot.LocalEncoding, u'ignore' )

    def setScanFilesLabel( self, count ):
        self._lblScanFiles.Label = u'已扫描数:' + unicode( str(count), KumquatRoot.LocalEncoding, u'ignore' )

    def setSurplusFilesLabel( self, count ):
        self._lblSurplusFiles.Label = u'剩余文件:' + unicode( str(count), KumquatRoot.LocalEncoding, u'ignore' )

    @staticmethod
    def formatTime( time ):
        sec = int(time)
        ms = int( ( round( time, 3 ) - sec ) * 1000 )
        hour = sec / 3600
        sec %= 3600
        minute = sec / 60
        sec %= 60
        result = u''
        if hour > 0:
            result += u'%d时' % hour
        if minute > 0:
            result += u'%d分' % minute
        if sec > 0 or not result:
            result += u'%d秒' % sec
        return result


    def setUsedTimeLabel( self, time ):
        self._lblUsedTime.Label = u'已用时长:' + SearchingDlg.formatTime(time)


    def setSurplusTimeLabel( self, time ):
        self._lblSurplusTime.Label = u'剩余时长:' + self.formatTime(time)


    def setConformFilesLabel( self, count ):
        self._lblConformFiles.Label = u'符合条件:' + unicode( str(count), KumquatRoot.LocalEncoding, u'ignore' )

    def getIsFinish( self ):
        with KumquatRoot.GlobalLock:
            isFinish = self._isFinish
        return isFinish

    def setIsFinish( self, value ):
        with KumquatRoot.GlobalLock:
            self._isFinish = value

        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_btnExit', 'Label', u'退出' if value else u'终止' ) )
        wx.PostEvent( self, MainDlg.UpdateUiEvent( '_btnControl', 'Enabled', not value ) )

        if self._isFinish:
            self._timer.Stop()
            wx.PostEvent( self, wx.TimerEvent( self._timer.Id, self._timer.Interval ) )

    isFinish = property( getIsFinish, setIsFinish, doc = "是否完成搜索" )

    def getIsAbort( self ):
        with KumquatRoot.GlobalLock:
            isAbort = self._isAbort
        return isAbort

    def setIsAbort( self, value ):
        with KumquatRoot.GlobalLock:
            self._isAbort = value

    isAbort = property( getIsAbort, setIsAbort, doc = "是否终止" )
    # 更新UI控件的自定义事件
    def onUpdateUi( self, evt ):
        ctrlName, propName, value = evt._args
        control = self.__getattribute__(ctrlName)
        control.__setattr__( propName, value )

    def onTimer( self, evt ):
        if evt.Id == self._timer.Id:
            thisTime = time.time()
            oneUsedTime = thisTime - self._startTime
            self._usedTime += oneUsedTime
            self._startTime = thisTime

            speed = self._scanFiles / self._usedTime # 速度

            self._surplusFiles = self._totalFiles - self._scanFiles # 剩余未搜索

            try:
                surplusTime = self._surplusFiles / speed
            except:
                surplusTime = -1

            self.setSurplusTimeLabel(surplusTime)

            self.setGaugeRange(self._totalFiles)
            self.setGaugeValue(self._scanFiles)
            self.setCurrentSearchLabel(self.currentSearch)
            self.setTotalFilesLabel(self._totalFiles)
            self.setScanFilesLabel(self._scanFiles)
            self.setSurplusFilesLabel(self._surplusFiles)
            self.setUsedTimeLabel(self._usedTime)
            self.setConformFilesLabel(self._conformFiles)

    def onBtnControl( self, evt ):
        if self._pauseFlag:# 当处于暂停中...
            self._pause.set() # 唤醒线程
            self._timer.Start(KumquatRoot.Limit.QueryInterval) # 开启定时器
            self._startTime = time.time() # 计算耗时用
            self._pauseFlag = False
            self._btnControl.Label = u'暂停'
        else:
            self._pause.clear() # 沉睡线程
            self._timer.Stop() # 停止定时器
            self._pauseFlag = True
            self._btnControl.Label = u'继续'

    def onBtnExit( self, evt ):
        if self.isFinish:
            self.EndModal(wx.ID_EXIT)
        else:
            self.isAbort = True
            self._pause.set() # 唤醒沉睡的线程，以便退出
            self._statistic.join()
            self._searching.join()
            self._timer.Stop() # 停止定时器
            self.EndModal(wx.ID_ABORT)


def test():
    app = wx.PySimpleApp()

    dlg = SearchingDlg( None, { 'RootPath':'F:\\' if os.path.sep == '\\' else '/', 'FilterExtList':[], 'IsUseMatchName':False, 'IsSearchWords':False }, None )
    if dlg.ShowModal() == wx.ID_ABORT:
        pass

if __name__ == '__main__':
    test()
