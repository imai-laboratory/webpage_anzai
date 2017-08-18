#!/usr/local/perl-5.8.3/bin/perl

use strict;
use DBI;
require 'cgi-lib.pl';


my %get_data;
&ReadParse( \%get_data );

my $gakuseki = $get_data{'gakuseki'};


my $out = "";
my $http_header = "Content-type: text/html\n\n";
my $errormessage = "";

my $db;
my $str;
my @arr;


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT suisensho from users2 where gakuseki=\'$gakuseki\'" );
$str->execute();

@arr = $str->fetchrow;
my $db_suisensho = $arr[0];

$str->finish();
$db->disconnect();


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$db->{AutoCommit} = 0;
$db->{RaiseError} = 1;

my $suisensho = ( $db_suisensho + 1 ) % 2;
my $last_update2 = localtime;

eval{
	$db->do( "UPDATE users2 SET suisensho=\'$suisensho\', last_update2=\'$last_update2\' where gakuseki=\'$gakuseki\'" );
	$db->commit();
};
if( $@ ){
	$errormessage = "Transaction aborted because $@\n\n\n";
	$db->rollback;
}

$db->disconnect();

open( IN, "update.htm" );

$out = $http_header;

while( <IN> ){
	$out .= $_;
}

close( IN );


$out =~ s/<%errormessage%>/$errormessage/g;
print $out;
