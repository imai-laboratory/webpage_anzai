#! /usr/local/perl5/bin/perl
#! /usr/local/perl-5.6.1/bin/perl

print "Content-type: text/html\n\n";

print "<html>\n";
print "<head>\n";
print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=euc\">\n";
print "<meta http-equiv=\"Content-Language\" content=\"ja\">\n";
print "<title>获瘟</title>\n";
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
print "<h2>获瘟</h2>\n";
print "</td></tr></table>\n";
print "<p align=\"center\"><table border=1 class=\"table\"><tr><th>柴家叹</th><th><br></th></tr>\n";

if( open( SRC, "shiryou.txt" )){
	$tmp = 0;
	while( <SRC> ){
		chomp;
		split(/:/);

		if( $tmp == 0 ){
			print "<tr class=\"even\"><td>$_[0]</td><td>$_[1]</td></tr>\n";
			$tmp = 1;
		} else {
			print "<tr class=\"odd\"><td>$_[0]</td><td>$_[1]</td></tr>\n";
			$tmp = 0;
		}
	}

	close( SRC );
}

print "</table></p>\n";
print "<p><a href=\"index.htm\">提る</a></p>\n";
print "</body>\n";
print "</html>\n";

