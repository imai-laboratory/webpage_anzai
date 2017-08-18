#!/usr/local/bin/perl

#===========================================================
# wwwboard: Version 2.52
# Copyright (C) 1997, 1999 �Ƃق� s-hasei@mtg.biglobe.ne.jp
# http://www2e.biglobe.ne.jp/~s-hasei/
# �t���[�\�t�g�E�Ĕz�z/����/���p�\�E���s�v
#===========================================================

#
# 1997.03.23 ����
# 1997.03.?? ���s�����s�Ƃ��Ĉ����悤�ɏC��
# 1997.04.10 ���ԑт������Ă��܂����Ƃ�������ɑΏ�
# 1997.04.20 �����^�O�������Ƌ����I�ɉ��s���}������Ă��܂����ɑΏ�
# 1997.05.11 �����l��300�s�Ɍ��炵��
# 1997.05.11 �u�ĕ`��v���u�ĕ\���v��
# 1997.05.11 �u�߂�v�{�^��������
# 1997.05.18 �u�`���v�ɉ���
# 1997.06.08 ���[���A�h���X����͂ł���悤�ɂ���
# 1997.06.15 �t�q�k����͂ł���悤�ɂ���
# 1997.06.15 �j����\������悤�ɂ���
# 1997.06.15 �����R�[�h�̕��������ɑΏ������B(jcode�̗p)
# 1997.07.06 10���ȏ�Â����b�N�t�@�C���͍폜����悤�ɂ���
# 1997.08.24 NN2.0�ŕ�����������o�O���C��
# 1997.10.19 ���Ȑf�f�@�\������
# 1997.11.09 HTML�^�O�������Ȃ��w����\�ɂ���
# 1998.04.12 x-sjis���w�肵�Ȃ��悤�ɂ���
# 1998.05.24 �����[�h���Ă���d�������݂��Ȃ��悤�ɂ���
# 1998.05.24 �A���p(&)�ƃN�H�[�g(")�������������Ȃ��悤�ɂ���
# 1998.05.25 ��d�������݋֎~��Netscape�T�[�o�[�œ����Ȃ������̂ňꎞ������
# 1998.08.02 </BODY></HTML>�̏����Y����C��
# 1998.11.08 SIGPIPE�Ώ��ƃG���[���̃��b�Z�[�W�ǉ�
# 1999.02.07 Ver2.52 2000�N�Ή�
#

#
# Maximum number of messages
#
$max_msgs = 120;

#
# Return URL
#
#$return_url = "http://www.mic.atr.co.jp/~michita/156_index.html";
$return_url = "http://www.yk.rim.or.jp/~michita/alfa/156_index4rim.html";
$jump_url = "http://www.yk.rim.or.jp/~michita/cgi-bin/eeeboard.cgi";
$read_url = "http://www.yk.rim.or.jp/~michita/alfa/board_frame.html";

#
# Allow HTML tags
#
$allow_html = 0;

#
# Set timezone
#
$ENV{'TZ'} = "JST-9";

#
# Remove lockfile when terminated by signal
#
###sub sigexit { rmdir("lock/wwwboard.loc"); exit(0); }
###$SIG{'PIPE'} = $SIG{'INT'} = $SIG{'HUP'} = $SIG{'QUIT'} = $SIG{'TERM'} = "sigexit";

#
# Constant variables
#
@wdays = ( "��", "��", "��", "��", "��", "��", "�y", "��" );

##########99/12/14
$message = "";
##########


############Cookeeee start
#
# Cookie�̒l�𓾂�
#
&getCookie();
$from = $COOKIE{'NAME'};
$from =~ s/<img src=(.*)>(.*)<img src=(.*)>/$2/;
$from =~ s/(.*)<img src=(.*)>/$1/; ### delete icon tag from FORM format.
$subject = $COOKIE{'SUBJECT'};
$mail = $COOKIE{'MAIL'};
$url = $COOKIE{'URL'};
############Cookeeee end


