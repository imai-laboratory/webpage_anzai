#!/usr/local/bin/perl
# cosmosではここの位置 spicaはlocalぬき

#$mailto = 'michita@ayu.ics.keio.ac.jp';

$header = <<END_OF_DATA;
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=Shift_JIS">
<title>メール送信結果</title>
</head>
<body>
<h1>メール送信結果</h1>
<hr>
<p>下記のメールを送信しました。ありがとうございました。</p>
<hr>
END_OF_DATA



print "Content-type: text/html\n\n";

print "<html><body>Hello CGI</body></html>";



