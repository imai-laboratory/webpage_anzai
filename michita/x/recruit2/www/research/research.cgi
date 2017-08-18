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
my $errormessage = "";

my $db;
my $str;
my @arr;


$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
$str = $db->prepare( "SELECT password from users2 where gakuseki=\'$gakuseki\'" );
$str->execute();

@arr = $str->fetchrow;
my $db_password = $arr[0];

$str->finish();
$db->disconnect();


if( $password eq "" || $gakuseki eq "" || $password ne $db_password ){
	open( IN, "researcherr.htm" );
} else {
	$db = DBI->connect( 'DBI:Pg:dbname=shushoku', 'postgres' ) || die $db->errstr;
	$db->{AutoCommit} = 0;
	$db->{RaiseError} = 1;

	my $lab = $get_data{'lab'};
	my $seibetsu = $get_data{'seibetsu'};
	my $naisen = $get_data{'naisen'};
	my $email = $get_data{'email'};
	my $addr = $get_data{'addr'};
	my $kisei = $get_data{'kisei'};
	my $tel = $get_data{'tel'};
	my $keitai = $get_data{'keitai'};
	my $kibou1 = $get_data{'kibou1'};
	my $kibou2 = $get_data{'kibou2'};
	my $kibou3 = $get_data{'kibou3'};
	my $kigyoumei1 = $get_data{'kigyoumei1'};
	my $kigyoumei2 = $get_data{'kigyoumei2'};
	my $kigyoumei3 = $get_data{'kigyoumei3'};
	my $nainaitei1 = $get_data{'nainaitei1'};
	my $nainaitei2 = $get_data{'nainaitei2'};
	my $nainaitei3 = $get_data{'nainaitei3'};
	my $riyuu1 = $get_data{'riyuu1'};
	my $riyuu2 = $get_data{'riyuu2'};
	my $riyuu3 = $get_data{'riyuu3'};
	my $katsudou1 = $get_data{'katsudou1'};
	my $katsudou2 = $get_data{'katsudou2'};
	my $katsudou3 = $get_data{'katsudou3'};
	my $last_update = localtime;

	eval{
		$db->do( "UPDATE users2 SET lab=\'$lab\', seibetsu=\'$seibetsu\', naisen=\'$naisen\', email=\'$email\', addr=\'$addr\', kisei=\'$kisei\', tel=\'$tel\', keitai=\'$keitai\', kibou1=\'$kibou1\', kibou2=\'$kibou2\', kibou3=\'$kibou3\', kigyoumei1=\'$kigyoumei1\', kigyoumei2=\'$kigyoumei2\', kigyoumei3=\'$kigyoumei3\', nainaitei1=\'$nainaitei1\', nainaitei2=\'$nainaitei2\', nainaitei3=\'$nainaitei3\', riyuu1=\'$riyuu1\', riyuu2=\'$riyuu2\', riyuu3=\'$riyuu3\', katsudou1=\'$katsudou1\', katsudou2=\'$katsudou2\', katsudou3=\'$katsudou3\', last_update=\'$last_update\' where gakuseki=\'$gakuseki\'" );
		$db->commit();
	};
	if( $@ ){
		$errormessage = "Transaction aborted because $@\n\n\n";
		$db->rollback;
	}

	$db->disconnect();

	open( IN, "researchsuc.htm" );
}

$out = $http_header;

while( <IN> ){
	$out .= $_;
}

close( IN );


$out =~ s/<%errormessage%>/$errormessage/g;
$out =~ s/<%gakuseki%>/$gakuseki/g;
$out =~ s/<%password%>/$password/g;
print $out;