#
# Test mode
#
if ($ARGV[0] eq "test") {
	print "Content-type: text/html\n";
	print "\n";
	print "<HTML>\n";
	print "<HEAD>\n";
	print "<TITLE>wwwboard test</TITLE>\n";
	print "</HEAD>\n";
	print "<BODY TEXT=black BGCOLOR=white>\n";
	print "CGI�X�N���v�g�͐���ɓ��삵�Ă��܂��B\n";
	if (! -d "lock") {
		print "<BR>NG. lock�f�B���N�g�������݂��܂���B\n";
	} elsif (! -w "lock") {
		print "<BR>NG. lock�f�B���N�g���ɏ������݂��ł��܂���B\n";
	} elsif (-d "lock/wwwboard.loc") {
		print "<BR>NG. lock/wwwboard.loc ���c���Ă��܂��B\n";
	}
	if (! -f "wwwboard.dat") {
		print "<BR>NG. wwwboard.dat �����݂��܂���B\n";
	} elsif (! -w "wwwboard.dat") {
		print "<BR>NG. wwwboard.dat �ɏ������݂ł��܂���B\n";
	}
	if (! -f "wwwboard.tmp") {
		print "<BR>NG. wwwboard.tmp �����݂��܂���B\n";
	} elsif (! -w "wwwboard.tmp") {
		print "<BR>NG. wwwboard.tmp �ɏ������݂ł��܂���B\n";
	}
	print "</BODY>\n";
	print "</HTML>\n";
	exit(0);
}

#
# Japanese KANJI code
#
if (-f "jcode.pl") {
	$jflag = true;
	require "jcode.pl";
	$code = ord(substr("��", 0, 1));
	if ($code == 0xb4) {
		$ccode = "euc";
		$hcode = "x-euc-jp";
	} elsif ($code == 0x1b) {
		$ccode = "jis";
		$hcode = "iso-2022-jp";
	} else {
		$ccode = "sjis";
		$hcode = "x-sjis";
	}
}

