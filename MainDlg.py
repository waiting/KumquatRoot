#-----------------------------------------------
# coding: utf8
# author: WT
# date: 2012-07-22
# desc: 主界面对话框
#-----------------------------------------------

try:
    import os
    import wx
    import KumquatRoot
    import xml.dom.minidom
    import NamesListDlg
    import SearchingDlg
except ImportError, e:
    print e


class UpdateUiEvent(wx.PyCommandEvent):
    EVT_UpdateUiType = wx.NewEventType()
    EVT_UPDATEUI = wx.PyEventBinder(EVT_UpdateUiType)
    def __init__( self, *args ):
        wx.PyCommandEvent.__init__( self, self.EVT_UpdateUiType )
        self._args = args



class MainDlg(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(
            self,
            None,
            -1,
            u'橘根文件搜索',
            style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX | wx.SYSTEM_MENU,
            size = ( 640, 480 )
        )
        self.initUIs()

    def initUIs(self):
        "初始化UI"
        # first line -----------------------------------------------------------
        lblTest = wx.StaticText(
            self,
            -1,
            label = u'开始路径:',
            pos = ( 10, 21 )
        )
        rect = lblTest.Rect
        self._txtPathRoot = wx.TextCtrl(
            self,
            pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ),
            size = ( 320, 22 )
        )
        rect2 = self._txtPathRoot.Rect
        self._btnBrowse = wx.Button(
            self,
            label = u'浏览...(&B)',
            pos = ( rect2[0] + rect2[2] + 6, rect2[1] - 1 )
        )
        # second line ----------------------------------------------------------
        lblTest = wx.StaticText(
            self,
            label = u'匹配名字:',
            pos = ( rect[0], rect[1] + rect[3] + 16 )
        )
        rect = lblTest.Rect
        self._txtMatchName = wx.TextCtrl(
            self,
            pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ),
            size = ( 200, 22 )
        )
        rect2 = self._txtMatchName.Rect
        self._chkUseMatchName = wx.CheckBox(
            self,
            label = u'使用文件名匹配',
            pos = ( rect2[0] + rect2[2] + 10, rect2[1] + 5 )
        )
        # third line -----------------------------------------------------------
        lblTest = wx.StaticText(
            self,
            label = u'包含词组:',
            pos = ( rect[0], rect[1] + rect[3] + 16 )
        )
        rect = lblTest.Rect
        self._txtSearchWords = wx.TextCtrl( self, pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ), size = ( 200, 22 ) )
        rect2 = self._txtSearchWords.Rect
        self._chkSearchWords = wx.CheckBox(
            self,
            label = u'使用词组包含匹配',
            pos = ( rect2[0] + rect2[2] + 10, rect2[1] + 5 )
        )
        # forth line -----------------------------------------------------------
        self._rdoboxUseMatchMode = wx.RadioBox(
            self,
            pos = ( rect2[0], rect2[1] + rect2[3] + 2 ),
            choices = [ u'普通精确匹配', u'正则表达式匹配' ]
        )
        rect2 = self._rdoboxUseMatchMode.Rect

        # list report ----------------------------------------------------------
        self._lblResults = lblTest = wx.StaticText(
            self,
            label = u'搜索结果(0):',
            pos = ( rect[0], rect2[1] + rect2[3] + 10 )
        )
        rect = lblTest.Rect
        self._lstctlResults = wx.ListCtrl(
            self,
            pos = ( rect[0], rect[1] + rect[3] + 5 ),
            style = wx.LC_REPORT,
            size = ( self.ClientRect[2] - 2 * rect[0], self.ClientRect[3] - rect[0] - ( rect[1] + rect[3] + 5 ) )
        )
        rect2 = self._lstctlResults.Rect
        self._lstctlResults.InsertColumn( col = 0, heading = u'文件名', width = 100 )
        self._lstctlResults.InsertColumn( col = 1, heading = u'文件路径', width = rect2[2] - 230 )
        self._lstctlResults.InsertColumn( col = 2, heading = u'文件属性', width = rect2[2] - ( 100 + rect2[2] - 230 ) - 22 )
        # white/black list -----------------------------------------------------
        rect2 = self._btnBrowse.Rect
        box = wx.StaticBox(
            self,
            label = u'过滤设置',
            pos = ( rect2[0] + rect2[2] + 5, rect2[1] - 5 ),
            size = ( self.ClientRect[2] - 10 - ( rect2[0] + rect2[2] + 5 ), self._lstctlResults.Rect[1] - 10 - (rect2[1] - 5) )
        )

        btnTemp = self._btnBlackListSettings = wx.Button(
            self,
            label = u'编辑黑名单',
        )
        btnTemp.Size = ( box.Rect[2] - 30, btnTemp.Size[1] )
        btnTemp.Position = ( box.Rect[0] + (box.Rect[2] - btnTemp.Rect[2]) / 2, box.Rect[1] + 25 )

        rect2 = btnTemp.Rect

        btnTemp = self._btnWhiteListSettings = wx.Button(
            self,
            label = u'编辑白名单',
        )
        btnTemp.Size = ( box.Rect[2] - 30, btnTemp.Size[1] )
        btnTemp.Position = ( box.Rect[0] + (box.Rect[2] - btnTemp.Rect[2]) / 2, rect2[1] + rect2[3] + 6 )

        self._rdoboxUseListMode = wx.RadioBox(
            self,
            choices = [ u'使用黑名单', u'使用白名单' ],
            style = wx.RA_VERTICAL
        )
        self._rdoboxUseListMode.Position = ( box.Rect[0] + (box.Rect[2] - self._rdoboxUseListMode.Rect[2]) / 2, btnTemp.Position[1] + btnTemp.Size[1] )

        rect2 = self._rdoboxUseMatchMode.Rect
        self._btnSearch = wx.Button(
            self,
            label = u'搜索(&S)',
            pos = ( rect2[0]+rect2[2] + 10, rect2[1] + 6 ),
            size = ( box.Rect[0] - 10 - (rect2[0]+rect2[2] + 10), 37 )
        )

        self.Bind( wx.EVT_BUTTON, self.onBtnBrowse, self._btnBrowse )
        self.Bind( wx.EVT_BUTTON, self.onBtnBlackListSettings, self._btnBlackListSettings )
        self.Bind( wx.EVT_BUTTON, self.onBtnWhiteListSettings, self._btnWhiteListSettings )
        self.Bind( wx.EVT_BUTTON, self.onBtnSearch, self._btnSearch )

        self.Bind( UpdateUiEvent.EVT_UPDATEUI, self.onUpdateUi )

    def loadNamesList( self, isBlack ):
        '加载名单设置'
        try:
            settingsFile = open(u'settings.xml')
        except IOError, e:
            settingsFile = open( u'settings.xml', u'w+' )
            settingsFile.write(u'<settings></settings>')
            settingsFile.seek( 0, os.SEEK_SET )

        doc = xml.dom.minidom.parse(settingsFile)
        List = doc.documentElement.getElementsByTagName(u'blacklist' if isBlack else u'whitelist')
        if List:
            List = List[0]
            patterns = List.getElementsByTagName(u'pattern')
            pats = []
            for pat in patterns:
                pats.append( pat.firstChild.nodeValue if pat.firstChild else u'' )
            #return [pattern.firstChild.nodeValue for pattern in patterns]
            return pats
        else:
            return []

    def writeNamesList( self, isBlack, patterns ):
        settingsFile = open( u'settings.xml', u'r+' )
        doc = xml.dom.minidom.parse(settingsFile)
        settingsFile.truncate(0)
        settingsFile.seek( 0, os.SEEK_SET )
        newList = doc.createElement(u'blacklist' if isBlack else u'whitelist')
        oldList = doc.documentElement.getElementsByTagName(u'blacklist' if isBlack else u'whitelist')
        if oldList:
            oldList = oldList[0]
            doc.documentElement.replaceChild( newList, oldList )
        else:
            doc.documentElement.appendChild(newList)

        for pattern in patterns:
            patNode = doc.createElement(u'pattern')
            newList.appendChild(patNode)
            patText = doc.createTextNode(pattern)
            patNode.appendChild(patText)

        settingsFile.write( doc.toxml(u'utf-8') )

    def notifyAddResult( self, fileName, filePath, fileAttr ):
        wx.PostEvent( self, UpdateUiEvent( '_lstctlResults', '', ( fileName, filePath, fileAttr ) ) )
        KumquatRoot.do_events()

    def addResult( self, fileName, filePath, fileAttr ):
        lstctl = self._lstctlResults
        index = lstctl.ItemCount
        lstctl.InsertStringItem( index, fileName )
        lstctl.SetStringItem( index, 1, filePath )
        lstctl.SetStringItem( index, 2, fileAttr )
        self.ResultsLabel = lstctl.ItemCount

    def clearResults( self ):
        self._lstctlResults.DeleteAllItems()
        self.ResultsLabel = 0

    def setResultsLabel( self, count = 0 ):
        self._lblResults.Label = u'搜索结果(%d):' % count

    ResultsLabel = property( fset = setResultsLabel )
    # 事件响应 -----------------------------------------------------------------
    def onUpdateUi( self, evt ):
        ctrlName, prop, value = evt._args
        control = self.__getattribute__(ctrlName)
        if control == self._lstctlResults:
            fileName, filePath, fileAttr = value
            self.addResult( fileName, filePath, fileAttr )
        else:
            control.__setattr__( prop, value )

    def onBtnSearch( self, evt ):
        "搜索按钮响应"
        #取得变量信息
        params = {}
        params['UseMatchMode'] = self._rdoboxUseMatchMode.Selection # 0:精确匹配, 1:正则表达式
        params['UseListMode'] = self._rdoboxUseListMode.Selection # 0:黑名单, 1:白名单
        params['IsUseMatchName'] = self._chkUseMatchName.Value
        params['MatchName'] = self._txtMatchName.Value
        params['IsSearchWords'] = self._chkSearchWords.Value
        params['SearchWords'] = self._txtSearchWords.Value
        params['FilterExtList'] = self.loadNamesList( params['UseListMode'] == 0 ) # 加载过滤名单
        params['RootPath'] = self._txtPathRoot.Value # 搜索路径
        params['RootPath'] = params['RootPath'] if params['RootPath'] else os.path.abspath(os.path.curdir)

        #清空结果列表
        self.clearResults()
        #打开SearchingDlg，进行搜索
        searchDlg = SearchingDlg.SearchingDlg( self, params, self )
        if searchDlg.ShowModal() == wx.ID_ABORT:
            wx.MessageBox( u'搜索终止！', u'搜索状态' )
        else:
            pass #wx.MessageBox(u'搜索完毕！', u'搜索状态' )



    def onBtnBrowse( self, evt ):
        dirDlg = wx.DirDialog( self, message = u'请选择一个待搜索目录' )
        if dirDlg.ShowModal() == wx.ID_OK:
            self._txtPathRoot.Value = dirDlg.Path

    def onBtnBlackListSettings( self, evt ):
        dlg = NamesListDlg.NamesListDlg( self, True )
        items = self.loadNamesList(True)
        dlg._txtNamesList.Value = os.linesep.join(items) + os.linesep if len(items) else u''
        if dlg.ShowModal() == wx.ID_OK:
            self.writeNamesList( True, dlg._txtNamesList.Value.splitlines() )

    def onBtnWhiteListSettings( self, evt ):
        dlg = NamesListDlg.NamesListDlg( self, False )
        items = self.loadNamesList(False)
        dlg._txtNamesList.Value = os.linesep.join(items) + os.linesep if len(items) else u''
        if dlg.ShowModal() == wx.ID_OK:
            self.writeNamesList( False, dlg._txtNamesList.Value.splitlines() )


def test():
    app = wx.PySimpleApp()
    dlg = MainDlg()
    dlg.ShowModal()


if __name__ == '__main__':
    test()