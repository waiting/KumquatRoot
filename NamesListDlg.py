#-----------------------------------------------
#coding=utf8
#author=WT
#date=2012-07-22
#编辑名单对话框
#-----------------------------------------------

import wx

class NamesListDlg(wx.Dialog):
    def __init__( self, parent, isBlack = False ):
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            u'编辑%s名单' % ( u'黑' if isBlack else u'白' ),
            style = wx.DEFAULT_DIALOG_STYLE | wx.SYSTEM_MENU,
            size = ( 400, 300 )
        )
        self.initUIs()

    def initUIs(self):
        "初始化UI"
        lblTemp = wx.StaticText(
            self,
            label = u'每行一个不带点号的扩展名，支持正则。空行表示无扩展名文件。',
            pos = ( 10, 5 )
        )
        self._txtNamesList = wx.TextCtrl(
            self,
            pos = ( lblTemp.Position[0], lblTemp.Position[1] + lblTemp.Size[1] + 5 ),
            size = ( self.ClientSize[0] - 2 * lblTemp.Position[0], 210 ),
            style = wx.TE_MULTILINE
        )
        btnOK = wx.Button( self, label = u'确定(&O)', id = wx.ID_OK )
        btnOK.Position = ( self._txtNamesList.Position[0], self._txtNamesList.Position[1] + self._txtNamesList.Size[1] + 8 )
        btnCancel = wx.Button( self, label = u'取消(&C)', id = wx.ID_CANCEL )
        btnOK.Position = ( ( self.ClientSize[0] - ( btnOK.Size[0] + 20 + btnCancel.Size[0] ) ) / 2, btnOK.Position[1] )

        btnCancel.Position = ( btnOK.Position[0] + btnOK.Size[0] + 20, btnOK.Position[1] )

def test():
    app = wx.PySimpleApp()
    dlg = NamesListDlg( None, False )
    dlg.ShowModal()

if __name__ == '__main__':
    test()