#
# Read variables
#
if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $query_string, $ENV{'CONTENT_LENGTH'});
	@a = split(/&/, $query_string);
	foreach $x (@a) {
		($name, $value) = split(/=/, $x);
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		if ($allow_html) {
			$value =~ s/<!--/&lt;!--/g;
			$value =~ s/-->/--&gt;/g;
		} else {
########99/12/14
		    if ($name ne "NUMBER"){
##############
			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
################################ By Linta 99/09/16
                        if ($name eq "FROM"){

		            if ($jflag) {
			       &jcode'convert(*value, $ccode);
		            }

			    $value =~ s/�͂��݂�/�͂��݂�<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/kuma\.gif\">/g;
			    $value =~ s/�����/�����<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/hebi\.gif\">/g;
			    $value =~ s/�_�~�A��/�_�~�A��<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/life1\.gif\"height=\"45\" width=\"45\">/g;
			    $value =~ s/�҂��/�҂��<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/rabbit\.gif\">/g;
			    $value =~ s/hide/hide<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/horse\.gif\">/g;
			    $value =~ s/POKE/POKE<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/taki\.gif\">/g;
			    $value =~ s/Poke/<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/poke-f\.gif\">Poke<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/poke-b\.gif\">/g;
#			    $value =~ s/�o�n�j�d/<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/poke1\.gif\">�o�n�j�d<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/poke2\.gif\">/g;
			    $value =~ s/�o�n�j�d/<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/poke-f\.gif\">�o�n�j�d<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/poke-b\.gif\">/g;
			    $value =~ s/Yossy/Yossy<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/ninja\.gif\">/g;
			    $value =~ s/TA28/TA28<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/hebi2\.gif\">/g;
			    $value =~ s/HIRO/HIRO<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/rolex\.gif\">/g;
			    $value =~ s/�r�i�ȁj/�r�i�ȁj<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/baby\.gif\">/g;
			    $value =~ s/���ڂ���/���ڂ���<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/chusya\.gif\">/g;
			    $value =~ s/S.KUBO/S.KUBO<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/zou\.gif\">/g;
			    $value =~ s/�ق��ق�/�ق��ق�<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/maguro\.gif\">/g;
			    $value =~ s/Aquio/Aquio<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/flag\.gif\">/g;
			    $value =~ s/dada/dada<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/tie\.gif\">/g;
			    $value =~ s/TAQ/TAQ<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/checker\.gif\">/g;
			    $value =~ s/�r����/�r����<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/ninja2\.gif\">/g;
			    $value =~ s/�C(.*)�j/�C$1�j<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/shell\.gif\">/g;
			    $value =~ s/�E���p�p/<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/tyrell-1\.gif\">�E���p�p<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/tyrell-2\.gif\">/g;
			    $value =~ s/�킢���/�킢���<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/wine\.gif\">/g;
			    $value =~ s/�x��������/�x��������<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/racco\.gif\">/g;
			    $value =~ s/SYLPH/SYLPH<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/lillly\.gif\">/g;
			    $value =~ s/�g��������/�g��������<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/nose\.gif\">/g;
			    $value =~ s/Hide��/Hide��<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/nose\.gif\">/g;
			    $value =~ s/�킢���/�킢���<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/sungrass\.gif\">/g;
			    $value =~ s/����̏���/<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/cross\.gif\">����̏���<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/hebi3\.gif\">/g;
			    $value =~ s/sylbee/sylbee<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/bee\.gif\">/g;
			    $value =~ s/�Ղ������/�Ղ������<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/michelan\.gif\">/g;
			    $value =~ s/�Ղ�����/�Ղ�����<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/michelan\.gif\">/g;
			    $value =~ s/�͂񂾂����/�͂񂾂����<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/kaminari\.gif\">/g;
			    $value =~ s/Sei/Sei<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/manta\.gif\">/g;
			    $value =~ s/��(.*)�g��/��$1�g��<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/handle\.gif\">/g;
			    $value =~ s/��/��<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/pig\.gif\">/g;
			    $value =~ s/���������/���������<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/helmet\.gif\">/g;
			    $value =~ s/�r�D�j�t�a�n/�r�D�j�t�a�n<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/hat\.gif\">/g;
			    $value =~ s/�g������/�g������<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/frog\.gif\">/g;
			    $value =~ s/�͂���/�͂���<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/hajime\.gif\">/g;
			    $value =~ s/�c��������/�c��������<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/diamond\.gif\">/g;
			    $value =~ s/���Ɋ���/���Ɋ���<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/kani\.gif\">/g;
			    $value =~ s/�˂�/�˂�<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/cat\.gif\">/g;
			    $value =~ s/�Ԃ��Ԃ�/�Ԃ��Ԃ�<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/lion\.gif\">/g;
			    $value =~ s/koko/koko<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/moon\.gif\">/g;
			    $value =~ s/����/����<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/moon\.gif\">/g;
			    $value =~ s/�y�y����/�y�y����<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/peperon\.gif\">/g;
			    $value =~ s/�a�n�m�g/�a�n�m�g<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/star\.gif\">/g;
			    $value =~ s/kye/kye<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/kye\.gif\">/g;
			    $value =~ s/DaVinci/DaVinci<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/bbs\.gif\">/g;
			    $value =~ s/(.*)�P(.*)�P/$1�P$1�P<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/sensya\.gif\">/g;
			    $value =~ s/�Ƃ��V/�Ƃ��V<img src=\"http\:\/\/www.yk.rim.or.jp\/\~michita\/mark\/dronjo\.gif\">/g;
                        }




                        if ($name eq "MESSAGE"){


		            if ($jflag) {
			       &jcode'convert(*value, $ccode);
               		    }

                            $value2 = "";
                            @b = split(/^/, $value);
                  	    foreach $hoge_x (@b) {

        	$hoge_x =~ s/http:\/\/(.*)\r/<a href="http:\/\/$1">http:\/\/$1<\/a>\r/g;
        	$hoge_x =~ s/mailto:(.*)\r/<a href="mailto:$1">$1<\/a>\r/g;

        	$hoge_x =~ s/(w*|\s*)#(.*)\r/$1<font color=\"#af00ff\">��$2<\/font>\r/g;
        	$hoge_x =~ s/(\w*|\s*)&gt;(.*)\r/$1<font color=\"#00a0cf\">&gt;$2<\/font>\r/g;
        	$hoge_x =~ s/(.*)��(.*)\r/$1<font color=\"#00a0cf\">��$2<\/font>\r/g;
         	$hoge_x =~ s/(.*)��(.*)\r/$1<font color=\"#af00ff\">��$2<\/font>\r/g;
		$hoge_x =~ s/�����O:(.*)\r/<font color=\"#ff0000\">��$1<\/font>\r/g;

       	        $hoge_x =~ s/^(w*|\s*)#(.*)\r{,0}$/$1<font color=\"#af00ff\">��$2<\/font>/g;
        	$hoge_x =~ s/^(\w*|\s*)&gt;(.*)\r{0}$/$1<font color=\"#00a0cf\">&gt;$2<\/font>/g;
        	$hoge_x =~ s/^(.*)��(.*)\r{,0}$/$1<font color=\"#00a0cf\">��$2<\/font>/g;
         	$hoge_x =~ s/^(.*)��(.*)\r{,0}$/$1<font color=\"#af00ff\">��$2<\/font>/g;


#        	$hoge_x =~ s/^(w*|\s*)#(.*)\r/$1<font color=\"#af00ff\">��$2<\/font>\r/g;
#        	$hoge_x =~ s/^(\w*|\s*)&gt;(.*)\r/$1<font color=\"#00a0cf\">&gt;$2<\/font>\r/g;
#        	$hoge_x =~ s/^(.*)��(.*)\r/$1<font color=\"#00a0cf\">��$2<\/font>\r/g;
#         	$hoge_x =~ s/^(.*)��(.*)\r/$1<font color=\"#af00ff\">��$2<\/font>\r/g;
#		$hoge_x =~ s/^�����O:(.*)\r/<font color=\"#ff0000\">��$1<\/font>\r/g;

#        	$hoge_x =~ s/^(w*|\s*)#(.*)$/$1<font color=\"#af00ff\">��$2<\/font>/g;
#        	$hoge_x =~ s/^(\w*|\s*)&gt;(.*)$/$1<font color=\"#00a0cf\">&gt;$2<\/font>/g;
#        	$hoge_x =~ s/^(.*)��(.*)$/$1<font color=\"#00a0cf\">��$2<\/font>/g;
#         	$hoge_x =~ s/^(.*)��(.*)$/$1<font color=\"#af00ff\">��$2<\/font>/g;


                               $value2 = join('',$value2,$hoge_x);


              	            }
                            $value = $value2;


                       }



#                        if ($name eq "MESSAGE"){
#			     $value =~ s/#/<font color=\"#af00ff\">#/g;
#     			     $value =~ s/&gt;/<font color=\"#0000ff\">&gt;/g;
#			     $value =~ s/��/<font color=\"#0000ff\">��/g;
#			     $value =~ s/�����O:/<font color=\"#0000ff\">&gt;/g;
#			     $value =~ s/��/<font color=\"#af00ff\">��/g;
#               		     $value =~ s/\r/<\/font ><b>\r/g;
#                        }


#               		$value =~ s//<\/font >\r/g;
################################ 
		}

		if ($jflag) {
			&jcode'convert(*value, $ccode);
		}

##############################99/12/15
                if ($name eq "NUMBER"){
                   if($FORM{$name} ne ""){
		      $FORM{$name} = "$FORM{$name},$value";
                   } else {
		      $FORM{$name} = "$value";
                   }
		}
                else {
##############################
		    $FORM{$name} = $value;
##############################99/12/15
                } 
##############################
          }
	}

}

