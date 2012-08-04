#coding:utf-8

#-------------------------------------------------------------------------------
# Name:        FeedbackDlg.py
# Purpose:
#
# Author:      Mr.Wid
#
# Created:     29-07-2012
# Copyright:   (c) Mr.Wid 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import time
import httplib
import urllib
import md5
import platform
import xml.dom.minidom

def en(x):
    return x.encode("utf8")

def submit_feedback( username, email, info, content ):
    try:
        clientKey = md5.md5('KumquatRoot.1:' + time.strftime("%Y-%m-%d")).hexdigest()
        params_get = urllib.urlencode({ 'client_key':clientKey, 'action':'feedback_add' })
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/xml"
        }
        conn = httplib.HTTPConnection("www.x86pro.com")

        params_post = urllib.urlencode({
            'username':en(username),
            'email':en(email),
            'info':en(info),
            'content':en(content)
        })

        conn.request("POST", "/kumquat/apiserver.php?" + params_get, params_post, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        xmldom = xml.dom.minidom.parseString(data)

        statusNode = xmldom.getElementsByTagName('status')
        statusNode = statusNode[0]

        errno = int(statusNode.attributes['error'].nodeValue)

        return errno, statusNode.attributes['desc'].nodeValue
    except:
        return -1, u'网络连接错误!'

def get_system_info():
    _format = 'soft:KumquatRoot;os:%s;py_ver:%s;wx_ver:%s'
    return _format%( platform.platform(), platform.python_version(), wx.version() )

class FeedbackDlg(wx.Dialog):
    def __init__( self, parent ):
        wx.Dialog.__init__(
            self,
            parent = parent,
            title = u'意见反馈',
            size = ( 300, 400 )
        )
        #标签控件---------------------
        self.lblLabel = [ u'姓名:', u'E-mail:' ]
        y = 30
        for lbl in self.lblLabel:
            wx.StaticText(
                self,
                label = lbl,
                pos = ( 30, y )
            )
            y += 40

        #文本框控件-------------------
        self._txtUserName = wx.TextCtrl(
            self,
            pos = ( 80, 28 ),
            size = ( 180, 20 ),
        )
        self._txtUserEmail = wx.TextCtrl(
            self,
            pos = ( 80, 68 ),
            size = ( 180, 20 ),
        )
        self.groupBox = wx.StaticBox(
            self,
            label = u'内容(必填)[0/1024]',
            pos = ( 20, y ),
            size = ( 255, 200 )
        )
        self._txtUserContents = wx.TextCtrl(
            self,
            pos = ( 30, y + 20 ),
            size = ( 235, 170 ),
            style = wx.TE_MULTILINE,
        )
        self._txtUserContents.SetMaxLength(1024)

        #按钮控件----------------------
        self._btnSub = wx.Button(
            self,
            label = u"提交",
            pos = ( 85, 320 ),
            size = ( 50, 30 )
        )
        self._btnCancel = wx.Button(
            self,
            id = wx.ID_CANCEL,
            label = u"取消",
            pos = ( 155, 320 ),
            size = ( 50, 30 )
        )

        #事件绑定----------------------
        self._btnSub.Bind( wx.EVT_BUTTON, self.OnSub )
        self._txtUserContents.Bind( wx.EVT_TEXT, self.ResetBoxLabel )

    #事件方法----------------------
    def ResetBoxLabel( self, event ):
        length = len(self._txtUserContents.Value)
        self.groupBox.SetLabel( u'内容(必填)[%d/1024]' % length )

    def OnSub(self, event):
        if not self._txtUserContents.Value:
            wx.MessageBox(u'反馈内容不能为空!')
            return

        errno, desc = submit_feedback( self._txtUserName.Value, self._txtUserEmail.Value, get_system_info(), self._txtUserContents.Value )

        wx.MessageBox(desc)
        if not errno:
            self.EndModal(wx.ID_OK)

def test():
    app = wx.PySimpleApp()
    feedback = FeedbackDlg(None)
    feedback.ShowModal()

if __name__ == '__main__':
    test()