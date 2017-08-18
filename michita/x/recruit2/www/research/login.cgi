#!/usr/local/perl-5.8.3/bin/perl

use strict;
use DBI;
require 'cgi-lib.pl';


my %get_data;
&ReadParse( \%get_data );

my $gakuseki = $get_data{'gakuseki'};
my $password = $get_data{'password'};


my $out = "";
my $http_header = "Content-type: text/html\n\n";

my $db;
my $str;
my @arr;

my @company;

my $tmp1 = "";
my $tmp2 = "";


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT name, id from company order by id asc" );
$str->execute();

while( @arr = $str->fetchrow ){
	$company[@company] = $arr[0];
}

$str->finish();
$db->disconnect();


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT * from users2 where gakuseki=\'$gakuseki\'" );
$str->execute();

@arr = $str->fetchrow;
my $db_password = $arr[1];

$str->finish();
$db->disconnect();


if( $password eq "" || $gakuseki eq "" || $password ne $db_password ){
	open( IN, "loginerr.htm" );
} else {
	open( IN, "loginsuc.htm" );
}

$out = $http_header;

while( <IN> ){
	$out .= $_;
}

close( IN );


$out =~ s/<%lastupdate%>/$arr[27]/g;

if( $arr[3] == 1 ){
	$out =~ s/<%gakunen%>/開放環境科学/g;
} else {
	$out =~ s/<%gakunen%>/情報工学科/g;
}
$out =~ s/<%name%>/$arr[2]/g;

if( $arr[5] == 0 ){
	$tmp1 = "<option value=\"0\" selected>未選択</option>\n";
} else {
	$tmp1 = "<option value=\"0\">未選択</option>\n";
}
if( $arr[5] == 1 ){
	$tmp1 .= "<option value=\"1\" selected>男</option>\n";
} else {
	$tmp1 .= "<option value=\"1\">男</option>\n";
}
if( $arr[5] == 2 ){
	$tmp1 .= "<option value=\"2\" selected>女</option>\n";
} else {
	$tmp1 .= "<option value=\"2\">女</option>\n";
}
$out =~ s/<%seibetsu%>/$tmp1/g;

$out =~ s/<%gakuseki%>/$arr[0]/g;
$out =~ s/<%lab%>/$arr[4]/g;
$out =~ s/<%naisen%>/$arr[6]/g;
$out =~ s/<%email%>/$arr[7]/g;
$out =~ s/<%addr%>/$arr[8]/g;
$out =~ s/<%kisei%>/$arr[9]/g;
$out =~ s/<%tel%>/$arr[10]/g;
$out =~ s/<%keitai%>/$arr[11]/g;
$out =~ s/<%password%>/$password/g;

for( my $i = 1; $i <= 3; $i++ ){
	$tmp1 = "";
	for( my $j = 0; $j < @company; $j++ ){
		$tmp1 .= "<option value=\"$j\"";

		if( $j == $arr[11+$i] ){
			$tmp1 .=" selected";
		}
		$tmp1 .= ">$j. $company[$j]</option>\n";
	}
	$tmp2 = "<%kibou" . $i . "%>";
	$out =~ s/$tmp2/$tmp1/g;
	$tmp2 = "<%kigyoumei" . $i . "%>";
	$out =~ s/$tmp2/$arr[14+$i]/g;

	if( $arr[17+$i] == 0 ){
		$tmp1 = "<option value=\"0\" selected>内々定を得ていない</option>\n";
		$tmp1 .= "<option value=\"1\">内々定を得ている</option>\n";
	} else {
		$tmp1 = "<option value=\"0\">内々定を得ていない</option>\n";
		$tmp1 .= "<option value=\"1\" selected>内々定を得ている</option>\n";
	}
	$tmp2 = "<%nainaitei" . $i ."%>";
	$out =~ s/$tmp2/$tmp1/g;
	$tmp2 = "<%riyuu" . $i . "%>";
	$out =~ s/$tmp2/$arr[20+$i]/g;
	$tmp2 = "<%katsudou" . $i . "%>";
	$out =~ s/$tmp2/$arr[23+$i]/g;
}
print $out;


# 0.  gakuseki text not null unique,
# 1.  password text not null,
# 2.  username text not null,
# 3.  gakunen int not null,
# 4.  lab text default '',
# 5.  seibetsu int default 0,
# 6.  naisen text default '',
# 7.  email text default '',
# 8.  addr text default '',
# 9.  kisei text default '',
# 10. tel text default '',
# 11. keitai text default '',
# 12. kibou1 int default 0,
# 13. kibou2 int default 0,
# 14. kibou3 int default 0,
# 15. kigyoumei1 text default '',
# 16. kigyoumei2 text default '',
# 17. kigyoumei3 text default '',
# 18. nainaitei1 int default 0,
# 19. nainaitei2 int default 0,
# 20. nainaitei3 int default 0,
# 21. riyuu1 text default '',
# 22. riyuu2 text default '',
# 23. riyuu3 text default '',
# 24. katsudou1 text default '',
# 25. katsudou2 text default '',
# 26. katsudou3 text default '',
# 27. last_update text default '' not null
