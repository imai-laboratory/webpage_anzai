#!/usr/local/bin/perl

#=====================================================================
# $BBjL\(B
#=====================================================================
#   $BL>(B    $B>N(B: WwwMail Ver3.27
#   $B:G=*99?7(B: 2008$BG/(B1$B7n(B14$BF|(B
#   $B:n(B $B@.(B $B<T(B: $BENJc!9(B
#   $B<o(B    $BJL(B: $B%U%j!<%=%U%H!J;dMQ!&>&MQ$rLd$o$:MxMQ!&2~B$!&N.MQ!&:FG[I[2D!K(B
#   $B:G(B $B?7(B $BHG(B: http://tohoho.wakusei.ne.jp/

#=====================================================================
# $B%+%9%?%^%$%:(B
#=====================================================================
# $B!z(B perl$B$N%Q%9L>(B
#    $B$3$N%U%!%$%k$N@hF,$N#19T$r!"$"$J$?$,MxMQ$9$k%5!<%P!<$K%$%s%9%H!<(B
#    $B%k$5$l$?(B perl $B%3%^%s%I$N%Q%9L>$K1~$8$FJQ99$7$F$/$@$5$$!#Nc$($P!"(B
#    $B;d$,2CF~$7$F$$$k(B BIGLOBE $B$G$O!"(B#!/usr/local/bin/perl $B$H$J$j$^$9!#(B
#    $B2r$i$J$$>l9g$O!"%W%m%P%$%@$d%5!<%P$N4IM}<T$K$*Ld$$9g$o$;$/$@$5$$!#(B
#   $B!V(B#!$B!W$NA0$K$O!"6uJ8;z$d6u9T$dB>$NJ8;z$,$O$$$i$J$$$h$&$K$7$F$/$@$5$$!#(B

# $B!z(B $BAw?.@h%a!<%k%"%I%l%9(B
#    $mailto = 'abc@xxx.yyy.zzz'; $B$N$h$&$K$"$J$?$N%a!<%k%"%I%l%9$K(B
#    $B=q$-49$($F$/$@$5$$!#(B
$mailto = 'infoproc@ayu.ics.keio.ac.jp';

# $B!z(B $B%5%V%8%'%/%H(B($B7oL>(B)
#    $BAw?.$5$l$k%a!<%k$N%5%V%8%'%/%H$r;XDj$7$F$/$@$5$$!#(B
$subject = '[infoproc]080425';

# $B!z(B $B%a!<%kAw?.%3%^%s%I(B
#    Web$B%5!<%P!<$,(BUNIX$B$N>l9g$O(Bsendmail$B%3%^%s%I!"(BWindows$B7O$N>l9g$O(BBLATJ.EXE
#    $B%3%^%s%I$N%Q%9L>$r;XDj!J(B$mailcmd = 'C:\BLATJ\BLATJ.EXE'; $B$J$I!K$7$F$/(B
#    $B$@$5$$!#$3$N%3%^%s%I$,B8:_$7$J$$>l9g$O!"(BWwwMail $B$OF0:n$7$^$;$s!#$^$?!"(B
#    $BB8:_$7$F$$$F$b!"%a!<%kAw?.$N@_Dj$,9T$o$l$F$$$J$$>l9g$,$"$j$^$9!#>\:Y(B
#    $B$O%W%m%P%$%@$d%5!<%P!<$N4IM}<T$K$*Ld$$9g$o$;$/$@$5$$!#(B
$mailcmd = '/usr/lib/sendmail';

# $B!z(B $BAw?.7k2L%a%C%;!<%8(B($B%X%C%@(B)
#    <<END_OF_DATA $B!A(B END_OF_DATA $B$N4V$r9%$_$K$"$o$;$FJQ99$7$F$/$@$5$$!#(B
$header = <<END_OF_DATA;
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=Shift_JIS">
<title>restult</title>
</head>
<body>
<h1>Finish</h1>
<hr>
<hr>
END_OF_DATA

# $B!z(B $BAw?.7k2L%a%C%;!<%8(B($B%U%C%?(B)
#    <<END_OF_DATA $B!A(B END_OF_DATA $B$N4V$r9%$_$K$"$o$;$FJQ99$7$F$/$@$5$$!#(B
$footer = <<END_OF_DATA;
</body>
</html>
END_OF_DATA

#====================================================================
# $B<+8J?GCG5!G=!#(B
#====================================================================
# $B%a!<%kAw?.$,$&$^$/F0:n$7$J$$;~$K!"(B
# http://$B!A(B/$B!A(B/wwwmail.cgi?test $B$N7A<0$G8F$S=P$7$F$/$@$5$$!#(B
if ($ENV{'REQUEST_METHOD'} eq "GET") {
	print "Content-type: text/html; charset=Shift_JIS\n";
	print "\n";
	print "<html>\n";
	print "<head>\n";
	print "<title>WwwMail</title>\n";
	print "</head>\n";
	print "<body>\n";
	print "<p>CGI is OK</p>\n";
	unless (-f $mailcmd) {
		print "<p>No $mailcmd</p>\n";
	}
	unless (-x $mailcmd) {
		print "<p>Cannot execute $mailcmd</p>\n";
	}
	unless (-f "jcode.pl") {
		print "<p>No jcode.pl</p>\n";
	}
	unless (-f "mimew.pl") {
		print "<p>No mimew.pl</p>\n";
	}
	print "</body>\n";
	print "</html>\n";
	exit 0;
}

#====================================================================
# $BK\BN(B
#====================================================================

