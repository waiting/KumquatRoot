ScarchingDlg功能函数帮助文档
============================

##与进度条相关##
*setProgressLength(self, int percent)       -> #设置进度条已完成进度

##与标签相关的方法##
*setScarchingFileName(self, string content) -> 设置"正在搜索"标签内容

*setTotalFileNumber(self, string number)    -> 设置"文件总计"标签内容

*setSearchedFileNumber(self, string number) -> 设置"已扫面数"标签内容

*setSurplusFileNumber(self, string number)  -> 设置"剩余文件"标签内容

*setUsedTime(self, string number)           -> 设置"已用时长"标签内容

*setSurplusTime(self, string number)        -> 设置"剩余时长"标签内容

*setConformNumber(self, string number)      -> 设置"符合条件"标签内容

##与按钮有关##
*按下"暂停"按钮时熬出"PressPauseButton"异常类
*按下"终止"按钮时熬出"PressStopButton"异常类

*Version:0.1.20120723.2251*