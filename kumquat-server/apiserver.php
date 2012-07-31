<?php
/**
	用户反馈服务API
	接受2个GET参数: client_key(客户端验证Key), action(执行动作)

	返回信息为XML
	<?xml version="1.0" encoding="utf-8" ?>
	<apiserver>
		<action name="$name" desc="$desc" />
		<status error="$error" desc="$desc" />
		<extra desc="$desc">$data</extra> ?
		<refer url="$refer" desc="$desc" /> ?
	</apiserver>
 */

$actions = array(
	'feedback_add' => '添加反馈', // 接受4个POST参数: username(用户名), email(邮箱), content(反馈内容), info(信息"os:nt;version:1.0;...")
	'none' => '无动作',
);

# Error code
define( 'KR_OK', 0 ); // 无错
define( 'KR_AUTH_FAILED', 1 ); // 验证失败
define( 'KR_NOT_IMPL', 2 ); // 未实现
define( 'KR_NO_ACTION', 3 ); // 无动作


function action_node( $name, $desc )
{
	$name = htmlspecialchars($name);
	$desc = htmlspecialchars($desc);
	echo '<action name="'.$name.'" desc="'.$desc.'" />';
}

function status_node( $error, $desc )
{
	$error = htmlspecialchars($error);
	$desc = htmlspecialchars($desc);
	echo '<status error="'.$error.'" desc="'.$desc.'" />';
}

function extra_node( $data, $desc )
{
	$desc = htmlspecialchars($desc);
	echo '<extra desc="'.$desc.'">'.$data.'</extra>';
}

function refer_node( $refer, $desc = '返回上一页' )
{
	$refer = htmlspecialchars($refer);
	$desc = htmlspecialchars($desc);
	echo "<refer url=\"$refer\" desc=\"$desc\" />";
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

# XML
header('Content-Type: text/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="utf-8" ?>';
echo '<apiserver>';

# client_key 是一个字符串，用于简单验证客户端身份
$client_key_auth = 'KumquatRoot.1:2012-07-31';

$client_key = isset($_GET['client_key']) ? gpc($_GET['client_key']) : '';
$action = isset($_GET['action']) ? gpc($_GET['action']) : 'none';

# 要执行的动作
if ( isset( $actions[$action] ) )
	action_node( $action, $actions[$action] );
else
	action_node( 'none', $actions['none'] );

if ( $client_key != $client_key_auth )
{
	status_node( KR_AUTH_FAILED, '客户端验证失败' );
	//extra_node( urlencode($client_key_auth), '验证串' );
}
else
	switch ( $action )
	{
	case 'feedback_add':
		$username = isset($_POST['username']) ? gpc($_POST['username']) : '';
		$email = isset($_POST['email']) ? gpc($_POST['email']) : '';
		$content = isset($_POST['content']) ? gpc($_POST['content']) : '';
		$info = isset($_POST['info']) ? gpc($_POST['info']) : '';
		$time = time();
		$ip = ip();

		status_node( KR_NOT_IMPL, '暂未实现' );
		
		break;
	default:
		status_node( KR_NO_ACTION, '没有执行任何动作' );
		break;
	}


echo '</apiserver>';
