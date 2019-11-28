	# Port Scanner - Jose Rosendo

import socket
import sys
import os
import subprocess

# Check if IP syntax is correct
def correctIP(ip):
    try:
        for octet in list(map(int, sys.argv[1].split("."))):
            if octet in range(0, 256) and len(sys.argv[1].split(".")) == 4:
                isCorrect = True
            else:
                isCorrect = False
                print("Error. IP {} is not correct.".format(sys.argv[1], end=""))
                exit()

        if isCorrect:
            print("IP {} is correct.".format(sys.argv[1], end=""))

    except ValueError:
        print("Error. IP {} is not correct.".format(sys.argv[1], end=""))
        exit()

# Check if host exists in the network
def ipExists(ip):
    if os.name == 'nt': # Windows
        if str("mil") in str(subprocess.Popen(["ping", ip, "-n", "1"],stdout=subprocess.PIPE).stdout.read()): # If ping response contains string "mil", short for milli-seconds or milisegundos
            print("IP {} is up.".format(ip))
        else:
            print("IP {} is down.".format(ip))
    else: # Any OS but Windows (Unix)
        if  os.system("ping -q -c 1 " + ip + " > /dev/null 2>&1") == 0:
            print("IP {} is up.".format(ip))
        else:
            print("IP {} is down.".format(ip))

# Check if host has a specific opened port
### def isOpen(ip, port):
###     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
###     sock.settimeout(1)
###     result = sock.connect_ex((sys.argv[1], port))
###     if result == 0:
###         print("Port {} is open for host {}.".format(port, ip))
###     else:
###         print("Port {} is not open for host {}.".format(port, ip))

# Check open ports from a host
### def openPorts(ip):
###     existe = False
###     for port in range(1, 1025):
###         print(port)
###         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
###         sock.settimeout(1)
###         result = sock.connect_ex((sys.argv[1], port))
###         if result == 0:
###             existe = True
###             break
###         else:
###             existe = False
### 
###     if existe:
###         print("Port {} is open for IP {}.".format(port, sys.argv[1]))
###     else:
###         print("IP {} has no opened ports.".format(sys.argv[1]))


if len(sys.argv) > 1:
    correctIP(sys.argv[1])
    ipExists(sys.argv[1])
    #isOpen(sys.argv[1], 80)
    #openPorts(sys.argv[1])
else:
    print('Error. Module sintax structure: "file_name.py target_IP".')
    print("Please, insert a valid IP into the command line.")