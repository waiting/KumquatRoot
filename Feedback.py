#coding:utf-8

#-------------------------------------------------------------------------------
# Name:        Feedback.py
# Purpose:
#
# Author:      Mr.Wid
#
# Created:     29-07-2012
# Copyright:   (c) Mr.Wid 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx

class Feedback(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(
            self,
            parent=None,
            title=u'意见反馈',
            size=(300,400)
        )
        #标签控件---------------------
        self.lblLabel = [u'姓名:', u'E-mail:', u'内容:']
        self.y = 30
        for lbl in self.lblLabel:
            wx.StaticText(
                self,
                label = lbl ,
                pos=(30,self.y)
            )
            self.y += 40

        #文本框控件-------------------
        self.txtName = ['txtName', 'txtEmail']
        self.y = 28
        for txt in self.txtName:
            txt = wx.TextCtrl(
                self,
                pos = (80, self.y),
                size=(180,20)
            )
            self.y += 40

        groupBox = wx.StaticBox(
            self,
            label = u'内容(必填)',
            pos = (20, self.y),
            size = (255, 200)
        )
        self._txtContents = wx.TextCtrl(
            self,
            pos=(30,self.y + 20),
            size = (235, 170),
            style=wx.TE_MULTILINE
        )

        #按钮控件----------------------
        self._btnSub = wx.Button(
            self,
            label = u"提交",
            pos = (85, 320),
            size = (50, 30)
        )
        self._btnCancel = wx.Button(
            self,
            label = u"取消",
            pos = (155, 320),
            size = (50, 30)
        )

def test():
    app=wx.PySimpleApp()
    feedback=Feedback()
    feedback.ShowModal()

if __name__ == '__main__':
    test()