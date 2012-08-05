<?php
/** 给定一个值，若真，则输出指定字符串，否则输出另外字符串
 * @param $b boolean
 * @param $v1 string
 * @param $v2 string
 * @return string */
function iif($b, $v1, $v2 = '')
{
	return $b ? $v1 : $v2;
}

/** 从GET,POST,COOKIE获取字符串. ',",\,NULL
 * @param $str string
 * @param $haveSlashes bool[optional] true,结果包含\; false,结果祛除\
 * @return string */
function gpc( $str, $haveSlashes = false )
{
	$magic_quotes_gpc = ini_get('magic_quotes_gpc');
	if ( $haveSlashes )
		return $magic_quotes_gpc ? $str : addslashes($str);
	else
		return $magic_quotes_gpc ? stripslashes($str) : $str;
}

/** 返回用户IP地址
 * @return string */
function ip()
{
	$ip = "Unknown";
	if ( isset($_SERVER["HTTP_X_FORWARDED_FOR"]) )
		$ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
	else if ( isset($_SERVER["HTTP_CLIENT_IP"]) )
		$ip = $_SERVER["HTTP_CLIENT_IP"];
	else if ( isset($_SERVER["REMOTE_ADDR"]) )
		$ip = $_SERVER["REMOTE_ADDR"];
	else if ( getenv("HTTP_X_FORWARDED_FOR") )
		$ip = getenv("HTTP_X_FORWARDED_FOR");
	else if ( getenv("HTTP_CLIENT_IP") )
		$ip = getenv("HTTP_CLIENT_IP");
	else if ( getenv("REMOTE_ADDR") )
		$ip = getenv("REMOTE_ADDR");
	return $ip;
}

require_once 'config.inc.php';
mb_internal_encoding($page_charset);
$pdo = new PDO( $db_dsn, $db_user, $db_pwd, array( PDO::ATTR_PERSISTENT => true ) );
