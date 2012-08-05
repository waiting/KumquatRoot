<?php
require_once 'init-settings.php';
	
?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=<?php echo $page_charset; ?>" />
<title>Kumquat 反馈查看</title>
<style type="text/css">
body {
	font-size:12px;
}
a:link {
	color:#009966;
	text-decoration:none;
}
a:visited {
	color:#009966;
	text-decoration:none;
}
a:hover {
	color:#99CC99;
	text-decoration:overline underline;
}
h1 {
	font-size:28px;
	text-align:center;
}
/* 图片边框样式 */
.clsImage {
	border:none;
}
/* content内容样式 */
#content {
	font-size:12px;
	text-align:center;
}
#table_form {
/*	border:dashed 1px;*/
}
.msg_block {
	width:780px;
	text-align:left;
	margin:0px auto 0px auto;
}
.msg_header {
	background-color: #FFCC99;
	padding:2px;
	border-top:solid 1px;
	border-left:solid 1px;
	border-right:solid 1px;
	margin-top:10px;
}
.msg_body {
	width:758px;
	background-color: #FFFFFF;
	padding:10px;
	margin:0;
	border:solid 1px;
	overflow:auto;
}
/* footer 底部样式*/
#footer {
	font-size:12px;
	text-align:center;
	color:#333333;
	font-weight:bold;
}
</style>
</head>
<body>
<h1>Kumquat 反馈信息</h1>
<div class='msg_block'>
<?php
$res = $pdo->query('select * from feedbacks;');
while ( $row = $res->fetch() )
{
?>
    <div class='msg_header'>用户:[<?php echo iif( $row['username'], $row['username'], '匿名' ); ?>] <?php if ( $row['email'] ) echo "邮箱:<a href=\"mailto:$row[email]\">$row[email]</a> " ; ?>时间:[<?php echo date( 'Y-m-d H:i:s', $row['time'] ); ?>]</div>
    <pre class='msg_body'><?php echo htmlspecialchars($row['content']); ?></pre>
<?php
}
?>
</div>
</body>
</html>
