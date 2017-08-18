#!/usr/local/perl-5.8.3/bin/perl

use strict;
use DBI;
require 'cgi-lib.pl';


my $i;

my $db;
my $str;
my @arr;

my @company_name;
my @company_max;
my @company_kibou1;
my @company_kibou2;
my @company_kibou3;


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT name, max, id from company order by id asc" );
$str->execute();

while( @arr = $str->fetchrow ){
	$company_name[@company_name] = $arr[0];
	$company_max[@company_max] = $arr[1];
}

for( $i = 0; $i < @company_name; $i++ ){
	$company_kibou1[$i] = 0;
	$company_kibou2[$i] = 0;
	$company_kibou3[$i] = 0;
}


$str->finish();
$db->disconnect();


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT kibou1, count(kibou1) from users2 group by kibou1" );
$str->execute();

while( @arr = $str->fetchrow ){
	$company_kibou1[$arr[0]] = $arr[1];
}

$str->finish();
$db->disconnect();


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT kibou2, count(kibou2) from users2 group by kibou2" );
$str->execute();

while( @arr = $str->fetchrow ){
	$company_kibou2[$arr[0]] = $arr[1];
}

$str->finish();
$db->disconnect();


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT kibou3, count(kibou3) from users2 group by kibou3" );
$str->execute();

while( @arr = $str->fetchrow ){
	$company_kibou3[$arr[0]] = $arr[1];
}

$str->finish();
$db->disconnect();


print "<html lang=\"ja\">\n";
print "<head><title>¿ÊÏ©´õË¾Ä´ºº</title>\n";
print "<meta http-equiv=\"content-type\" content=\"text/html; charset=euc-jp\">\n";
print "<link rel=\"stylesheet\" href=\"recruit.css\">\n";
print "</head><body>\n";
print "<img src=\"top.png\"><br><br>\n";
print "<center><table width=\"95%\">\n";
print "<tr><td class=\"title\">ID</td><td class=\"title\">¿Ê³Ø¡¦½¢¿¦</td><td class=\"title\">Êç½¸¿Í¿ô</td><td class=\"title\">Âè1´õË¾</td><td class=\"title\">Âè2´õË¾</td><td class=\"title\">Âè3´õË¾</td></tr>\n";

for( $i = 1; $i <= 2; $i++ ){
	print "<tr><td class=\"data_singaku\">$i</td><td class=\"data_singaku\">$company_name[$i]</td><td class=\"data_singaku\">-</td><td class=\"data_singaku\">$company_kibou1[$i]</td><td class=\"data_singaku\">$company_kibou2[$i]</td><td class=\"data_singaku\">$company_kibou3[$i]</td></tr>\n";
}

for( $i = 3; $i < @company_name; $i++ ){
	print "<tr><td class=\"data_syusyoku\">$i</td><td class=\"data_syusyoku\">$company_name[$i]</td><td class=\"data_syusyoku\">$company_max[$i]</td><td class=\"data_syusyoku\">$company_kibou1[$i]</td><td class=\"data_syusyoku\">$company_kibou2[$i]</td><td class=\"data_syusyoku\">$company_kibou3[$i]</td></tr>\n";
}

print "</table></center>\n";
print "</body>\n";
print "</html>\n";
