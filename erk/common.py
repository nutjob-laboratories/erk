
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
		<table style="width: 100%" border="0">
      <tbody>
        <tr>
          <td style="text-align: center; vertical-align: middle;">&nbsp;<img src="{LOGO_IMAGE}">&nbsp;&nbsp;</td>
          <td>
            <table style="width: 100%" border="0">
              <tbody>
              <tr>
              <td style="text-align: left; vertical-align: middle;">&nbsp;
              </td>
              </tr>
                <tr>
                  <td style="text-align: left; vertical-align: middle;"><big><b>Version {APPLICATION_VERSION}</b></big></td>
                </tr>
                <tr>
                  <td style="text-align: left; vertical-align: middle;"><i>It's how you say IRC</i></td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>'''

