#! /usr/local/perl5/bin/perl5


if( @ARGV != 1 ){
	print "Usage: create_sql.pl data.csv\n";
	exit;
}


if( !open( SRC, "$ARGV[0]" )){
	exit;
}


print "drop table company\;\n";
print "create table company ( id int not null unique , name text not null ,category int not null default 1, max int default 0, bikou text, kibou1 int default 0 , kibou2 int default 0, kibou3 int default 0)\;\n\n";

print "insert into company values (0,\'Ì¤ÁªÂò\',0,0)\;\n";
print "insert into company values (1,\'¿Ê³Ø - Çî»Î\',0,0)\;\n";
print "insert into company values (2,\'¿Ê³Ø - ½¤»Î\',0,0)\;\n";
print "insert into company values (3,\'¼«Í³±þÊç\',2,0)\;\n";

while( <SRC> ){
	chomp;
	split( /,/ );

	print "insert into company values ($_[1], \'$_[2]\',$_[4], $_[5], \'$_[6]\')\;\n";
}

close( SRC );
