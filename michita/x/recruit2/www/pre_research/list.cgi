#!/usr/local/perl-5.6.1/bin/perl
use strict;
use DBI;
require 'cgi-lib.pl';

# $out : ���Ϥ���ʸ����
my $out="";
my $http_header = "Content-type: text/html\n\n";
my $errormessage="";
# �ǡ����μ��Ф�
my %recvdata;
&ReadParse (\%recvdata);
my $stage = $recvdata{'stage'};

# postgres����³
my $dbh;
my $sth;
$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','pgsql')||die $dbh->errstr;

my $out.=$http_header;

my @arr;
my @userid;
my @username;
my @kibou1;
my @kibou2;
my @kibou3;
my @last_login;
my @last_modified;
my $usernum=0;
$sth = $dbh->prepare("SELECT userid,username,kibou1,kibou2,kibou3,last_login,last_modified from users order by userid");
$sth->execute();
my $i=0;
while(@arr=$sth->fetchrow){
	$userid[$i]=@arr[0];
	$username[$i]=@arr[1];
	$kibou1[$i]=@arr[2];
	$kibou2[$i]=@arr[3];
	$kibou3[$i]=@arr[4];
	$last_login[$i]=@arr[5];
	$last_modified[$i]=@arr[6];
	$i++;
}$usernum=$i;

my @company;
my @category;
my $company_maxid;
$sth = $dbh->prepare("SELECT id,name,category from company");
$sth->execute();
while(@arr=$sth->fetchrow){
	$company[@arr[0]]=@arr[1];
	$category[@arr[0]]=@arr[2];
	if ($company_maxid<@arr[0]){
		$company_maxid=@arr[0];
	}
}

$out.="<html><body><pre>";
$out.="ͽ��Ĵ�� �������ǤΥꥹ�� (CSV�ʤΤǡ��ڤä�Ž�ä�Excel���ɤ߹���Ǥ�������)\n\n";
$out.="�����ֹ�,̾��,��1��˾,��1��˾id,��2��˾,��2��˾id,��3��˾,��3��˾id\n";
for ($i=0;$i<$usernum;$i++){
	$out.="$userid[$i],$username[$i],$company[$kibou1[$i]],$kibou1[$i],$company[$kibou2[$i]],$kibou2[$i],$company[$kibou3[$i]],$kibou3[$i]\n";
}

$out.="</pre></body></html>";
print $out;
print %recvdata;
$sth->finish();
$dbh->disconnect();