#
# Remove lockfile when terminated by signal
#
if ($FORM{'MESSAGE'} ne "") {
sub sigexit { rmdir("lock/wwwboard.loc"); exit(0); }
$SIG{'PIPE'} = $SIG{'INT'} = $SIG{'HUP'} = $SIG{'QUIT'} = $SIG{'TERM'} = "sigexit";
}


#
# File lock
#
if ($FORM{'MESSAGE'} ne "") {
foreach $i ( 1, 2, 3, 4, 5, 6 ) {
	if (mkdir("lock/wwwboard.loc", 755)) {
		last;
	} elsif ($i == 1) {
		($mtime) = (stat("lock/wwwboard.loc"))[9];
#		if ($mtime < time() - 600) {
		if ($mtime < time() - 300) {
			rmdir("lock/wwwboard.loc");
		}
	} elsif ($i < 6) {
		sleep(2);
	} else {
		print "Content-type: text/html\n";
		print "\n";
		print "<HTML>\n";
		print "<HEAD>\n";
		print "<TITLE>�f����</TITLE>\n";
		print "</HEAD>\n";
		print "<BODY>\n";
		print "<H1>�f����</H1>\n";
		print "<HR>\n";
		print "�����A�f�������G���Ă���܂��B���΂炭���҂��̏�A";
		print "�ēx�A�N�Z�X���肢���܂��B\n";
		print "<HR>\n";
		print "</BODY>\n";
		print "</HTML>\n";
		exit(1);
	}
}
}

