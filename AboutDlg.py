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

KumquatRoot_Introduction = u'''KumquatRoot是一款完全免费的绿色软件,集文件搜索、内容查找于一身。具有小巧精致、操作简单、高效搜索的特点.

*文件名检索:
    指定目录范围,只需要输入文件名或文件名的正则表达式，即可快速找到所有符合条件的文件.

*文件内容检索:
    指定目录范围,使用关键字或者正则表达式，即可找到在该目录下所有包含该字符的文件.

*黑白名单功能:
    设置文件后缀白名单或黑名单后,在搜索时即可选择使用白名单或者黑名单进行检索,选择白名单时,软件仅查找以白名单中内容为后缀的文件;选择黑名单时，软件将自动过滤掉以黑名单内容为后缀的文件.

*混合查找:
    您还可以既限制文件名也限制关键字进行或文件文件内容查找,大大提高了文件查找的效率.

*完善的意见反馈服务:
    在主界面使用鼠标右键即可弹出菜单栏,在"反馈"选项中,可以反馈您对本软件的建议以及意见,我们将努力按照您的建议以及意见对软件进行维护,力争为您提供更好的服务.

金桔软件工作室 ( KumquatSoft )
联系我们: kumquatsoft@163.com
'''

KumquatRoot_License = u'''用户须知:请仔细阅读本协议(未成年人应当在其法定监护人陪同下阅读).

重要声明:
    <1>.您一旦复制、安装或使用《KumquatRoot》软件以及软件的所有或任何部分,即默认您已接受本协议中规定的所有条款和条件,否则您无权复制、安装或使用《KumquatRoot》软件以及其软件的任何部分;
    <2>.本《KumquatRoot用户使用协议》以下简称《协议》;
    <3>.软件使用者您以下简称"用户";
    <4>."KumquatRoot软件"以下简称"本软件";
    <5>.开发单位"金桔软件工作室"以下简称"金桔"或"金桔软件";
    <6>.本《协议》是金桔软件根据《中华人民共和国著作权法》、《中华人民共和国合同法》、《著作权行政处罚实施办法》等国家法律法规拟定.

《KumquatRoot用户使用协议》内容如下:

    1.知识产权声明:
        本软件的一切版权等知识产权，以及与本软件相关的所有信息内容,包括但不限于:文字表述及其组合、图标、图饰、图表、色彩、界面设计、版面框架、有关数据、印刷材料、电子文档、软件代码等均受《中华人民共和国著作权法》和《国际著作权条约》以及其他知识产权法律法规的保护。

    2.用户授权:
        本软件为免费软件,著作权归金桔软件所有。本《协议》授予您下列相关权利:
        <1>.您可以安装和使用无限制次数的本软件所提供的服务；
        <2>.您可以复制、分发和传播无限制数量的软件产品,但您必须保证每一份复制、分发和传播都是完整和真实的,包括所有有关本软件的软件主体及相关文件、电子文档、宣传内容，著作权和商标宣言,亦包括本《协议》.

    3.用户权利限制声明:
        用户在遵守法律及本使用协议的前提下，可依本使用协议使用本软件,用户无权实施包括但不限于下列行为：
        <1>.对本软件进行逆向工程、反向编译和反向汇编;
        <2>.将本软件将各个部分分开用于其他目的;
        <3>.利用本软件发表、传送、传播、储存违反国家法律、危害国家安全、祖国统一、社会稳定的内容，或侮辱诽谤、色情、暴力及任何违反国家法律法规政策的内容;
        <4>.利用本软件进行任何危害计算机以及计算机网络安全的行为,包括但不限于:未经允许进入公众计算机网络或者他人计算机系统并删除、修改、增加存储信息;未经许可企图探查、扫描、测试本软件所在的弱点或其它实施破坏网络安全的行为;故意传播恶意程序或病毒以及其他破坏干扰正常网络信息服务的行为.

    4.协议的终止:
        如果您在使用过程中未遵守本《协议》的各项条款,即默认用户与金桔软件终止本《协议》,终止协议后,则您必须销毁本软件及其各部分的所有副本.
        除您主动与金桔软件终止协议外,如果出现下述情况之一,金桔软件可随时终止与您的使用协议:
        <1>.您违反了本使用协议中任何条款的规定(或您的行为方式明显表明您无意或无法遵循本使用协议的条款规定);
        <2>.法律要求金桔软件终止与您的本使用协议;
        <3>.金桔软件不再向您所居住的国家/地区提供产品或服务;
        <4>.金桔软件不再向您所使用的系统提供产品或服务.

    5.用户隐私权制度:
        为更好的服务用户,用户在反馈意见时,本软件将自动获取用户的操作系统版本、Python平台版本、wxPython平台版本以便对本软件进行改进,此外,本软件不会获取任何用户有关信息,除法律程序所规定,金桔软件不会在未经用户授权的情况下公开、编辑、或透露用户的任何相关信息.

    6.免责条款:
        <1>.本软件并无附带任何形式的明示的或暗示的保证，包括任何关于本软件的适用性, 无侵犯知识产权或适合作某一特定用途的保证。
        <2>.使用本软件由用户自己承担风险,在任何情况下,对于因使用本软件或无法使用本软件而导致的任何损失,金桔软件均无须承担法律责任;
        <3>.金桔软件可随时更改本软件,无须对用户另作通知;
        <4>.由于本软件可以通过互联网等途径下载、传播,对于从非金桔软件官方网站(http://www.x86pro.com/)或指定站点下载的本软件以及从非金桔软件发行的介质上获得的本软件,金桔软件无法保证该软件是否感染计算机病毒、是否隐藏有伪装的特洛伊木马程序或者黑客软件,金桔软件不承担由此引起的直接或间接损害责任;

    7.法律的适用和管辖:
        本协议的生效、履行、解释及争议的解决均适用中华人民共和国法律,本协议中的条款因与中华人民共和国现行法律相抵触的部分自动无效,但不影响其他部分的效力.

联系我们:
    网站: http://www.x86pro.com
    邮箱: kumquatsoft@163.com
'''

