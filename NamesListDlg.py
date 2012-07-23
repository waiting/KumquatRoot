#-----------------------------------------------
#coding=utf8
#author=WT
#date=2012-07-22
#编辑名单对话框
#-----------------------------------------------

import wx

class NamesListDlg(wx.Dialog):
    def __init__(self, parent, edit_black = False ):
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            edit_black ? u'编辑%s名单' : u'',
            style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX | wx.SYSTEM_MENU,
            size = ( 320, 240 )
        )
        self.InitUIs()

    # 初始化UI #################################################################
    def InitUIs(self):
        # first line -----------------------------------------------------------
        label = wx.StaticText(
            self,
            -1,
            label = u'开始路径:',
            pos = ( 10, 21 )
        )
        rect = label.Rect
        self.TextCtrl_PathRoot = wx.TextCtrl(
            self,
            pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ),
            size = ( 320, 22 )
        )
        rect2 = self.TextCtrl_PathRoot.Rect
        self.Button_Browse = wx.Button(
            self,
            label = u'浏览...(&B)',
            pos = ( rect2[0] + rect2[2] + 6, rect2[1] - 1 )
        )
        # second line ----------------------------------------------------------
        label = wx.StaticText(
            self,
            label = u'匹配名字:',
            pos = ( rect[0], rect[1] + rect[3] + 16 )
        )
        rect = label.Rect
        self.TextCtrl_MatchName = wx.TextCtrl( self, pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ), size = ( 200, 22 ) )
        rect2 = self.TextCtrl_MatchName.Rect
        self.CheckBox_UseMatchName = wx.CheckBox(
            self,
            label = u'使用文件名匹配',
            pos = ( rect2[0] + rect2[2] + 10, rect2[1] + 5 )
        )
        # third line -----------------------------------------------------------
        label = wx.StaticText(
            self,
            label = u'包含词组:',
            pos = ( rect[0], rect[1] + rect[3] + 16 )
        )
        rect = label.Rect
        self.TextCtrl_IncludeWords = wx.TextCtrl( self, pos = ( rect[0] + rect[2] + 8, rect[1] - 3 ), size = ( 200, 22 ) )
        rect2 = self.TextCtrl_IncludeWords.Rect
        self.CheckBox_UseIncludeWords = wx.CheckBox(
            self,
            label = u'使用词组包含匹配',
            pos = ( rect2[0] + rect2[2] + 10, rect2[1] + 5 )
        )
        # forth line -----------------------------------------------------------
        self.RadioBox_UseMatchMode = wx.RadioBox(
            self,
            pos = ( rect2[0], rect2[1] + rect2[3] + 2 ),
            choices = [ u'普通精确匹配', u'正则表达式匹配' ]
        )
        rect2 = self.RadioBox_UseMatchMode.Rect

        # list report ----------------------------------------------------------
        label = wx.StaticText(
            self,
            label = u'搜索结果:',
            pos = ( rect[0], rect2[1] + rect2[3] + 10 )
        )
        rect = label.Rect
        self.ListCtrl_Results = wx.ListCtrl(
            self,
            pos = ( rect[0], rect[1] + rect[3] + 5 ),
            style = wx.LC_REPORT,
            size = ( self.ClientRect[2] - 2 * rect[0], self.ClientRect[3] - rect[0] - ( rect[1] + rect[3] + 5 ) )
        )
        rect2 = self.ListCtrl_Results.Rect
        self.ListCtrl_Results.InsertColumn( col = 0, heading = u'文件名', width = 100 )
        self.ListCtrl_Results.InsertColumn( col = 1, heading = u'文件路径', width = rect2[2] - 230 )
        self.ListCtrl_Results.InsertColumn( col = 2, heading = u'文件属性', width = rect2[2] - ( 100 + rect2[2] - 230 ) - 5 )
        # white/black list -----------------------------------------------------
        rect2 = self.Button_Browse.Rect
        groupbox = wx.StaticBox(
            self,
            label = u'过滤设置',
            pos = ( rect2[0] + rect2[2] + 5, rect2[1] - 5 ),
            size = ( self.ClientRect[2] - 10 - ( rect2[0] + rect2[2] + 5 ), self.ListCtrl_Results.Rect[1] - 10 - (rect2[1] - 5) )
        )

        button = self.Button_WhiteListSettings = wx.Button(
            self,
            label = u'编辑白名单',
        )
        button.Size = ( groupbox.Rect[2] - 30, button.Size[1] )
        button.Position = ( groupbox.Rect[0] + (groupbox.Rect[2] - button.Rect[2]) / 2, groupbox.Rect[1] + 25 )

        rect2 = button.Rect

        button = self.Button_BlackListSettings = wx.Button(
            self,
            label = u'编辑黑名单',
        )
        button.Size = ( groupbox.Rect[2] - 30, button.Size[1] )
        button.Position = ( groupbox.Rect[0] + (groupbox.Rect[2] - button.Rect[2]) / 2, rect2[1] + rect2[3] + 6 )

        self.RadioBox_UseListMode = wx.RadioBox(
            self,
            choices = [ u'使用黑名单', u'使用白名单' ],
            style = wx.RA_VERTICAL
        )
        self.RadioBox_UseListMode.Position = ( groupbox.Rect[0] + (groupbox.Rect[2] - self.RadioBox_UseListMode.Rect[2]) / 2, button.Position[1] + button.Size[1] )

        rect2 = self.RadioBox_UseMatchMode.Rect
        self.Button_Search = wx.Button(
            self,
            label = u'搜索(&S)',
            pos = ( rect2[0]+rect2[2] + 10, rect2[1] + 6 ),
            size = ( groupbox.Rect[0] - 10 - (rect2[0]+rect2[2] + 10), 37 )
        )

