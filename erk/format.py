
from datetime import datetime
from itertools import combinations

import html

from erk.config import *
from erk.resources import *

CHAT_MESSAGE = "0"
SELF_MESSAGE = "1"
ACTION_MESSAGE = "2"
NOTICE_MESSAGE = "3"
ERROR_MESSAGE = "4"
SYSTEM_MESSAGE = "5"
MOTD_MESSAGE = "6"
HR_MESSAGE = "7"

HORIZONTAL_RULE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

UNSEEN_MESSAGES_MARKER = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;"><small>&nbsp;</small>
			</td>
			<td><center><small>NEW</small></center></td>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;"><small>&nbsp;</small>
			</td>
		</tr>
	</tbody>
</table>'''

TIMESTAMP_TEMPLATE = """<td style="vertical-align:top; font-size:small; text-align:left;"><div style="!TIMESTAMP_STYLE!">[!TIME!]</div></td><td style="font-size:small;">&nbsp;</td>"""

MESSAGE_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><div style="!ID_STYLE!">!ID!</div></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

MESSAGE_TEMPLATE_USERLINK = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><a style="color:inherit; text-decoration: none;" href="!ID!"><div style="!ID_STYLE!">!ID!</div></a></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

SYSTEM_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

MESSAGE_STYLE_TEMPLATE = """<td style="text-align: left; vertical-align: top;"><div style="!MESSAGE_STYLE!">!MESSAGE!</div></td>"""
MESSAGE_NO_STYLE_TEMPLATE = """<td style="text-align: left; vertical-align: top;">!MESSAGE!</td>"""

IRC_00 = "#FFFFFF"
IRC_01 = "#000000"
IRC_02 = "#0000FF"
IRC_03 = "#008000"
IRC_04 = "#FF0000"
IRC_05 = "#A52A2A"
IRC_06 = "#800080"
IRC_07 = "#FFA500"
IRC_08 = "#FFFF00"
IRC_09 = "#90EE90"
IRC_10 = "#008080"
IRC_11 = "#00FFFF"
IRC_12 = "#ADD8E6"
IRC_13 = "#FFC0CB"
IRC_14 = "#808080"
IRC_15 = "#D3D3D3"

def render_message(styles,mtype,user,message,timestamp=None,max_nick_size=20,no_html=True,irc_color=True,links=True,show_timestamp=True,timestamp_seconds=False,timestamp_24=True,filter_profanity=False,click_usernames=True):

	# message = html.escape(message)

	if no_html: message = remove_html_markup(message)
	if links: message = inject_www_links(message,styles[HYPERLINK_STYLE_NAME])
	if irc_color:
		if string_has_irc_formatting_codes(message):
			message = convert_irc_color_to_html(message)
	else:
		message = strip_color(message)

	if filter_profanity: message = filterProfanityFromText(message)

	# This is for whois messages
	message = message.replace("\n","<br>")

	#message = fr"{message}"

	if mtype==SYSTEM_MESSAGE:

		output = SYSTEM_TEMPLATE
		mstyle = styles[SYSTEM_STYLE_NAME]

	elif mtype==ERROR_MESSAGE:

		output = SYSTEM_TEMPLATE
		mstyle = styles[ERROR_STYLE_NAME]

	elif mtype==ACTION_MESSAGE:

		output = SYSTEM_TEMPLATE
		mstyle = styles[ACTION_STYLE_NAME]

	elif mtype==MOTD_MESSAGE:

		message = message.replace("\n","<br>")

		output = SYSTEM_TEMPLATE
		mstyle = styles[MOTD_STYLE_NAME]

	elif mtype==HR_MESSAGE:

		output = HORIZONTAL_RULE
		mstyle = styles[MESSAGE_STYLE_NAME]

	else:

		if click_usernames:
			if mtype==SELF_MESSAGE:
				output = MESSAGE_TEMPLATE
			else:
				output = MESSAGE_TEMPLATE_USERLINK

		else:

			output = MESSAGE_TEMPLATE
		mstyle = styles[MESSAGE_STYLE_NAME]

	if mstyle=="":
		output = output.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_NO_STYLE_TEMPLATE)
	else:
		output = output.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_STYLE_TEMPLATE)
		output = output.replace("!MESSAGE_STYLE!",mstyle)

	if show_timestamp:
		if timestamp==None:
			t = datetime.timestamp(datetime.now())
		else:
			t = timestamp

		if timestamp_24:
			tfs = '%H:%M'
		else:
			tfs = '%I:%M'

		if timestamp_seconds:
			tfs = tfs + ':%S'

		pretty_timestamp = datetime.fromtimestamp(t).strftime(tfs)

		ts = TIMESTAMP_TEMPLATE.replace("!TIMESTAMP_STYLE!",styles[TIMESTAMP_STYLE_NAME])
		ts = ts.replace("!TIME!",pretty_timestamp)
		output = output.replace("!TIMESTAMP!",ts)
	else:
		output = output.replace("!TIMESTAMP!",'')

	idl = max_nick_size - len(user)
	if idl>0:
		ident = ('&nbsp;'*idl)+user
	else:
		ident = user

	if mtype==SELF_MESSAGE:
		user_style = styles[SELF_STYLE_NAME]
	elif mtype==CHAT_MESSAGE:
		user_style = styles[USERNAME_STYLE_NAME]
	elif mtype==NOTICE_MESSAGE:
		user_style = styles[NOTICE_STYLE_NAME]
	else:
		user_style = ''

	output = output.replace("!ID_STYLE!",user_style)
	output = output.replace("!ID!",ident)

	output = output.replace("!MESSAGE!",message)
	return output

def remove_html_markup(s):
	tag = False
	quote = False
	out = ""

	for c in s:
			if c == '<' and not quote:
				tag = True
			elif c == '>' and not quote:
				tag = False
			elif (c == '"' or c == "'") and tag:
				quote = not quote
			elif not tag:
				out = out + c

	return out

def inject_www_links(txt,style):
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', txt)
	for u in urls:
		u = re.sub('<[^<]+?>', '', u)
		link = f"<a href=\"{u}\"><span style=\"{style}\">{u}</span></a>"
		txt = txt.replace(u,link)
	return txt

def string_has_irc_formatting_codes(data):
	for code in ["\x03","\x02","\x1D","\x1F","\x0F"]:
		if code in data: return True
	return False

def convert_irc_color_to_html(text):

	html_tag = "font"

	# other format tags
	fout = ''
	inbold = False
	initalic = False
	inunderline = False
	incolor = False
	for l in text:
		if l=="\x02":
			inbold = True
			fout = fout + "<b>"
			continue
		if l=="\x1D":
			initalic = True
			fout = fout + "<i>"
			continue
		if l=="\x1F":
			inunderline = True
			fout = fout + "<u>"
			continue
		if l=="\x03":
			incolor = True
			fout = fout + l
			continue

		if l=="\x0F":
			if incolor:
				incolor = False
				fout = fout + f"</{html_tag}>"
				continue
			if inbold:
				fout = fout + "</b>"
				inbold = False
				continue
			if initalic:
				fout = fout + "</i>"
				initalic = False
				continue
			if inunderline:
				fout = fout + "</u>"
				inunderline = False
				continue

		fout = fout + l

	if inbold: fout = fout + "</b>"
	if initalic: fout = fout + "</i>"
	if inunderline: fout = fout + "</u>"

	text = fout

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		if int(fore)==0: foreground = str(IRC_00)
		if int(fore)==1: foreground = str(IRC_01)
		if int(fore)==2: foreground = str(IRC_02)
		if int(fore)==3: foreground = str(IRC_03)
		if int(fore)==4: foreground = str(IRC_04)
		if int(fore)==5: foreground = str(IRC_05)
		if int(fore)==6: foreground = str(IRC_06)
		if int(fore)==7: foreground = str(IRC_07)
		if int(fore)==8: foreground = str(IRC_08)
		if int(fore)==9: foreground = str(IRC_09)
		if int(fore)==10: foreground = str(IRC_10)
		if int(fore)==11: foreground = str(IRC_11)
		if int(fore)==12: foreground = str(IRC_12)
		if int(fore)==13: foreground = str(IRC_13)
		if int(fore)==14: foreground = str(IRC_14)
		if int(fore)==15: foreground = str(IRC_15)

		if int(back)==0: background = str(IRC_00)
		if int(back)==1: background = str(IRC_01)
		if int(back)==2: background = str(IRC_02)
		if int(back)==3: background = str(IRC_03)
		if int(back)==4: background = str(IRC_04)
		if int(back)==5: background = str(IRC_05)
		if int(back)==6: background = str(IRC_06)
		if int(back)==7: background = str(IRC_07)
		if int(back)==8: background = str(IRC_08)
		if int(back)==9: background = str(IRC_09)
		if int(back)==10: background = str(IRC_10)
		if int(back)==11: background = str(IRC_11)
		if int(back)==12: background = str(IRC_12)
		if int(back)==13: background = str(IRC_13)
		if int(back)==14: background = str(IRC_14)
		if int(back)==15: background = str(IRC_15)

		t = f"\x03{fore},{back}"
		r = f"<{html_tag} style=\"color: {foreground}; background-color: {background}\">"
		text = text.replace(t,r)

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		if int(fore)==0: foreground = str(IRC_00)
		if int(fore)==1: foreground = str(IRC_01)
		if int(fore)==2: foreground = str(IRC_02)
		if int(fore)==3: foreground = str(IRC_03)
		if int(fore)==4: foreground = str(IRC_04)
		if int(fore)==5: foreground = str(IRC_05)
		if int(fore)==6: foreground = str(IRC_06)
		if int(fore)==7: foreground = str(IRC_07)
		if int(fore)==8: foreground = str(IRC_08)
		if int(fore)==9: foreground = str(IRC_09)
		if int(fore)==10: foreground = str(IRC_10)
		if int(fore)==11: foreground = str(IRC_11)
		if int(fore)==12: foreground = str(IRC_12)
		if int(fore)==13: foreground = str(IRC_13)
		if int(fore)==14: foreground = str(IRC_14)
		if int(fore)==15: foreground = str(IRC_15)

		if int(back)==0: background = str(IRC_00)
		if int(back)==1: background = str(IRC_01)
		if int(back)==2: background = str(IRC_02)
		if int(back)==3: background = str(IRC_03)
		if int(back)==4: background = str(IRC_04)
		if int(back)==5: background = str(IRC_05)
		if int(back)==6: background = str(IRC_06)
		if int(back)==7: background = str(IRC_07)
		if int(back)==8: background = str(IRC_08)
		if int(back)==9: background = str(IRC_09)
		if int(back)==10: background = str(IRC_10)
		if int(back)==11: background = str(IRC_11)
		if int(back)==12: background = str(IRC_12)
		if int(back)==13: background = str(IRC_13)
		if int(back)==14: background = str(IRC_14)
		if int(back)==15: background = str(IRC_15)

		t = f"\x03{fore},{back}"
		r = f"<{html_tag} style=\"color: {foreground}; background-color: {background}\">"
		text = text.replace(t,r)

	text = text.replace("\x0310",f"<{html_tag} style=\"color: {IRC_10};\">")
	text = text.replace("\x0311",f"<{html_tag} style=\"color: {IRC_11};\">")
	text = text.replace("\x0312",f"<{html_tag} style=\"color: {IRC_12};\">")
	text = text.replace("\x0313",f"<{html_tag} style=\"color: {IRC_13};\">")
	text = text.replace("\x0314",f"<{html_tag} style=\"color: {IRC_14};\">")
	text = text.replace("\x0315",f"<{html_tag} style=\"color: {IRC_15};\">")

	text = text.replace("\x0300",f"<{html_tag} style=\"color: {IRC_00};\">")
	text = text.replace("\x0301",f"<{html_tag} style=\"color: {IRC_01};\">")
	text = text.replace("\x0302",f"<{html_tag} style=\"color: {IRC_02};\">")
	text = text.replace("\x0303",f"<{html_tag} style=\"color: {IRC_03};\">")
	text = text.replace("\x0304",f"<{html_tag} style=\"color: {IRC_04};\">")
	text = text.replace("\x0305",f"<{html_tag} style=\"color: {IRC_05};\">")
	text = text.replace("\x0306",f"<{html_tag} style=\"color: {IRC_06};\">")
	text = text.replace("\x0307",f"<{html_tag} style=\"color: {IRC_07};\">")
	text = text.replace("\x0308",f"<{html_tag} style=\"color: {IRC_08};\">")
	text = text.replace("\x0309",f"<{html_tag} style=\"color: {IRC_09};\">")

	text = text.replace("\x030",f"<{html_tag} style=\"color: {IRC_00};\">")
	text = text.replace("\x031",f"<{html_tag} style=\"color: {IRC_01};\">")
	text = text.replace("\x032",f"<{html_tag} style=\"color: {IRC_02};\">")
	text = text.replace("\x033",f"<{html_tag} style=\"color: {IRC_03};\">")
	text = text.replace("\x034",f"<{html_tag} style=\"color: {IRC_04};\">")
	text = text.replace("\x035",f"<{html_tag} style=\"color: {IRC_05};\">")
	text = text.replace("\x036",f"<{html_tag} style=\"color: {IRC_06};\">")
	text = text.replace("\x037",f"<{html_tag} style=\"color: {IRC_07};\">")
	text = text.replace("\x038",f"<{html_tag} style=\"color: {IRC_08};\">")
	text = text.replace("\x039",f"<{html_tag} style=\"color: {IRC_09};\">")

	text = text.replace("\x03",f"</{html_tag}>")

	# close font tags
	if f"<{html_tag} style=" in text:
		if not f"</{html_tag}>" in text: text = text + f"</{html_tag}>"

	out = []
	indiv = False
	for w in text.split(' '):

		if indiv:
			if w==f"<{html_tag}":
				out.append(f"</{html_tag}>")

		if w==f"<{html_tag}": indiv = True
		if w==f"</{html_tag}>": indiv = False

		out.append(w)

	text = ' '.join(out)

	return text

def strip_color(text):

	html_tag = "font"

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	text = text.replace("\x0310","")
	text = text.replace("\x0311","")
	text = text.replace("\x0312","")
	text = text.replace("\x0313","")
	text = text.replace("\x0314","")
	text = text.replace("\x0315","")

	text = text.replace("\x0300","")
	text = text.replace("\x0301","")
	text = text.replace("\x0302","")
	text = text.replace("\x0303","")
	text = text.replace("\x0304","")
	text = text.replace("\x0305","")
	text = text.replace("\x0306","")
	text = text.replace("\x0307","")
	text = text.replace("\x0308","")
	text = text.replace("\x0309","")

	text = text.replace("\x030","")
	text = text.replace("\x031","")
	text = text.replace("\x032","")
	text = text.replace("\x033","")
	text = text.replace("\x034","")
	text = text.replace("\x035","")
	text = text.replace("\x036","")
	text = text.replace("\x037","")
	text = text.replace("\x038","")
	text = text.replace("\x039","")

	text = text.replace("\x03","")

	text = text.replace("\x02","")
	text = text.replace("\x1D","")
	text = text.replace("\x1F","")
	text = text.replace("\x0F","")

	return text
