#!/usr/local/perl-5.8.3/bin/perl

use strict;
use DBI;
require 'cgi-lib.pl';


my $out = "";
my $list = "";
my $http_header = "Content-type: text/html\n\n";


my $db;
my $str;
my @arr;

my @company;


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT name, id from company order by id asc" );
$str->execute();

while( @arr = $str->fetchrow ){
	$company[@company] = $arr[0];
}

$str->finish();
$db->disconnect();


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT gakuseki, username, kibou1, kigyoumei1, last_update2, suisensho from users2 order by gakuseki asc" );
$str->execute();


while( @arr = $str->fetchrow ){
	$list .= "<tr><td class=\"chousahyou\">";
	$list .= "<a target=\"_blank\" href=\"view2.cgi?$arr[0]\">$arr[0]</a></td>";
	$list .= "<td class=\"chousahyou\">$arr[1]</td>";
	$list .= "<td class=\"chousahyou\">$company[$arr[2]]</td>";
	$list .= "<td class=\"chousahyou\">$arr[3]</td>";
	$list .= "<td class=\"chousahyou\">$arr[4]</td><td class=\"chousahyou\">";
	$list .= "<form method=\"POST\" action=\"update.cgi\" name=\"update$arr[0]\">";
	$list .= "<input type=\"hidden\" name=\"gakuseki\" value=\"$arr[0]\">";
	if( $arr[5] == 0 ){
		$list .= "<input type=\"submit\" value=\"発行\">";
	} else {
		$list .= "<input type=\"submit\" value=\"発行済\">";
	}
	$list .= "</form></td></tr>\n";
}

$str->finish();
$db->disconnect();


open( IN, "view.htm" );
$out = $http_header;

while( <IN> ){
	$out .= $_;
}

close( IN );


my $time = localtime;

$out =~ s/<%localtime%>/$time/;
$out =~ s/<%list%>/$list/;
print $out;