#
# Write to date file
#
if ($FORM{'MESSAGE'} ne "") {

	#
	# Get date and time
	#
	($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst)
			= localtime(time);
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
		$year + 1900, $mon + 1, $mday, @wdays[$wday], $hour, $min);

        #GET Conter
        #
	
        if ( -f "wwwbcount.dat") {
                open(IN,"wwwbcount.dat");
                $count = <IN>;
               	close(IN);
              	$count++;
              	open(OUT, ">wwwbcount.dat");
              	print OUT "$count";
                close(OUT);
                $tmp_c = $count  % 1000;
                if( $tmp_c == 0) {
              	   $count = "<i><font color=\"#ff0000\">$count<\/font><\/i>";
                }

        }

	#
	# Write current message.
	#
################# cookeeeeeiii
print &setCookie("NAME", $FORM{'FROM'});
print &setCookie("SUBJECT", $FORM{'ODAI'});
print &setCookie("MAIL", $FORM{'MAIL'});
print &setCookie("URL", $FORM{'URL'});
################# cookeeeeeiii
############Cookeeee start
#
# Cookie�̒l�𓾂�
#
&getCookie();
$from = $COOKIE{'NAME'};
if ($FORM{'FROM'} eq "") {
    $from = "";
}
else{
    $from = $FORM{'FROM'};
}
$from =~ s/<img src=(.*)>(.*)<img src=(.*)>/$2/;
$from =~ s/(.*)<img src=(.*)>/$1/;

$subject = $COOKIE{'SUBJECT'};
if ($FORM{'ODAI'} eq "") {
    $subject = "";
}
else{
    $subject = $FORM{'ODAI'};
}
$mail = $COOKIE{'MAIL'};
if ($FORM{'MAIL'} eq "") {
    $mail = "";    
}
else {
    $mail = $FORM{'MAIL'};
}
$url = $COOKIE{'URL'};
if ($FORM{'URL'} eq "") {
    $url = "";
}
else {
    $url = $FORM{'URL'};
}
############Cookeeee end

	$FORM{'MESSAGE'} =~ s/\r*$//g;
	$FORM{'MESSAGE'} =~ s/\r/<BR>/g;
	open(OUT, "> wwwboard.tmp");
	print OUT "<TABLE BORDER=1><TR><TD BGCOLOR=\"#000000\">\n";
	print OUT "<FONT COLOR=\"#FFFFFF\">No.$count</FONT></TD>\n";
################################## Subject
	print OUT "<TD>\n";
#	print OUT "����:</TD>";
#	print OUT "<TD>\n";
	if ($FORM{'ODAI'} eq "") {
	    print OUT "<FONT size = 4 COLOR=\"#FF0000\">(����)</FONT></TD><TD BGCOLOR=\"#0faaff\"><i>$date</i></TD></TR>\n";
	}else{
	print OUT "<FONT size = 4 COLOR=\"#FF0000\"><b>$FORM{'ODAI'}</b></FONT></TD><TD BGCOLOR=\"#0faaff\"><i>$date</i></TD></TR>\n";
        }
#	print OUT "<TR><TD></TD>\n";
	print OUT "<TR>\n";
	print OUT "<TD ALIGN=\"center\">\n";
	if ($FORM{'MAIL'} eq "") {
	    print OUT  "�����O:</TD> <TD VALIGN = \"middle\" BGCOLOR=\"#ffaaaa\"><FONT size = 4 COLOR=\"#0000FF\"><b>$FORM{'FROM'}</b></FONT>����</TD> \n";
	} else {
	    print OUT "�����O:</TD> <TD VALIGN = \"middle\" BGCOLOR=\"#aaaaff\"><A HREF=\"mailto:$FORM{'MAIL'}\"><FONT size = 4 ><b>$FORM{'FROM'}</b></FONT></A>����</TD> \n";
#	    print OUT "�����O:</TD> <TD VALIGN = \"middle\" BGCOLOR=\"#aaaaff\"><H3><A HREF=\"mailto:$FORM{'MAIL'}\">$FORM{'FROM'}</A>����</H3></TD> <TD BGCOLOR=\"##ffaaaa\"> $date</TD></TR>\n";
	}
	if ($FORM{'URL'} ne "") {
	    print OUT "<TD BGCOLOR=\"#aaaaff\">URL:<A HREF=\"$FORM{'URL'}\">$FORM{'URL'}</A></TD></TR>\n";
	}
