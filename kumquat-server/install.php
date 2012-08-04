<?php
header('Content-Type: text/html; charset=utf-8');
require_once 'init-settings.php';

$ret = $pdo->exec(
	"CREATE TABLE IF NOT EXISTS feedbacks(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(32) NOT NULL default '',
		email VARCHAR(128) NOT NULL default '',
		info VARCHAR(512) NOT NULL default '',
		content TEXT NOT NULL default '',
		ip VARCHAR(15) NOT NULL default '0.0.0.0',
		time INTEGER NOT NULL default '0'
	);"
);

if ( $ret !== false )
{
	echo '初始化数据库成功！';
}