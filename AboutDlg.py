#!/usr/bin/python
#coding:utf-8

#-------------------------------------------------------------------------------
# Name:        AboutDlg.py
# Purpose:
#
# Author:      Mr.Wid
#
# Created:     26-07-2012
# Copyright:   (c) Mr.Wid 2012
# Licence:
#-------------------------------------------------------------------------------

import wx

class AboutDlg(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent = parent,
            title = u'关于',
            size = (400, 500)
    )
        self.lblImage()
        self.boxInf()
    #-----------------------创建控件------------------------
    #--------标签--------
    def lblImage(self):
        _img = wx.Image('KumquatRoot_font.png', wx.BITMAP_TYPE_ANY)
        _width = _img.GetWidth()
        kumrootImage = wx.StaticBitmap(
            self,
            -1,
            wx.BitmapFromImage(_img),
            pos = ((400-_width)/2-5, 20)
        )

    def boxInf(self):
        self._groupBox = wx.StaticBox(
            self,
            label = u'信息',
            pos = (15, 110),
            size = (365, 130)
        )
        self._lblVersion = wx.StaticText(
            self,
            label = u'版本:    1.0.0',
            pos = (30, 140 )
        )
        self._lblAuthor = wx.StaticText(
            self,
            label = u'作者:    WT、Mr.Wid',
            pos = (30, 160 )
        )
        self._lblWTEmail = wx.StaticText(
            self,
            label = u'E-mail:  zth555@qq.com (WT)\n'+' '*11+\
                    u'mr_wid@163.com (Mr.Wid)',
            pos = (30, 180 )
        )
        self._lblWebsite = wx.StaticText(
            self,
            label = u'网址:    ',
            pos = (30, 215 )
        )
        self._lblLinkx86 = wx.HyperlinkCtrl(
            self,
            id = -1,
            label = u'http://www.x86pro.com',
            url = u'http://www.x86pro.com',
            pos = (75, 215)
            )

        #-------选项卡-------
        self._noteBook = wx.Notebook(
            self,
            -1,
            pos = (20, 260),
            size=(355, 170),
            style = wx.NB_FIXEDWIDTH)
        _txtIntroduction = wx.TextCtrl(
            self._noteBook,
            -1,
            style = wx.MULTIPLE|wx.TE_READONLY
        )
        _txtLicense = wx.TextCtrl(
            self._noteBook,
            -1,
            style = wx.MULTIPLE|wx.TE_READONLY
        )
        _txtOthers = wx.TextCtrl(self._noteBook,
            -1,
            style = wx.MULTIPLE|wx.TE_READONLY
        )

        self._noteBook.AddPage(_txtIntroduction, u"介绍")
        self._noteBook.AddPage(_txtLicense, u"协议")
        self._noteBook.AddPage(_txtOthers, u"其他")

        #------确定按钮------
        self._btnOK = wx.Button(
            self,
            label = u"确定",
            pos = (170, 435),
            size = (60, 30)
        )
def test():
    app = wx.PySimpleApp()
    aboutDlg = AboutDlg(None)
    aboutDlg.ShowModal()

if __name__ == '__main__':
    test()