#!/usr/local/bin/ruby
print "Content-type: text/html; charset=EUC-jp\n\n"

print "<html><body>"
print "<form action=\"disp.cgi\" method=\"POST\">"
print "Anzai-Imai Lab. paper upload service(alpha version) constructed by Masahiko Taguchi<br><br>"
print "��ʸ��������Ϥ��Ƥ�������������Ū�����Ƥι��ܤ�����ɬ�ܤǤ���<br>"
print "Please input your paper/journal information. Basically, all items are essential factor.<br><br>"
print "<table>"

print "<tr><td>Paper Type</td><td><input type=\"radio\" name=\"type\" value=\"jconf\" id=\"jconf\"><label for=\"jconf\">����ز� </label><input type=\"radio\" name=\"type\" value=\"iconf\" id=\"iconf\"><label for=\"iconf\">Int'l Conf. </label><input type=\"radio\" name=\"type\" value=\"jj\" id=\"jj\"><label for=\"jj\">��ʸ��(��ʸ) </label><input type=\"radio\" name=\"type\" value=\"ej\" id=\"ej\"><label for=\"ej\">Journal(English) </label></td><td>* Select your paper type</td></tr>"

print "<tr><td>�����ȥ�(��ʸ)</td><td><input type=\"text\" name=\"jtitle\" style=\"width:500px\"></td><td>(ex)�ɥ館�����߷�</td></tr>"
print "<tr><td>Title(English)</td><td><input type=\"text\" name=\"etitle\" style=\"width:500px\"></td><td>(ex)The Design of DORAEMON</td></tr>"
print "<tr><td>����(��ʸ)</td><td><input type=\"text\" name=\"jauthor\" style=\"width:500px\"></td><td>(ex)ƣ�� ����ͺ��ƣ�� �ץ�</td></tr>"
print "<tr><td>Author(English)</td><td><input type=\"text\" name=\"eauthor\" style=\"width:500px\"></td><td>(ex)Fujio Fujiko, Pro Fujiko</td></tr>"

print "<tr><td>���ͽ�ƽ�̾(��ʸ)</td><td><input type=\"text\" name=\"jbook\" style=\"width:300px\"></td><td>(ex)�ɥ館���βʳ�</td></tr>"
print "<tr><td>J./proc. Name(English)</td><td><input type=\"text\" name=\"ebook\" style=\"width:300px\"></td><td>(ex)The Journal of DORAEMON Science</td></tr>"

print "<tr><td>Volume</td><td><input type=\"text\" name=\"vol\" style=\"width:100px\"></td><td>* when no Volume, input`na'</td></tr>"
print "<tr><td>Number</td><td><input type=\"text\" name=\"no\" style=\"width:100px\"></td><td>* when no Number, input`na'</td></tr>"
print "<tr><td>Page</td><td>From <input type=\"text\" name=\"ppf\" style=\"width:100px\"> To <input type=\"text\" name=\"ppt\" style=\"width:100px\"></td><td>(ex)From 7 To 12</td></tr>"

print "<tr><td>ȯɽ���(��ʸ)</td><td>���Ż��� <input type=\"text\" name=\"jbldg\" style=\"width:100px\"> ������ <input type=\"text\" name=\"jplace\" style=\"width:100px\"> ���Ź� <input type=\"text\" name=\"jcountry\" style=\"width:100px\"></td><td>(ex)���������ء����͡�����</td></tr>"
print "<tr><td>Venue(English)</td><td>Building <input type=\"text\" name=\"ebldg\" style=\"width:100px\"> Place <input type=\"text\" name=\"eplace\" style=\"width:100px\"> Country <input type=\"text\" name=\"ecountry\" style=\"width:100px\"></td><td>(ex)Keio Univ., Yokohama, Japan</td></tr>"

print "<tr><td>Presentation Date</td><td>Year <input type=\"text\" name=\"year\" style=\"width:100px\"> Month <input type=\"text\" name=\"month\" style=\"width:100px\"> Day <input type=\"text\" name=\"day\" style=\"width:100px\"></td><td>(ex)2007(Year)/9(Month)/15(Day)</td></tr>"

print "<tr><td>Conf. Period</td><td>From <input type=\"text\" name=\"fperiod\" style=\"width:200px\"> To <input type=\"text\" name=\"tperiod\" style=\"width:200px\"></td><td>(ex)From 2007/9/13 To 2007/9/15</td></tr>"

print "<tr><td>PDF File Path</td><td><input type=\"file\" name=\"filepath\" size=60></td><td>* use reference button</td></tr>"

# print "<tr><td>...</td><td><input type=\"text\" name=\"...\" style=\"width:100px\"></td><td>(ex)...</td></tr>"


print "<tr><td></td><td><input type=\"submit\" value=\"submit\"></td></tr>"
print "</table></form>"
pritn "</body><html>"
