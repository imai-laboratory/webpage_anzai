#!/usr/local/bin/perl
use strict;
use DBI;
require 'cgi-lib.pl';
my $sth;
my $tmp1;
#	my $dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','pgsql');
	my $dbh2 = DBI->connect ('DBI:Pg:dbname=recruit','cosmos');
	
	$sth = $dbh2->prepare("SELECT * from users where kibou1='0'");
	$sth->execute();$tmp1=$sth->rows;
	print "///" . $tmp1;