################################## Name
	print OUT "</TABLE>\n";
	print OUT "<TABLE ><TR><TD><b>\n";
	print OUT "$FORM{'MESSAGE'}\n";
#	print OUT "<br> \n";
	print(OUT "<!--- host:  $ENV{'REMOTE_ADDR'}  --->\n");
##### 99/12/15
print OUT "<P><INPUT TYPE=checkbox NAME=NUMBER VALUE=\"$count\">���̃J�L�R�Ƀ��X����H\n";
######
##### 99/12/14
#print OUT "<FORM METHOD=POST ACTION=\"h6aaboard.cgi?reply\">\n";
#print OUT "<FORM METHOD=POST ACTION=\"writeboard.cgi?reply\">\n";
#print OUT "<INPUT TYPE=hidden NAME=NUMBER VALUE=\"$count\">\n";
#print OUT "<P><INPUT TYPE=submit VALUE=\"�ԐM \[ Reply \]\">\n";
#print OUT "</FORM>\n";
######
	print OUT "</b></TD></TR></TABLE>\n";
	print OUT "<HR>\n";



	#
	# Append messages.
	#
	open(IN, "wwwboard.dat");
	while (<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);

	#
	# Copy .tmp to .dat
	#
#	open(IN, "wwwboard.tmp");
        @nkfv = `nkf -s wwwboard.tmp`; #for nkf
	open(OUT, "> wwwboard.dat");
	$msgs = 0;
#	while (<IN>) {
	while (@nkfv) {  # for nkf
	    $tmpline = shift @nkfv; # for nkf

#		if ($_ =~ /^<TABLE><TR><TD>/) {
#		if ($_ =~ /^<TABLE BORDER=1><TR><TD BGCOLOR=\"#000000\">/) {
		if ($tmpline =~ /^<TABLE BORDER=1><TR><TD BGCOLOR=\"#000000\">/) { #for nkf
			if ($max_msgs != 0) {
				if ($msgs++ >= $max_msgs) {
					last;
				}
			}
		}
#		print OUT;
		print OUT "$tmpline"; # for nkf
	}
#	close(IN);
	close(OUT);
}


#
# File unlock
#
if ($FORM{'MESSAGE'} ne "") {
rmdir("lock/wwwboard.loc");
}

#if ($ARGV[0] eq "reload") {
#	rmdir("lock/wwwboard.loc");
#	print "Location: $ENV{'SCRIPT_NAME'}\n";
#	print "\n";
#	exit(0);
#}


