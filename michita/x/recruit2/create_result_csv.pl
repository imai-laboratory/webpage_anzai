#!/usr/local/perl-5.8.3/bin/perl

use strict;
use DBI;
require 'cgi-lib.pl';


my $i;

my $db;
my $str;
my @arr;


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT u.gakunen, u.gakuseki, u.username, c.name, u.kigyoumei1, u.lab, u.email, u.tel, u.keitai from users2 u, company c where u.kibou1 = c.id order by u.gakuseki asc" );
$str->execute();

print "³ØÇ¯, ³ØÀÒÈÖ¹æ, Ì¾Á°, Âè£±´õË¾, ´ë¶È/³Ø¹»Ì¾, ¸¦µæ¼¼, ¥á¡¼¥ë¥¢¥É¥ì¥¹, ÅÅÏÃÈÖ¹æ, ·ÈÂÓÅÅÏÃ\n";
while( @arr = $str->fetchrow ){
	for( $i = 0; $i < @arr; $i++ ){
		print "$arr[$i], ";
	}
	print "\n";
}

$str->finish();
$db->disconnect();