KumquatRoot_Others = u'''关于http://www.x86pro.com:
    X86PRO.COM是一个编程技术文章站点,始建于2009年4月,虽然文章数不算多,但大部分属于原创,我们欢迎有能力的人献文。
    X86PRO.COM同时也是金桔软件工作室的官方网站。

站长的话:
    本站先后使用了3个后台系统,2009年是WT自制的WTSite，2010年是用了DedeCMS，今年就用WordPress看看。

    由于WordPress本身的原因不支持IE6,所以您在浏览本站时最好使用其他浏览器,比如Chrome,Firefox,Opera,ie7+。

    还是要强调一下，本站意在为想要学好编程的人提供一个平台，如果您只是想应付考试赚学分，那请您离开，本站不适合您。

    2011年5月左右,本站停开,2012年本站再次开放。

    本站QQ群:38583240,79913713。

金桔软件工作室 ( KumquatSoft )
联系我们: kumquatsoft@163.com
'''

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
            label = u'作者:    WT、Mr.Wid  (金桔软件工作室)',
            pos = (30, 160 )
        )
        self._lblWTEmail = wx.StaticText(
            self,
            label = u'E-mail:  zth555@qq.com (WT)   mr_wid@163.com (Mr.Wid)\n'+' '*11+\
                    u'kumquatsoft@163.com (金桔软件)',
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

        #显示介绍、协议、其他文本框中的内容
        _txtLicense.SetValue(KumquatRoot_License)
        _txtIntroduction.SetValue(KumquatRoot_Introduction)
        _txtOthers.SetValue(KumquatRoot_Others)

        #------确定按钮------
        self._btnOK = wx.Button(
            self,
            id = wx.ID_OK,
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