##### 99/12/14
if ($ARGV[0] eq "reply") {
    $target = 0;
    open(IN, "wwwboard.dat");
#    open(IN, "h6aaboard.dat");
    while (<IN>) {
	if ($FORM{'NUMBER'} ne "") {

#	    if ($_ =~ /^<FONT COLOR=\"#FFFFFF\">No\.$FORM{'NUMBER'}/) {
#	    if ($_ =~ /^<FONT COLOR=\"#FFFFFF\">\[h6aaboard $FORM{'NUMBER'}\]<\/FONT><\/TD>/){
######## 99/12/15
	    @tt_num = split(/,/, $FORM{'NUMBER'});
	    foreach $tt (@tt_num) {
#		print "|$tt|\n";
#	    if ($_ =~ /^<FONT COLOR=\"#FFFFFF\">No\.$FORM{'NUMBER'}/) {
#	    if ($_ =~ /^<FONT COLOR=\"#FFFFFF\">\[h6aaboard $FORM{'NUMBER'}\]<\/FONT><\/TD>/){
	        if ($_ =~ /^<FONT COLOR=\"#FFFFFF\">No\.$tt/) {
#		if ($_ =~ /^<FONT COLOR=\"#FFFFFF\">\[h6aaboard $tt\]<\/FONT><\/TD>/){
		    $target = 2;
		}		
	    }
##########
#		$target = 2;
#	    }		
#            if ($_ =~ /^<FORM METHOD=POST ACTION=\"writeboard\.cgi\?reply\">/) {
#            if ($_ =~ /^<FORM METHOD=POST ACTION=\"h6aaboard\.cgi\?reply\">/) {
######### 99/12/15
#            if ($_ =~ /^<FORM METHOD=POST ACTION=\"h6aaboard\.cgi\?reply\">/) {
            if ($_ =~ /^<P><INPUT TYPE=checkbox NAME=NUMBER VALUE=\"(.*)\">���̃J�L�R�Ƀ��X����H/) {
################
		$target = 0;
	    }
    	    if($target == 1){
		$tmp_mes = $_;
		$tmp_mes =~ s/\<BR\>//g;
#		$tmp_mes =~ s/\<font (.*)\"\>(.*)\<\/font\>/$2/g;
		while($tmp_mes =~ s/\<font color=\"#(\w*)\"\>(.*)/$2/g){
		      ;
		  }
		while($tmp_mes =~ s/\<\/font\>(.*)/$1/g){
		      ;
		  }
		while($tmp_mes =~ s/\<\/a\>(.*)/$1/g){
		      ;
		  }
		while($tmp_mes =~ s/\<a href=\"(.*)\"\>(.*)/$2/g){
		    ;
		}
		$message = "$message>$tmp_mes";
	    }
    	    if($target == 2){
		if($_ =~ /^<FONT size = 4 COLOR=\"#FF0000\"><b>(.*)<\/b><\/FONT><\/TD><TD BGCOLOR=\"##ffaaaa\"><i>(.*)<\/i><\/TD><\/TR>/){
		   $tmp_sub = $1;
		   $tmp_sub =~ s/Re: //g;
		   $subject = "Re: $tmp_sub";
		}
                if ($_ =~ /^<TABLE ><TR><TD><b>/) {
	         	$target = 1;
	        }
            } 
	}
    }
#print "</BODY>\n";
#print "</HTML>\n";
    close(IN);
#    rmdir("lock/h6aaboard.loc");
#    rmdir("lock/wwwboard.loc");
#    exit(0);

}
##### 


