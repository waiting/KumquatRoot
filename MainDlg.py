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
    import math
    import xml.dom.minidom
    import NamesListDlg
    import SearchingDlg
    import Feedback
    import AboutDlg
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
        self._resultItems =[]
        self._resultItemsCount = 0
        self._page = 1
        self._pageCount = 0

    def initUIs(self):
        "初始化UI"
        icons = wx.IconBundle()
        icons.AddIconFromFile( u'KumquatRoot.ico', wx.BITMAP_TYPE_ICO )
        self.SetIcons(icons)
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

        rect = box.Rect
        self._btnGoPage = wx.Button(
            self,
            label = u'Go',
            pos = ( rect[0] - 30 - 4, self._lblResults.Rect[1] - 2 ),
            size = ( 30, 20 )
        )
        rect = self._btnGoPage.Rect

        self._txtCurPage = wx.TextCtrl(
            self,
            pos = ( rect[0] - 46 - 4, rect[1] ),
            size = ( 46, 20 )
        )
        rect = self._txtCurPage.Rect

        self._btnNextPage = wx.Button(
            self,
            label = u'->',
            pos = ( rect[0] - 30 - 4, rect[1] ),
            size = ( 30, 20 )
        )
        rect = self._btnNextPage.Rect

        self._btnPrevPage = wx.Button(
            self,
            label = u'<-',
            pos = ( rect[0] -30 - 4, rect[1] ),
            size = ( 30, 20 )
        )

        self.Bind( wx.EVT_BUTTON, self.onBtnBrowse, self._btnBrowse )
        self.Bind( wx.EVT_BUTTON, self.onBtnBlackListSettings, self._btnBlackListSettings )
        self.Bind( wx.EVT_BUTTON, self.onBtnWhiteListSettings, self._btnWhiteListSettings )
        self.Bind( wx.EVT_BUTTON, self.onBtnSearch, self._btnSearch )

        self.Bind( wx.EVT_BUTTON, self.onBtnPrevPage, self._btnPrevPage )
        self.Bind( wx.EVT_BUTTON, self.onBtnNextPage, self._btnNextPage )
        self.Bind( wx.EVT_BUTTON, self.onBtnGoPage, self._btnGoPage )

        self.Bind( wx.EVT_CONTEXT_MENU, self.onContextMenu )
        #self.Bind( wx.EVT_COMMAND_RANGE() )
        #wx.EVT_COMMAND_RANGE( self, 1001, 1003, wx.wxEVT_CO )
        self._popMenu = wx.Menu()
        self._popMenu.Append( self.MENU_FEEDBACK, u'反馈...' )
        self._popMenu.Append( self.MENU_ABOUT, u'关于' )
        self._popMenu.Append( self.MENU_HELP, u'帮助' )
        self.Bind( wx.EVT_MENU_RANGE, self.onPopupMenu, id = self.MENU_FEEDBACK, id2 = self.MENU_HELP )

    MENU_FEEDBACK = 1001
    MENU_ABOUT = 1002
    MENU_HELP = 1003

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

    def addResult( self, fileName, filePath, fileAttr ):
        lstctl = self._lstctlResults
        index = lstctl.ItemCount
        lstctl.InsertStringItem( index, fileName )
        lstctl.SetStringItem( index, 1, filePath )
        lstctl.SetStringItem( index, 2, fileAttr )

    def clearResults( self ):
        self._lstctlResults.DeleteAllItems()

    def setResultsLabel( self, count, pageCount ):
        self._lblResults.Label = u'搜索结果(%d, 共%d页):' % ( count, pageCount )

    def updateResultsPage( self, page ):
        if self._pageCount < 1: return
        if page < 1:
            page = 1
        elif page > self._pageCount:
            page = self._pageCount

        self._page = page
        self._txtCurPage.Value = unicode(page)

        if self._page == self._pageCount:
            start = ( self._page - 1 ) * KumquatRoot.Limit.SplitPage
            end = self._resultItemsCount
        else:
            start = ( self._page - 1 ) * KumquatRoot.Limit.SplitPage
            end = start + KumquatRoot.Limit.SplitPage

        self.clearResults()

        for i in xrange( start, end ):
            fileName, filePath, fileAttr = self._resultItems[i]
            self.addResult( fileName, filePath, fileAttr )

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
        params['RootPath'] = params['RootPath'] if params['RootPath'] else unicode( os.path.abspath(os.path.curdir), KumquatRoot.LocalEncoding, u'ignore' )

        #清空结果列表
        self.clearResults()
        self._resultItems =[]
        self._resultItemsCount = 0

        #打开SearchingDlg，进行搜索
        searchDlg = SearchingDlg.SearchingDlg( self, params, self )
        if searchDlg.ShowModal() == wx.ID_ABORT:
            wx.MessageBox( u'搜索终止！', u'搜索状态' )
        else:
            pass

        self._resultItemsCount = len(self._resultItems) # 取得符合条件的结果数
        self._pageCount = int( math.ceil( float(self._resultItemsCount) / KumquatRoot.Limit.SplitPage ) ) # 页数

        self.setResultsLabel( self._resultItemsCount, self._pageCount )

        self._page = 1
        self._txtCurPage.Value = unicode(self._page)
        self.updateResultsPage(self._page) # 更新结果页

    def onBtnPrevPage( self, evt ):
        self.updateResultsPage( self._page - 1 )
    def onBtnNextPage( self, evt ):
        self.updateResultsPage( self._page + 1 )
    def onBtnGoPage( self, evt ):
        try:
            page = int(self._txtCurPage.Value)
        except:
            page = 1
        self.updateResultsPage(page)

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

    def onContextMenu( self, evt ):
        self.PopupMenu(self._popMenu)

    def onPopupMenu( self, evt ):
        if evt.Id == self.MENU_FEEDBACK:
            dlg = Feedback.Feedback()
        elif evt.Id == self.MENU_ABOUT:
            dlg = AboutDlg.AboutDlg()
        elif evt.Id == self.MENU_HELP:
            pass

def test():
    app = wx.PySimpleApp()
    dlg = MainDlg()
    dlg.ShowModal()


if __name__ == '__main__':
    test()