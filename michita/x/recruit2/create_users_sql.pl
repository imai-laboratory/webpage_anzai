#! /usr/local/perl5/bin/perl5


if( @ARGV != 1 ){
	print "Usage: create_sql.pl data.csv\n";
	exit;
}


if( !open( SRC, "$ARGV[0]" )){
	exit;
}


print "drop table users\;\n";
print "create table users ( userid text not null unique, password text not null , username text not null , kibou1 int default 0, kibou2 int default 0, kibou3 int default 0, now_last_login text default \'\' not null, last_login text default \'\' not null, last_modified text default \'\' not null)\;\n\n";


while( <SRC> ){
	chomp;
	split( /,/ );

	print "insert into users values (\'$_[1]\',\'$_[4]\',\'$_[2]\')\;\n";
}

close( SRC );
