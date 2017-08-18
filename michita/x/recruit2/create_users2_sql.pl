#! /usr/local/perl5/bin/perl5


if( @ARGV != 1 ){
	print "Usage: create_sql.pl data.csv\n";
	exit;
}


if( !open( SRC, "$ARGV[0]" )){
	exit;
}


print "drop table users2\;\n";
print "create table users2 ( gakuseki text not null unique, password text not null, username text not null, gakunen int not null, lab text default \'\', seibetsu int default 0, naisen text default \'\', email text default \'\', addr text default \'\', kisei text default \'\', tel text default \'\', keitai text default \'\', kibou1 int default 0, kibou2 int default 0, kibou3 int default 0 , kigyoumei1 text default \'\', kigyoumei2 text default \'\', kigyoumei3 text default \'\', nainaitei1 int default 0, nainaitei2 int default 0, nainaitei3 int default 0,riyuu1 text default \'\', riyuu2 text default \'\', riyuu3 text default \'\', katsudou1 text default \'\', katsudou2 text default \'\', katsudou3 text default \'\', last_update text default \'\' not null, last_update2 text default \'\' not null, suisensho int default 0 )\;\n\n";


while( <SRC> ){
	chomp;
	split( /,/ );

	print "insert into users2 values (\'$_[1]\',\'$_[4]\',\'$_[2]\', $_[0], \'$_[3]\')\;\n";
}

close( SRC );