#
# $B%i%$%V%i%j$N8F$S=P$7(B
#
require "jcode.pl";
require "mimew.pl";

#
# $BF~NOCM$rFI$_<h$k(B
#
if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $query_string, $ENV{'CONTENT_LENGTH'});
	@a = split(/&/, $query_string);
	foreach $x (@a) {
		($name, $value) = split(/=/, $x);
		$name =~ tr/+/ /;
		$name =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		&jcode'convert(*name, "jis");
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$value =~ s/\r\n/\n/g;
		&jcode'convert(*value, "jis");
		if ($FORM{$name} eq "") {
			$FORM{$name} = $value;
			$FORM[$cnt++] = $name;
		} else {
			$FORM{$name} .= (" " . $value);
		}
	}
}

#
# EMAIL$B$,@5>o$J%a!<%k$"$I$l$9$+$I$&$+H=CG$9$k(B
#
if ($FORM{'EMAIL'} =~ /^[-_\.a-zA-Z0-9]+\@[-_\.a-zA-Z0-9]+$/) {
	$mailfrom = $FORM{'EMAIL'};
}

#
# $B%a!<%k%X%C%@$r:n@.$9$k(B
#
{
	&jcode'convert(*subject, "jis");
	$mailhead = "";
	$mailhead .= "Content-Type: text/plain; charset=\"iso-2022-jp\"\n";
	$mailhead .= "Content-Transfer-Encoding: 7bit\n";
	$mailhead .= "MIME-Version: 1.0\n";
	$mailhead .= "To: $mailto\n";
	if ($mailfrom) {
		$mailhead .= "From: $FORM{'EMAIL'}\n";
#		$mailhead .= "Cc: $FORM{'EMAIL'}\n";
	} else {
		$mailhead .= "From: $mailto\n";
	}
	$mailhead .= "Subject: $subject\n";
	$mailhead .= "\n";
}

#
# $B%a!<%k%\%G%#$r:n@.$9$k(B
#
{
	for ($i = 0; $i < $cnt; $i++) {
		$mailbody .= "$FORM[$i] = $FORM{$FORM[$i]}\n";
	}

	# "." $B$N$_$N9T$O(B ". " $B$KJQ49$9$k!#(B
	# 2$B2s7+$jJV$5$J$$$H!"(B2$B9TO"B3$G(B "." $B$N$_$N9T$KBP1~$G$-$J$$(B
	# "." $B$r(B ".." $B$KJQ49$9$k=hM}$,0lHLE*$@$=$&$@$,!"$"$($F!"(B
	# "." $B$r(B ". " $B$KJQ49$9$k!#(B
	$mailbody =~ s/(^|\n)\.(\n|$)/$1. $2/g;
	$mailbody =~ s/(^|\n)\.(\n|$)/$1. $2/g;
}

#
# $B%a!<%k$rAw?.$9$k(B
#
if ($mailcmd =~ /sendmail/) {
	unless (open(OUT, "| $mailcmd -t")) {
		&errexit("cannot send (1)");
	}
	unless (print OUT &mimeencode($mailhead)) {
		&errexit("cannot send (2)");
	}
	unless (print OUT $mailbody) {
		&errexit("cannot send (3)");
	}
	close(OUT);
} elsif ($mailcmd =~ /BLAT/i) {
	&jcode'convert(*subject, "sjis");
	$cmd = "$mailcmd";
	$cmd .= " -";
	$cmd .= " -t $mailto";
	$cmd .= " -s \"$subject\"";
	if ($mailfrom) {
		$cmd .= " -c $mailfrom";
		$cmd .= " -f $mailfrom";
	}
	unless (open(OUT, "| $cmd > NUL:")) {
		&errexit("cannot send (4)");
	}
	&jcode'convert(*mailbody, "sjis");
	unless (print OUT $mailbody) {
		&errexit("cannot send (5)");
	}
	&jcode'convert(*mailbody, "jis");
	close(OUT);
} else {
	&errexit("No $mailcmd");
}

#
# $B%V%i%&%62hLL$KAw?.7k2L$r=q$-=P$9(B
#
{
	&jcode'convert(*header, "sjis");
	&jcode'convert(*footer, "sjis");

	$mail = $mailhead . $mailbody;
	&jcode'convert(*mail, "euc");
	$mail =~ s/&/&amp;/g;
	$mail =~ s/"/&quot;/g;
	$mail =~ s/</&lt;/g;
	$mail =~ s/>/&gt;/g;
	$mail =~ s/\n/<BR>/g;
	&jcode'convert(*mail, "sjis");

	print "Content-type: text/html\n";
	print "\n";
	print "$header\n";
#	print "$mail\n";
	print "$footer\n";
}

#
# $B%(%i!<%a%C%;!<%8$r=PNO$7$F=*N;(B
#
sub errexit {
	local($err) = @_;
	local($msg);

	$msg  = "Content-type: text/html\n";
	$msg .= "\n";
	$msg .= "<html>\n";
	$msg .= "<head>\n";
	$msg .= "<meta http-equiv=\"Content-type\" content=\"text/html; charset=Shift_JIS\">\n";
	$msg .= "<title>Result</title>\n";
	$msg .= "</head>\n";
	$msg .= "<body>\n";
	$msg .= "<h1>Result</h1>\n";
	$msg .= "<hr>\n";
	$msg .= "<p>$err</p>\n";
	$msg .= "<hr>\n";
	$msg .= "</body>\n";
	$msg .= "</html>\n";

	&jcode'convert(*msg, "sjis");

	print $msg;

	exit(0);
}
