<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>API服务接口</title>
<style type="text/css">
* {
	font-size:12px;
	font-family:'宋体';
}
pre { margin:0; padding:0; }
table { border-collapse:collapse; }
table tr td { border-collapse:collapse; padding:4px;}
table.api tr td {border:1px solid #666;}
code {font-family:'Courier New';}
var {font-size:14px;}
.bgclr {background:#CCC;};
.typeword {color:blue;font-family:'Courier New';}
.defvalue {color:darkgreen;font-family:'Courier New';}
.method {color:darkred;}
h1 {font-size:32px;}
.warning {color:#FF6600;}
.error {color:#FF0000;font-family:'Courier New';}
</style>
</head>
<body>
<h1>API服务接口</h1>
<h2>API地址：<xsl:value-of select="apiserver/@url" /></h2>
	<xsl:for-each select="apiserver/api">
	<xsl:sort select="@name"/>
		<table class="api">
		<tr>
			<td align="right" class="bgclr">API名称：</td>
			<td>[<span class="method"><xsl:value-of select="@method" /></span>]<xsl:value-of select="@name" />　<span class="error"><xsl:value-of select="@attr" /></span></td>
			<td><xsl:value-of select="@desc" /></td>
		</tr>
		<tr>
			<td align="right" class="bgclr" valign="top">参数列表：</td>
			<td style="overflow:auto;" valign="top">
				<xsl:for-each select="params/param">
					<div><xsl:choose><xsl:when test="@method">[<span class="method"><xsl:value-of select="@method" /></span>]</xsl:when><xsl:otherwise>[<span class="method"><xsl:value-of select="../../@method" /></span>]</xsl:otherwise></xsl:choose><code><var><xsl:value-of select="@name" /></var>:<span class="typeword"><xsl:value-of select="@type" /></span><xsl:if test="@defvalue">=<span class="defvalue"><xsl:value-of select="@defvalue" /></span></xsl:if></code>,<xsl:value-of select="@desc" /></div>
					<div style="padding-left:1em;">
						<xsl:for-each select="value">
							<div><xsl:value-of select="@value" />　<xsl:value-of select="@desc" /></div>
						</xsl:for-each>
					</div>
				</xsl:for-each>
			</td>
			<td style="overflow:auto;" valign="top"><pre><xsl:if test="notice"><xsl:value-of select="notice/text()" /></xsl:if></pre></td>
		</tr>
		<tr>
			<td align="right" class="bgclr">返回值：</td>
			<td><span class="typeword"><xsl:value-of select="return/@type" /></span></td>
			<td><pre><xsl:value-of select="return/text()" /></pre></td>
		</tr>
		</table>
		<br />
	</xsl:for-each>
</body>
</html>
</xsl:template>
</xsl:stylesheet>