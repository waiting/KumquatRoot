#-----------------------------------------------
#coding=utf8
#author=WT
#date=2012-07-22
#主界面对话框
#-----------------------------------------------

import os
import wx
from xml.dom import minidom
from NamesListDlg import NamesListDlg

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
        self._txtMatchName = wx.TextCtrl( self, pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ), size = ( 200, 22 ) )
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
        lblTest = wx.StaticText(
            self,
            label = u'搜索结果:',
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
        self._lstctlResults.InsertColumn( col = 2, heading = u'文件属性', width = rect2[2] - ( 100 + rect2[2] - 230 ) - 5 )
        # white/black list -----------------------------------------------------
        rect2 = self._btnBrowse.Rect
        box = wx.StaticBox(
            self,
            label = u'过滤设置',
            pos = ( rect2[0] + rect2[2] + 5, rect2[1] - 5 ),
            size = ( self.ClientRect[2] - 10 - ( rect2[0] + rect2[2] + 5 ), self._lstctlResults.Rect[1] - 10 - (rect2[1] - 5) )
        )

        btnTemp = self._btnWhiteListSettings = wx.Button(
            self,
            label = u'编辑白名单',
        )
        btnTemp.Size = ( box.Rect[2] - 30, btnTemp.Size[1] )
        btnTemp.Position = ( box.Rect[0] + (box.Rect[2] - btnTemp.Rect[2]) / 2, box.Rect[1] + 25 )

        rect2 = btnTemp.Rect

        btnTemp = self._btnBlackListSettings = wx.Button(
            self,
            label = u'编辑黑名单',
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

    def loadNamesList( self, isBlack ):
        u'加载名单设置'
        try:
            settingsFile = open(u'settings.xml')
        except IOError, e:
            settingsFile = open( u'settings.xml', 'w+' )
            settingsFile.write(u'<settings></settings>')
            settingsFile.seek( 0, os.SEEK_SET )

        doc = minidom.parse(settingsFile)
        List = doc.documentElement.getElementsByTagName(u'blacklist' if isBlack else u'whitelist')
        if List:
            List = List[0]
            patterns = List.getElementsByTagName(u'pattern')
            return [pattern.firstChild.nodeValue for pattern in patterns]
        else:
            return []

    def writeNamesList( self, isBlack, patterns ):
        settingsFile = open( u'settings.xml', 'r+' )
        doc = minidom.parse(settingsFile)
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

        settingsFile.write( doc.toxml('utf-8') )


    # 事件响应 -----------------------------------------------------------------
    def onBtnBrowse( self, evt ):
        dirDlg = wx.DirDialog( self, message = u'请选择一个待搜索目录' )
        if dirDlg.ShowModal() == wx.ID_OK:
            self._txtPathRoot.Label = dirDlg.Path

    def onBtnBlackListSettings( self, evt ):
        dlg = NamesListDlg( self, True )
        dlg._txtNamesList.Label = os.linesep.join( self.loadNamesList(True) )
        if dlg.ShowModal() == wx.ID_OK:
            self.writeNamesList( True, dlg._txtNamesList.Label.splitlines() )

    def onBtnWhiteListSettings( self, evt ):
        dlg = NamesListDlg( self, False )
        dlg._txtNamesList.Label = os.linesep.join( self.loadNamesList(False) )
        if dlg.ShowModal() == wx.ID_OK:
            self.writeNamesList( False, dlg._txtNamesList.Label.splitlines() )


def test():
    app = wx.PySimpleApp()
    dlg = MainDlg()
    dlg.ShowModal()


if __name__ == '__main__':
    test()