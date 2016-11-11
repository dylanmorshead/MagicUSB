import sys, os
import win32com.client
from time import sleep
import unicodedata
import sys, traceback, os

__author__ = "Dylan Morshead"
__copyright__ = "Copyright (C) 2016 Dylan Morshead"
__license__ = "GNU Pubilc Licence V3.0"
__version__ = "1.0"


# MagicUSB inspired by UsbKILL, nothing like this exists for windows, so I coded my own.
# Nice Tool I must add, pretty much shut down when a new device is added, mimmics UsbKILL
# Sadly not all USB devices work, I don't think, most do, but things like an XBOX controller won't, I assume you have to loop through a difference WMI object.

#(C) Dylan Morshead 2016

# this function pretty much mimmics lsusb to a point, PID, VID.
# could be written better, but I'm a bit rusty with python.

# Unlike usbKILL this script is quite limited, feel free to add more shit to it.

# Anti-Forensic Tool, well trys to be, isn't perfect <3

#  /\/\   __ _  __ _(_) ___   /\ /\/ _\  / __\
# /    \ / _` |/ _` | |/ __| / / \ \ \  /__\//
#/ /\/\ \ (_| | (_| | | (__  \ \_/ /\ \/ \/  \
#\/    \/\__,_|\__, |_|\___|  \___/\__/\_____/
#              |___/                                                                                                     

def usb():
    wmi = win32com.client.GetObject ("winmgmts:")
    devices = []
    for usb in wmi.InstancesOf ("Win32_USBHub"):
        device = usb.DeviceID
        decoded = device.decode()
        VID = decoded.strip("USB\VID_")[:4]
        PID = decoded.split("&")[1].strip("PID_")[:4]
        if VID.find("ROOT"):
            devices.append(VID + ":" + PID)
    return devices


# shuts down the pc if we find an odd usb device.

def shutdown ():
    os.system('shutdown -t 0 -s -f')


def list_devices():
    for device in usb():
        print(device)


# mimics the loop function in usbKILL


def splash():
    print("  /\/\   __ _  __ _(_) ___   /\ /\/ _\  / __\\")
    print(" /    \ / _` |/ _` | |/ __| / / \ \ \  /__\//")
    print("/ /\/\ \ (_| | (_| | | (__  \ \_/ /\ \/ \/  \\")
    print("\/    \/\__,_|\__, |_|\___|  \___/\__/\_____/")
    print("             |___/                           ")
    print("(C) Dylan Morshead 2016 - dylan@morshead.org ")
    print("       Whited Listed Devices (Default)       ")
    list_devices()


def loop():

    splash()
    # obviously the main loop
    # by default we whitelist all the devices, currently connected.

    start_devices = usb()
    acceptable_devices = usb()

    while True:

        # get a list of the current devices
        current_devices = usb()

        for device in current_devices:
            if device not in acceptable_devices:
                # kill the computer
                shutdown()
        for device in start_devices:
            if device not in current_devices:
                shutdown()
        sleep(0.25) # sleeps for 0.25 seconds

loop()
