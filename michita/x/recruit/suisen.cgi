#! /usr/local/perl5/bin/perl
#! /usr/local/perl-5.6.1/bin/perl

print "Content-type: text/html\n\n";

print "<html>\n";
print "<head>\n";
print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=euc\">\n";
print "<meta http-equiv=\"Content-Language\" content=\"ja\">\n";
print "<title>学校推薦</title>\n";
print "<style type=\"text/css\">\n";
print "<!--\n";
print "table.section{width:100%}\n";
print "table.table{width:80%}\n";
print "td.section{text-align:center;color:white;background-color:#0000ff}\n";
print "tr.even{background-color:\#eeeeee}\n";
print "tr.odd{background-color:\#fdfdfd}\n";
print "-->\n</style>\n";
print "</head>\n";

print "<body>\n";
print "<table border=1 class=\"section\"><tr><td class=\"section\">\n";
print "<h2>学校推薦</h2>\n";
print "</td></tr></table>\n";
print "<p align=\"center\"><table border=1 class=\"table\"><tr><th>会社名</th><th>募集</th><th>備考</th></tr>\n";

if( open( SRC, "suisen.txt" )){
	$tmp = 0;
	while( <SRC> ){
		chomp;
		split(/:/);

		if( $tmp == 0 ){
			print "<tr class=\"even\"><td>$_[0]</td><td>$_[1]</td><td>$_[2]</td></tr>\n";
			$tmp = 1;
		} else {
			print "<tr class=\"odd\"><td>$_[0]</td><td>$_[1]</td><td>$_[2]</td></tr>\n";
			$tmp = 0;
		}
	}

	close( SRC );
}

print "</table></p>\n";
print "<ul>\n";
print "<li>情報系: 情報工学科、開放環境科学の情報系専修</li>\n";
print "<li>[面]は就職担当者が企業の方と面談を行ったことを示す。</li>\n";
print "<ul>\n";
print "<li>就職担当者が面談を行っているため、直接話をうかがっています。また何かあったら、先方の担当者に質問できます。</li>\n";
print "</ul>\n";
print "</ul>\n";
print "<p><a href=\"index.htm\">戻る</a></p>\n";
print "</body>\n";
print "</html>\n";

