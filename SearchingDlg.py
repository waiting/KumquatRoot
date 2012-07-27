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
    import thread
    import Queue
    import os
    import re
    import KumquatRoot
    from MainDlg import MainDlg
except ImportError:
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
        # 进行搜索
        if params and params['IsSearchWords']:
            pass
        KumquatRoot.GlobalLock.acquire()
        searchDlg.setCurrentSearch(filePath)
        searchDlg._scanFiles += 1
        searchDlg._surplusFiles = searchDlg._totalFiles - searchDlg._scanFiles
        searchDlg.setScanFiles(searchDlg._scanFiles)
        searchDlg.setSurplusFiles(searchDlg._surplusFiles)
        KumquatRoot.GlobalLock.release()

        if mainDlg:
            mainDlg.addResult( os.path.basename(filePath), os.path.dirname(filePath), u'None' )

        KumquatRoot.GlobalLock.acquire()
        isAbort = searchDlg._isAbort
        KumquatRoot.GlobalLock.release()
        if isAbort:
            break


# 统计线程
def cb_statistic( *args, **kwargs ):
    "cb_statistic( SearchingDlg searchDlg, MainDlg mainDlg, params )"
    searchDlg, mainDlg, params = args
    queue = searchDlg._queue
    if params:
        for rootPath, dirNames, fileNames in os.walk(params['RootPath']):
            KumquatRoot.GlobalLock.acquire()
            isAbort = searchDlg._isAbort
            KumquatRoot.GlobalLock.release()
            if isAbort:
                break
            for fileName in fileNames:
                # 判断根目录的情况
                if re.match( '^\\w:\\\\$', rootPath ):
                    filePath = rootPath + fileName
                else:
                    filePath = rootPath + os.path.sep + fileName
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
                KumquatRoot.GlobalLock.acquire()
                searchDlg._totalFiles += 1
                searchDlg.setTotalFiles(searchDlg._totalFiles)
                KumquatRoot.GlobalLock.release()

                queue.put(filePath)

                KumquatRoot.GlobalLock.acquire()
                isAbort = searchDlg._isAbort
                KumquatRoot.GlobalLock.release()
                if isAbort:
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
<<<<<<< HEAD
        self.initUIs()

        self._params = params # 主界面上的各项参数
        self._mainDlg = mainDlg # 控制主界面
        self._queue = Queue.Queue(KumquatRoot.QueueCount) # 待搜索文件队列

        self.isFinish = False
        self._isAbort = False
        self._totalFiles = 0
        self._scanFiles = 0
        self._surplusFiles = 0
        self._conformFiles = 0

        thread.start_new_thread( cb_statistic, ( self, mainDlg, params ) )
        thread.start_new_thread( cb_searching, ( self, mainDlg, params ) )


    def initUIs( self ):
        "初始化UI"
        self._gauge = wx.Gauge(
=======
        self.createProgressBar()    #创建进度条

    #------------------------创建进度条-----------------------------------------
    def createProgressBar(self):
        self.gauge = wx.Gauge(self, -1, 100, (25, 25), (370, 30))
        self.gauge.SetBezelFace(2)
        self.gauge.SetShadowWidth(2)

        self.createStopPauseButton()    #创建终止、暂停按钮
        self.createStatusLabel()    #创建任务状态标签

    #------------------------创建终止、暂停按钮-------------------------
    def createStopPauseButton(self):
        self.btnStopSearchButton = wx.Button(
>>>>>>> origin/master
            self,
            range = 100,
            pos = ( 25, 25 ),
            size = ( 370, 30 )
        )
<<<<<<< HEAD
        self._gauge.BezelFace = 2    #在多数平台上都无效果
        self._gauge.ShadowWidth = 2  #在多数平台上都无效果
        self._gauge.Range = 100

        self._btnControl = wx.Button(
            self,
=======
        self.Bind(wx.EVT_BUTTON, self.clickStopButton, self.btnStopSearchButton)

        self.btnPauseSearchButton = wx.Button(
            self ,
>>>>>>> origin/master
            label = u'暂停',
            pos = ( 410, 10 )
        )
        self.Bind( wx.EVT_BUTTON, self.onBtnControl, self._btnControl )

        self._btnExit = wx.Button(
            self,
            label = u'终止',
            pos = ( 410, 40 )
        )
<<<<<<< HEAD
        self.Bind( wx.EVT_BUTTON, self.onBtnExit, self._btnExit )

        #-------------------------状态标签-------------------------
        self._lblCurrentSearch = wx.StaticText(
=======
        self.Bind(wx.EVT_BUTTON, self.clickPauseButton, self.btnPauseSearchButton)

    #-------------------------文件状态标签-------------------------
    def createStatusLabel(self):
        self.lblCurrentSearchStatusLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'正在搜索:',
            pos = ( 25, 85 )
        )

<<<<<<< HEAD
        self._lblTotalFiles = wx.StaticText(
=======
        self.lblCurrentTotalFileLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'文件总计:',
            pos = ( 30, 130 )
        )
<<<<<<< HEAD
        self._lblScanFiles = wx.StaticText(
=======
        self.lblCurrentPassedFileLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'已扫描数:',
            pos = ( 180, 130 )
        )
<<<<<<< HEAD
        self._lblSurplusFiles = wx.StaticText(
=======
        self.lblCurrentLastFileLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'剩余文件:',
            pos = ( 330, 130 )
        )

<<<<<<< HEAD
        self._lblUsedTime = wx.StaticText(
=======
        #-------------------------时间状态标签-------------------------
        self.lblCurrentUsedTimeStatusLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'已用时长:',
            pos = ( 30, 160 )
        )
<<<<<<< HEAD
        self._lblSurplusTime = wx.StaticText(
=======
        self.lblCurrentLastTimeStatusLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'剩余时长:',
            pos = (180, 160)
        )
<<<<<<< HEAD
        self._lblConformFiles = wx.StaticText(
=======
        self.lblCurrentConformStatusLabel = wx.StaticText(
>>>>>>> origin/master
            self,
            label = u'符合条件:',
            pos = ( 330, 160 )
        )

        boxGroupBox = wx.StaticBox(
            self,
            label = u'任务状态',
            pos = (15, 105),
            size = (465, 90)
        )

<<<<<<< HEAD
    def setGaugeRange( self, range ):
        "设置'进度条'范围"
        self._gauge.Range = range

    def setGaugeValue( self, value ):
        "设置'进度条'值"
        self._gauge.Value = value

    def setCurrentSearch( self, content = None ):
        "设置'正在搜索'标签内容"
        try:
            self._lblCurrentSearch.Label = u'正在搜索:' + unicode( str(content), KumquatRoot.LocalEncoding )
        except UnicodeEncodeError, e:
            #print 'EncodeError:', content
            self._lblCurrentSearch.Label = u'正在搜索:' + content
            pass
        except UnicodeDecodeError, e:
            print 'DecodeError:', content
            pass

    def setTotalFiles( self, number = None ):
        "设置'文件总计'标签内容"
        self._lblTotalFiles.Label = u'文件总计:' + unicode(number)

    def setScanFiles( self, number = None ):
        "设置'已扫面数'标签内容"
        self._lblScanFiles.Label = u'已扫描数:' + unicode(number)

    def setSurplusFiles( self, number = None ):
        "设置'剩余文件'标签内容"
        self._lblSurplusFiles.Label = u'剩余文件:' + unicode(number)

    def setUsedTime( self, number = None ):
        "设置'已用时长'标签内容"
        self._lblUsedTime.Label = u'已用时长:' + unicode(number)

    def setSurplusTime( self, number = None ):
        "设置'剩余时长'标签内容"
        self._lblSurplusTime.Label = u'剩余时长:' + unicode(number)

    def setConformFiles( self, number = None ):
        "设置'符合条件'标签内容"
        self._lblConformFiles.Label = u'符合条件:' + unicode(number)

    def getIsFinish( self ):
        return self._isFinish
    def setIsFinish( self, value ):
        self._isFinish = value
        self._btnExit.Label = u'退出' if value else u'终止'

    isFinish = property( getIsFinish, setIsFinish, doc = "是否完成搜索" )

    def onBtnControl( self, evt ):

        print u'暂停'

    def onBtnExit( self, evt ):
        if self.isFinish:
            self.EndModal(wx.ID_EXIT)
        else:
            self._isAbort = True
            self.EndModal(wx.ID_ABORT)
=======
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
        self.lblCurrentSearchStatusLabel.SetLabel(u'正在搜索:' + str(content))

    #设置"文件总计"标签内容
    def setTotalFileNumber(self, number = None):
        '''
        #方法名称:setTotalFileNumber
        原型:setTotalFileNumber(self, string number)
        调用示例:SearchingDlg.setTotalFileNumber(u'12345')
        '''
        self.lblCurrentTotalFileLabel.SetLabel(u'文件总计:' + str(number))

    #设置"已扫面数"标签内容
    def setSearchedFileNumber(self, number = None):
        '''
        #方法名称:setSearchedFileNumber
        原型:setSearchedFileNumber(self, string number)
        调用示例:SearchingDlg.setSearchedFileNumber(u'12345')
        '''
        self.lblCurrentPassedFileLabel.SetLabel(u'已扫描数:' + str(number))

    #设置"剩余文件"标签内容
    def setSurplusFileNumber(self, number = None):
        '''
        #方法名称:setSurplusFileNumber
        原型:setSurplusFileNumber(self, string number)
        调用示例:SearchingDlg.setSurplusFileNumber(u'12345')
        '''
        self.lblCurrentLastFileLabel.SetLabel(u'剩余文件:' + str(number))

    #设置"已用时长"标签内容
    def setUsedTime(self, number = None):
        '''
        #方法名称:setUsedTime
        原型:setUsedTime(self, string number)
        调用示例:SearchingDlg.setUsedTime(u'24秒')
        '''
        self.lblCurrentUsedTimeStatusLabel.SetLabel(u'已用时长:' + str(number))

    #设置"剩余时长"标签内容
    def setSurplusTime(self, number = None):
        '''
        #方法名称:setSurplusTime
        原型:setSurplusTime(self, string number)
        调用示例:SearchingDlg.setSurplusTime(u'12345')
        '''
        self.lblCurrentLastTimeStatusLabel.SetLabel(u'剩余时长:' + str(number))

    #设置"符合条件"标签内容
    def setConformNumber(self, number = None):
        '''
        #方法名称:setConformNumber
        原型:setConformNumber(self, string number)
        调用示例:SearchingDlg.setConformNumber(u'12345')
        '''
        self.lblCurrentConformStatusLabel.SetLabel(u'符合条件:' + str(number))
    #-------------------------任务状态方法结束-------------------

    #-------------------------按钮方法开始-----------------------
    '''
    从'按钮方法开始'到'按钮方法结束'部分为面板上'暂停'、'终止'两个按钮的方法
    '''

    def clickPauseButton(self, event):  #点击"暂停"按钮时引发暂停异常
        raise PressPauseButton

    def clickStopButton(self, event):   #点击"终止"按钮时引发终止异常
        raise PressStopButton
    #-------------------------按钮方法结束-----------------------
>>>>>>> origin/master


def test():
    app = wx.PySimpleApp()
    dlg = SearchingDlg( None, { 'RootPath':'F:\\', 'FilterExtList':[], 'IsUseMatchName':False, 'IsSearchWords':True }, None )
    if dlg.ShowModal() == wx.ID_ABORT:
        pass

if __name__ == '__main__':
    test()
