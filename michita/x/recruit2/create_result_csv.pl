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

print "��ǯ, �����ֹ�, ̾��, �裱��˾, ���/�ع�̾, ���漼, �᡼�륢�ɥ쥹, �����ֹ�, ��������\n";
while( @arr = $str->fetchrow ){
	for( $i = 0; $i < @arr; $i++ ){
		print "$arr[$i], ";
	}
	print "\n";
}

$str->finish();
$db->disconnect();
