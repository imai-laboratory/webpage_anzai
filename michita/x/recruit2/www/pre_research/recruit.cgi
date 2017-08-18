#!/usr/local/perl-5.8.3/bin/perl
use strict;
use DBI;
require 'cgi-lib.pl';

# $out : 出力する文字列
my $out="";
my $http_header = "Content-type: text/html\n\n";
my $errormessage="";
# データの取り出し
my %recvdata;
&ReadParse (\%recvdata);
my $stage = $recvdata{'stage'};

# postgresに接続
my $dbh;
my $sth;
#$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','pgsql')||die $dbh->errstr;
#$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','nobody')||die $dbh->errstr;
$dbh = DBI->connect ('DBI:Pg:dbname=shushoku','postgres')||die $dbh->errstr;

# クッキー読み込み
my $cookie=$ENV{'HTTP_COOKIE'};
my $userid=(split( "=", $cookie ))[1];
if ($userid eq ""){
# クッキーがない
	$out.=$http_header;
	$out.=$ENV{'HTTP_COOKIE'};
	open(IN, "expire.html");
	while (<IN>) { $out.=$_; }
	close(IN);
}
else{
# クッキーがある
my $template.=$http_header;

# 変更
if ($stage eq "modify"){
	my $mykibou1;
	my $mykibou2;
	my $mykibou3;
	$sth = $dbh->prepare("SELECT kibou1,kibou2,kibou3 from users where userid=\'$userid\'");
	$dbh->{AutoCommit} = 0; $dbh->{RaiseError} = 1;
	$sth->execute();
	my @arr = $sth->fetchrow;
	$mykibou1=@arr[0];
	$mykibou2=@arr[1];
	$mykibou3=@arr[2];
	
	my $time = localtime;
	my $kibou1 = $recvdata{'kibou1'};
	my $kibou2 = $recvdata{'kibou2'};
	my $kibou3 = $recvdata{'kibou3'};
	

	my $dbh2;
#	$dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','pgsql')||die $dbh2->errstr;
#	$dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','nobody')||die $dbh2->errstr;
	$dbh2 = DBI->connect ('DBI:Pg:dbname=shushoku','postgres')||die $dbh2->errstr;
	$dbh2->{AutoCommit} = 0; $dbh2->{RaiseError} = 1;

	eval{
		$dbh2->do("UPDATE users SET kibou1=\'$kibou1\', kibou2=\'$kibou2\', kibou3=\'$kibou3\', last_modified=\'$time\' where userid=\'$userid\'");
		$dbh2->commit();

		my $tmp1;
		my $tmp2;
		my $tmp3;

		# 前の希望の更新
		# 行の数え上げ。。。。遅そう
		$sth = $dbh2->prepare("SELECT * from users where kibou1=\'$mykibou1\'");$sth->execute();$tmp1=$sth->rows;
		$sth = $dbh2->prepare("SELECT * from users where kibou2=\'$mykibou2\'");$sth->execute();$tmp2=$sth->rows;
		$sth = $dbh2->prepare("SELECT * from users where kibou3=\'$mykibou3\'");$sth->execute();$tmp3=$sth->rows;
		$dbh2->do("UPDATE company SET kibou1=\'$tmp1\' where id=\'$mykibou1\'");
		$dbh2->do("UPDATE company SET kibou2=\'$tmp2\' where id=\'$mykibou2\'");
		$dbh2->do("UPDATE company SET kibou3=\'$tmp3\' where id=\'$mykibou3\'");

		# あたらしい希望の更新
		$sth = $dbh2->prepare("SELECT * from users where kibou1=\'$kibou1\'");$sth->execute();$tmp1=$sth->rows;
		$sth = $dbh2->prepare("SELECT * from users where kibou2=\'$kibou2\'");$sth->execute();$tmp2=$sth->rows;
		$sth = $dbh2->prepare("SELECT * from users where kibou3=\'$kibou3\'");$sth->execute();$tmp3=$sth->rows;
		$dbh2->do("UPDATE company SET kibou1=\'$tmp1\' where id=\'$kibou1\'");
		$dbh2->do("UPDATE company SET kibou2=\'$tmp2\' where id=\'$kibou2\'");
		$dbh2->do("UPDATE company SET kibou3=\'$tmp3\' where id=\'$kibou3\'");
		$dbh2 -> commit;
	};
	if ($@) {
		$errormessage = "Transaction aborted because $@\n\n\n";
		$errormessage.= %recvdata;
		$dbh2->rollback;
	}
	$dbh2->disconnect;
}

# テンプレートファイル読み込み
open(IN, "tmp.html");
while (<IN>) { $template.=$_; }
close(IN);

my @arr;
$sth = $dbh->prepare("SELECT userid from users where kibou1<>0");
$sth->execute();
my $sankasya = $sth->rows;
$template=~s/<%sankasya%>/$sankasya/g;

my @arr;
$sth = $dbh->prepare("SELECT username,last_login,last_modified from users where userid=\'$userid\'");
$sth->execute();
my @arr=$sth->fetchrow;
my $username=$arr[0];
my $last_login=$arr[1];
my $last_modified=$arr[2];
$template=~s/<%username%>/$username/g;
$template=~s/<%userid%>/$userid/g;
$template=~s/<%last_login%>/$last_login/g;
$template=~s/<%last_modified%>/$last_modified/g;


# 企業読み込み
my $mykibou1;
my $mykibou2;
my $mykibou3;
$sth = $dbh->prepare("SELECT kibou1,kibou2,kibou3 from users where userid=\'$userid\'");
$sth->execute();
my @arr = $sth->fetchrow;
$mykibou1=@arr[0];
$mykibou2=@arr[1];
$mykibou3=@arr[2];

$sth = $dbh->prepare("SELECT * from company where id<3 order by id");
$sth->execute();
my @arr;
my $i=0;
my $companynum=0;
my $data="";
#my (@company_id, @company_name, @company_category, @company_max, @company_kibou1, @company_kibou2, @company_kibou3);
my (@company_id, @company_name, @company_category, @company_max, @company_bikou, @company_kibou1, @company_kibou2, @company_kibou3);
while(@arr = $sth->fetchrow){
	@company_id[$i] = @arr[0];
	@company_name[@company_id[$i]] = @arr[1];
	@company_category[@company_id[$i]] = @arr[2];
	@company_max[@company_id[$i]] = @arr[3];
	@company_bikou[@company_id[$i]] = @arr[4];
#	@company_kibou1[@company_id[$i]] = @arr[4];
#	@company_kibou2[@company_id[$i]] = @arr[5];
#	@company_kibou3[@company_id[$i]] = @arr[6];
	@company_kibou1[@company_id[$i]] = @arr[5];
	@company_kibou2[@company_id[$i]] = @arr[6];
	@company_kibou3[@company_id[$i]] = @arr[7];
	$companynum++;
	$i++;
}

if ($stage eq "sort"){
	my $sortby = $recvdata{'sortby'};

	if ($sortby eq "id"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by id asc");
	}
	elsif ($sortby eq "company_name"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by name asc, id asc");
	}
	elsif ($sortby eq "category"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by category asc, id asc");
	}
	elsif ($sortby eq "max"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by max desc, id asc");
	}
	elsif ($sortby eq "kibou1"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by kibou1 desc, kibou2 desc, kibou3 desc, id asc");
	}
	elsif ($sortby eq "kibou2"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by kibou2 desc, kibou1 desc, kibou3 desc, id asc");
	}
	elsif ($sortby eq "kibou3"){
		$sth = $dbh->prepare("SELECT * from company where id>=3 order by kibou3 desc, kibou1 desc, kibou2 desc, id asc");
	}

}
else{
	$sth = $dbh->prepare("SELECT * from company where id>=3 order by id asc");
}
$sth->execute();
while(@arr = $sth->fetchrow){
	@company_id[$i] = @arr[0];
	@company_name[@company_id[$i]] = @arr[1];
	@company_category[@company_id[$i]] = @arr[2];
	@company_max[@company_id[$i]] = @arr[3];
	@company_bikou[@company_id[$i]] = @arr[4];
#	@company_kibou1[@company_id[$i]] = @arr[4];
#	@company_kibou2[@company_id[$i]] = @arr[5];
#	@company_kibou3[@company_id[$i]] = @arr[6];
	@company_kibou1[@company_id[$i]] = @arr[5];
	@company_kibou2[@company_id[$i]] = @arr[6];
	@company_kibou3[@company_id[$i]] = @arr[7];
	$companynum++;
	$i++;
}

# 選択ボックス作成
$template=~s/<%mykibou1%>/<a href=\#$mykibou1>$mykibou1: @company_name[$mykibou1]<\/a>/g;
$template=~s/<%mykibou2%>/<a href=\#$mykibou2>$mykibou2: @company_name[$mykibou2]<\/a>/g;
$template=~s/<%mykibou3%>/<a href=\#$mykibou3>$mykibou3: @company_name[$mykibou3]<\/a>/g;

$data="<select name=\"kibou1\" class=company>\n";
for ($i=0;$i<$companynum;$i++){
	if ($mykibou1 eq $company_id[$i]){
		$data.="<option selected value=\"@company_id[$i]\">@company_id[$i]: @company_name[@company_id[$i]]\n";
	}else{
	$data.="<option value=\"@company_id[$i]\">@company_id[$i]: @company_name[@company_id[$i]]\n";
	}
}
$data.="</select>";
$template=~s/<%kibou1%>/$data/g;
$data="<select name=\"kibou2\" class=company>\n";
for ($i=0;$i<$companynum;$i++){
	if ($mykibou2 eq $company_id[$i]){
		$data.="<option selected value=\"@company_id[$i]\">@company_id[$i]: @company_name[@company_id[$i]]\n";
	}else{
	$data.="<option value=\"@company_id[$i]\">@company_id[$i]: @company_name[@company_id[$i]]\n";
	}
}
$data.="</select>";
$template=~s/<%kibou2%>/$data/g;
$data="<select name=\"kibou3\" class=company>\n";
for ($i=0;$i<$companynum;$i++){
	if ($mykibou3 eq $company_id[$i]){
		$data.="<option selected value=\"@company_id[$i]\">@company_id[$i]: @company_name[@company_id[$i]]\n";
	}else{
	$data.="<option value=\"@company_id[$i]\">@company_id[$i]: @company_name[@company_id[$i]]\n";
	}
}
$data.="</select>";
$template=~s/<%kibou3%>/$data/g;


# 表作成

my @category=('進学','推薦','自由','推薦<br>(人数不明)');
$i=1;
#$data="<tr><td class=data_singaku ><a name=@company_id[$i]>@company_id[$i]</a></td><td class=data_singaku_name>@company_name[@company_id[$i]]</td><td class=data_singaku >$category[$company_category[@company_id[$i]]]</td><td class=data_singaku >-</td><td class=data_singaku >@company_kibou1[@company_id[$i]]</td><td class=data_singaku >@company_kibou2[@company_id[$i]]</td><td class=data_singaku >@company_kibou3[@company_id[$i]]</td></tr>\n";
$data="<tr><td class=data_singaku ><a name=@company_id[$i]>@company_id[$i]</a></td><td class=data_singaku_name>@company_name[@company_id[$i]]</td><td class=data_singaku >$category[$company_category[@company_id[$i]]]</td><td class=data_singaku >-</td><td class=data_singaku >@company_kibou1[@company_id[$i]]</td><td class=data_singaku >@company_kibou2[@company_id[$i]]</td><td class=data_singaku >@company_kibou3[@company_id[$i]]</td><td class=data_singaku>@company_bikou[@company_id[$i]]</td></tr>\n";
$template=~s/<%singaku1%>/$data/g;

$i=2;
#$data="<tr><td class=data_singaku ><a name=@company_id[$i]>@company_id[$i]</a></td><td class=data_singaku_name>@company_name[@company_id[$i]]</td><td class=data_singaku >$category[@company_category[@company_id[$i]]]</td><td class=data_singaku >-</td><td class=data_singaku >@company_kibou1[@company_id[$i]]</td><td class=data_singaku >@company_kibou2[@company_id[$i]]</td><td class=data_singaku >@company_kibou3[@company_id[$i]]</td></tr>\n";
$data="<tr><td class=data_singaku ><a name=@company_id[$i]>@company_id[$i]</a></td><td class=data_singaku_name>@company_name[@company_id[$i]]</td><td class=data_singaku >$category[@company_category[@company_id[$i]]]</td><td class=data_singaku >-</td><td class=data_singaku >@company_kibou1[@company_id[$i]]</td><td class=data_singaku >@company_kibou2[@company_id[$i]]</td><td class=data_singaku >@company_kibou3[@company_id[$i]]</td><td class=data_singaku>@company_bikou[@company_id[$i]]</td></tr>\n";
$template=~s/<%singaku2%>/$data/g;

$data="";
$i=3;
while($i<$companynum){

	my $icon1="";
	my $icon2="";
	my $icon3="";
	if (@company_category[@company_id[$i]]==1){
		if (@company_kibou1[@company_id[$i]]<@company_max[@company_id[$i]]*0.7) {
			$icon1=" <img src=icon_01.gif alt=\"○\">";
		}
		elsif (@company_kibou1[@company_id[$i]]<@company_max[@company_id[$i]]) {
			$icon1=" <img src=icon_02.gif alt=\"△\">";
		}else{
			$icon1=" <img src=icon_03.gif alt=\"×\">";
		}
		if (@company_kibou2[@company_id[$i]]+@company_kibou1[@company_id[$i]]<@company_max[@company_id[$i]]*0.7) {
			$icon2=" <img src=icon_01.gif alt=\"○\">";
		}
		elsif (@company_kibou2[@company_id[$i]]+@company_kibou1[@company_id[$i]]<@company_max[@company_id[$i]]) {
			$icon2=" <img src=icon_02.gif alt=\"△\">";
		}else{
			$icon2=" <img src=icon_03.gif alt=\"×\">";
		}
		if (@company_kibou3[@company_id[$i]]+@company_kibou2[@company_id[$i]]+@company_kibou1[@company_id[$i]]<@company_max[@company_id[$i]]*0.7) {
			$icon3=" <img src=icon_01.gif alt=\"○\">";
		}
		elsif (@company_kibou3[@company_id[$i]]+@company_kibou2[@company_id[$i]]+@company_kibou1[@company_id[$i]]<@company_max[@company_id[$i]]) {
			$icon3=" <img src=icon_02.gif alt=\"△\">";
		}else{
			$icon3=" <img src=icon_03.gif alt=\"×\">";
		}
	}
#	$data.="<tr><td class=data_syusyoku ><a name=@company_id[$i]>@company_id[$i]</a></td><td class=data_syusyoku_name>@company_name[@company_id[$i]]</td><td class=data_syusyoku >$category[@company_category[@company_id[$i]]]</td><td class=data_syusyoku >@company_max[@company_id[$i]]</td><td class=data_syusyoku >@company_kibou1[@company_id[$i]]$icon1</td><td class=data_syusyoku >@company_kibou2[@company_id[$i]]$icon2</td><td class=data_syusyoku >@company_kibou3[@company_id[$i]]$icon3</td></tr>\n";
	$data.="<tr><td class=data_syusyoku ><a name=@company_id[$i]>@company_id[$i]</a></td><td class=data_syusyoku_name>@company_name[@company_id[$i]]</td><td class=data_syusyoku >$category[@company_category[@company_id[$i]]]</td><td class=data_syusyoku >@company_max[@company_id[$i]]</td><td class=data_syusyoku >@company_kibou1[@company_id[$i]]$icon1</td><td class=data_syusyoku >@company_kibou2[@company_id[$i]]$icon2</td><td class=data_syusyoku >@company_kibou3[@company_id[$i]]$icon3</td><td class=data_syusyoku_name>@company_bikou[@company_id[$i]]</td></tr>\n";
	$i++;
} $template=~s/<%company%>/$data/g;



$out.=$template;
}
$out=~s/<%errormessage%>/$errormessage/g;
print $out;
# print %recvdata;
$sth->finish();
$dbh->disconnect();
