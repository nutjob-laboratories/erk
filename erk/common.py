
import os
import sys

from erk.resources import *
from erk.strings import*

def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)

def convertSeconds(seconds):
	h = seconds//(60*60)
	m = (seconds-h*60*60)//60
	s = seconds-(h*60*60)-(m*60)
	return [h, m, s]

def prettyUptime(uptime):
	t = convertSeconds(uptime)
	hours = t[0]
	if len(str(hours))==1: hours = f"0{hours}"
	minutes = t[1]
	if len(str(minutes))==1: minutes = f"0{minutes}"
	seconds = t[2]
	if len(str(seconds))==1: seconds = f"0{seconds}"
	return f"{hours}:{minutes}:{seconds}"

START_BANNER = f'''
<center><table style="height: 100%" border="0">
      <tbody>
        <tr>
          <td>TOP&nbsp;</td>
        </tr>
        <tr>
          <td style="text-align: center; vertical-align: middle;">&nbsp;<center><img src="{LOGO_IMAGE}"></center></td>
        </tr>
        <tr>
          <td>BOTTOM&nbsp;</td>
        </tr>
      </tbody>
    </table></center>
'''

def get_network_url(net):
	
	if net.lower() =="2600net":
		return "https://www.scuttled.net/"

	if net.lower() =="accessirc":
		return "https://netsplit.de/networks/AccessIRC/"

	if net.lower() =="afternet":
		return "https://www.afternet.org/"

	if net.lower() =="aitvaras":
		return "http://www.aitvaras.eu/"

	if net.lower() =="anthrochat":
		return "https://www.anthrochat.net/"

	if net.lower() =="arcnet":
		return "http://arcnet-irc.org/"

	if net.lower() =="austnet":
		return "https://www.austnet.org/"

	if net.lower() =="azzurranet":
		return "https://netsplit.de/networks/Azzurra/"

	if net.lower() =="betachat":
		return "https://betachat.net/"

	if net.lower() =="buddyim":
		return "https://irc-source.com/net/BuddyIM"

	if net.lower() =="canternet":
		return "https://canternet.org/"

	if net.lower() =="chat4all":
		return "https://chat4all.net/"

	if net.lower() =="chatjunkies":
		return "https://netsplit.de/networks/ChatJunkies/"

	if net.lower() =="chatnet":
		return "http://www.chatnet.org/"

	if net.lower() =="chatspike":
		return "https://www.chatspike.net/"

	if net.lower() =="dalnet":
		return "https://www.dal.net/"

	if net.lower() =="darkmyst":
		return "https://www.darkmyst.org/"

	if net.lower() =="dark-tou-net":
		return "https://irc-source.com/net/Dark-Tou-Net"

	if net.lower() =="deltaanime":
		return "http://www.thefullwiki.org/DeltaAnime"

	if net.lower() =="efnet":
		return "http://www.efnet.org/"

	if net.lower() =="electrocode":
		return "https://netsplit.de/networks/ElectroCode/"

	if net.lower() =="enterthegame":
		return "http://www.enterthegame.com/"

	if net.lower() =="entropynet":
		return "https://entropynet.net/"

	if net.lower() =="espernet":
		return "https://esper.net/"

	if net.lower() =="euirc":
		return "https://www.euirc.net/"

	if net.lower() =="europnet":
		return "https://chat.europnet.org/"

	if net.lower() =="fdfnet":
		return "https://netsplit.de/networks/FDFnet/"

	if net.lower() =="freenode":
		return "https://freenode.net/"

	if net.lower() =="furnet":
		return "https://en.wikifur.com/wiki/FurNet_(IRC)"

	if net.lower() =="galaxynet":
		return "http://www.galaxynet.com/default.php?id=148"

	if net.lower() =="gamesurge":
		return "https://gamesurge.net/"

	if net.lower() =="geeksirc":
		return "https://twitter.com/geeksirc?lang=en"

	if net.lower() =="geekshed":
		return "http://www.geekshed.net/"

	if net.lower() =="gimpnet":
		return "https://www.gimp.org/irc.html"

	if net.lower() =="globalgamers":
		return "https://netsplit.de/networks/GlobalGamers/"

	if net.lower() =="hashmark":
		return "https://www.hashmark.net/"

	if net.lower() =="idlemonkeys":
		return "https://www.net-force.nl/"

	if net.lower() =="indirectirc":
		return "https://netsplit.de/networks/IndirectIRC/"

	if net.lower() =="interlinked":
		return "https://twitter.com/interlinkedirc"

	if net.lower() =="irc4fun":
		return "https://irc4fun.net/index.php?page=start"

	if net.lower() =="irchighway":
		return "https://irchighway.net/"

	if net.lower() =="ircnet":
		return "http://www.ircnet.org/"

	if net.lower() =="irctoo.net":
		return "https://netsplit.de/networks/IRCtoo/"

	if net.lower() =="kbfail":
		return "http://www.kbfail.net/"

	if net.lower() =="krstarica":
		return "https://pricaonica.krstarica.com/"

	if net.lower() =="librairc":
		return "http://www.librairc.net/"

	if net.lower() =="mindforge":
		return "https://mindforge.org/en/"

	if net.lower() =="mixxnet":
		return "https://www.mixxnet.net/"

	if net.lower() =="moznet":
		return "https://wiki.mozilla.org/IRC"

	if net.lower() =="obsidianirc":
		return "https://twitter.com/obsidianirc"

	if net.lower() =="oceanius":
		return "https://netsplit.de/networks/Oceanius/"

	if net.lower() =="oftc":
		return "https://www.oftc.net/"

	if net.lower() =="pirc.pl":
		return "https://pirc.pl/"

	if net.lower() =="ponychat":
		return "https://github.com/PonyChat"

	if net.lower() =="ptnet.org":
		return "https://www.ptnet.org/"

	if net.lower() =="quakenet":
		return "https://www.quakenet.org/"

	if net.lower() =="rizon":
		return "https://www.rizon.net/"

	if net.lower() =="serenity-irc":
		return "http://www.serenity-irc.net/"

	if net.lower() =="slashnet":
		return "http://slashnet.org/"

	if net.lower() =="snoonet":
		return "https://snoonet.org/irc-servers/"

	if net.lower() =="solidirc":
		return "http://search.mibbit.com/networks/solidirc"

	if net.lower() =="sorcerynet":
		return "https://www.sorcery.net/"

	if net.lower() =="spotchat":
		return "http://www.spotchat.org/"

	if net.lower() =="station51":
		return "https://netsplit.de/networks/Station51.net/"

	if net.lower() =="stormbit":
		return "https://stormbit.net/"

	if net.lower() =="swiftirc":
		return "https://swiftirc.net/"

	if net.lower() =="synirc":
		return "https://www.synirc.net/"

	if net.lower() =="techtronix":
		return "https://search.mibbit.com/channels/Techtronix"

	if net.lower() =="turlinet":
		return "https://www.servx.org/"

	if net.lower() =="undernet":
		return "http://www.undernet.org/"

	if net.lower() =="worldnet":
		return "https://netsplit.de/networks/Worldnet/"

	if net.lower() =="xertion":
		return "http://www.xertion.org/"

	return None