#!/usr/local/bin/perl
use strict;
use DBI;
require 'cgi-lib.pl';

# $out : ���Ϥ���ʸ����
my $out="";
my $http_header = "Content-type: text/html\n\n";
my $errormessage;

# �ǡ����μ��Ф�
my %recvdata;
&ReadParse (\%recvdata);
my $stage = $recvdata{'stage'};

# postgres����³
my $dbh;
my $sth;
#$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','pgsql')||die $dbh->errstr;
#$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','nobody')||die $dbh->errstr;
#$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','postgres')||die $dbh->errstr;
$dbh = DBI->connect ('DBI:Pg:dbname=recruit','nobody')||die $dbh->errstr;
# userid �� password �γ�ǧ
my $userid = $recvdata{'userid'};
my $password = $recvdata{'password'};
#$sth = $dbh->prepare("SELECT password, now_last_login from users where userid=\'$userid\'");
$sth = $dbh->prepare("SELECT password, now_last_login from users2 where userid=\'$userid\'");
$sth->execute();
my @arr=$sth->fetchrow;
my $pass=$arr[0];
my $last_login = $arr[1];

if ($password ne $pass || $password eq "" || $userid eq ""){
# �ѥ���ɤ����פ��ʤ�
	$out.=$http_header;
	open(IN, "loginerr.html");
	while (<IN>) { $out.=$_; }
	close(IN);}
else{
# �ѥ���ɤ����פ���
	$out.="Set-Cookie: userid=$userid;\n".$http_header;
	open(IN, "loginsuc.html");
	while (<IN>) { $out.=$_; }
	close(IN);
	
	# Last Login ����
#	my $dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','pgsql')||die $dbh->errstr;
#	my $dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','nobody')||die $dbh->errstr;
#	my $dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','postgres')||die $dbh->errstr;
	my $dbh2 = DBI->connect ('DBI:Pg:dbname=recruit','nobody')||die $dbh->errstr;
	my $time = localtime;
	eval{
		$dbh2->do("UPDATE users SET now_last_login=\'$time\',last_login=\'$last_login\' where userid=\'$userid\'");
		$dbh2->commit();
	};
	
	if ($@) {
		$errormessage = "Transaction aborted because $@\n\n\n";
		$errormessage.= %recvdata;
		$dbh2->rollback;
	}
	$dbh2->disconnect;
}

$out=~s/<%errormessage%>/$errormessage/g;
print $out;
$sth->finish();
$dbh->disconnect();