#
# Print HTML document
#
print "Content-type: text/html\n";
print "\n";
print "<HTML>\n";
print "<HEAD>\n";
print "<TITLE>�f����</TITLE>\n";
print "</HEAD>\n";
#print "<BODY TEXT=black BGCOLOR=white>\n";
print "<body BGCOLOR=\"#aaffaa\" TEXT=\"#000000\"  link=\"#f00700\" vlink=\"#505050\" alink=\"#00a822\">\n";
print "<H2>�f����</H2>\n";
if ($return_url ne "") {
	print "<A HREF=\"$return_url\"><font color = \"#ff0000\" size = 5><b>[�g�b�v�y�[�W�֖߂�]</b></font></A>\n";
}
if ($read_url ne "") {
	print "<A HREF=\"$read_url\"><font color = \"#ff0000\" size = 5><b> [�t���[���f����]</b></font></A>\n";
}
if ($jump_url ne "") {
	print "<A HREF=\"$jump_url\"><font color = \"#ff0000\" size = 5><b> [�I�t��̌f����]</b></font></A>\n";
}
print "<HR>\n";
print "<img src=\"http://www.yk.rim.or.jp/~michita/cgi-bin/wwwcount.cgi?gif\">\n";
#print "<FORM METHOD=POST ACTION=\"wwwboard.cgi?reload\">\n";
print "<FORM METHOD=POST ACTION=\"wwwboard.cgi\">\n";
print "<TABLE BORDER=3>\n";
print "<TR>";
print "<TD>�����O�F</TD>";
#print "<TD><INPUT TYPE=text NAME=FROM SIZE=54 VALUE=\"$FORM{'FROM'}\"></TD>\n";
print "<TD><INPUT TYPE=text NAME=FROM SIZE=54 VALUE=\"$from\"></TD>\n";
print "</TR>\n";
##################################  Subject
print "<TR>";
print "<TD>����F</TD>";
#print "<TD><INPUT TYPE=text NAME=ODAI SIZE=54 VALUE=\"$FORM{'ODAI'}\"></TD>";
print "<TD><INPUT TYPE=text NAME=ODAI SIZE=54 VALUE=\"$subject\"></TD>";
print "</TR>\n";
################################## Subject
print "<TR>";
print "<TD>MAIL�F</TD>";
#print "<TD><INPUT TYPE=text NAME=MAIL SIZE=54 VALUE=\"$FORM{'MAIL'}\"></TD>";
print "<TD><INPUT TYPE=text NAME=MAIL SIZE=54 VALUE=\"$mail\"></TD>";
print "</TR>\n";
print "<TR>";
print "<TD>�t�q�k�F</TD>";
#print "<TD><INPUT TYPE=text NAME=URL SIZE=54 VALUE=\"$FORM{'URL'}\"></TD>";
print "<TD><INPUT TYPE=text NAME=URL SIZE=54 VALUE=\"$url\"></TD>";
print "</TR>\n";
print "<TR>";
print "<TD COLSPAN=2><SMALL>MAIL�ɂ́A���[���A�h���X�����Ă��������B�ȗ��B</SMALL></TD>\n";
print "</TR>\n";
print "<TR>";
print "<TD COLSPAN=2><SMALL>URL�ɂ́Ahttp:�Ŏn�܂�z�[���y�[�W�A�h���X�����Ă��������B�ȗ��B</SMALL></TD>\n";
print "</TR>\n";
print "<TR><TD COLSPAN=2>";
#print "<TEXTAREA ROWS=7 COLS=60 NAME=MESSAGE></TEXTAREA></TD></TR>\n";
print "<TEXTAREA ROWS=7 COLS=60 NAME=MESSAGE>$message</TEXTAREA></TD></TR>\n";
print "</TABLE>\n";
print "<P><INPUT TYPE=submit VALUE=\"�������� / �ēǂݍ��� \[ Submit/Reload \]\">\n";
print "</FORM>\n";
#################### 99/12/15
#print "<FORM METHOD=POST ACTION=\"h6aaboard.cgi?reply\">\n";
print "<FORM METHOD=POST ACTION=\"writeboard.cgi?reply\">\n";
print "<P><INPUT TYPE=submit VALUE=\"�`�F�b�N�����J�L�R�ɕԐM \[ Reply \]\"><br>\n";
#print "<P><INPUT TYPE=submit VALUE=\"�`�F�b�N�����J�L�R�ɕԐM \[ Reply \]\">\n";
###################
#print "<td valign=\"middle\"></td><td valign=\"middle\"><strong><small><H4><b>�}�[�N��7��14�������`17���ߑO���܂ŏo�܂���.</b> </H4></small></strong></td>    <td valign=\"middle\"></td>\n";
print "<HR>\n";
open(IN, "wwwboard.dat");
while (<IN>) {
	print;
}
close(IN);
#################### 99/12/15
print "</FORM>\n";
###################
print "</BODY>\n";
print "</HTML>\n";

############Cockeeeiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
# Cookie�̒l��ǂݏo��
#
sub getCookie {
    local($xx, $name, $value);
    for $xx (split(/; */, $ENV{'HTTP_COOKIE'})) {
        ($name, $value) = split(/=/, $xx);
        $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
        $COOKIE{$name} = $value;
    }
}

#
# Cookie�ɒl���������ނ��߂�Set-Cookie:�w�b�_�𐶐�����
#
sub setCookie {
    local($tmp, $val);
    $val = $_[1];
    $val =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
    $tmp = "Set-Cookie: ";
    $tmp .= "$_[0]=$val; ";
    $tmp .= "expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
    return($tmp);
}

#
# Cookie���폜���邽�߂�Set-Cookie:�w�b�_�𐶐�����
#
sub clearCookie {
    $tmp = "Set-Cookie: ";
    $tmp .= "$_[0]=xx; ";
    $tmp .= " expires=Thu, 1-Jan-1980 00:00:00 GMT;\n";
    return($tmp);
}



#
# File unlock
#
##if ($FORM{'MESSAGE'} ne "") {
##rmdir("lock/wwwboard.loc");
##}
