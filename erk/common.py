
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