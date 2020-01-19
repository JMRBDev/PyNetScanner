	# Port Scanner - Jose Rosendo

import sys
import os
import subprocess
import signal
import socket
import urllib3
import smtplib

interruption = 0

def keyboardInterruptHandler(signal_received, frame):
    global interruption
    interruption = signal_received

    exit()

def setIpRange(ipRange):
    global firstIpOfRange
    global secondIpOfRange

    firstIpOfRange = list(map(int, ipRange.split("-")[0].split(".")))
    secondIpOfRange = list(map(int, ipRange.split("-")[1].split(".")))

def checkRange(numPing):
    if os.name == "nt": # Windows
        if str("mil") in str(subprocess.Popen(["ping", '.'.join([str(elem) for elem in firstIpOfRange]), "-n", numPing],stdout=subprocess.PIPE).stdout.read()): # If ping response contains string "mil", short for milli-seconds or milisegundos
            return "IP {} is up.".format('.'.join([str(elem) for elem in firstIpOfRange]))
        else:
            return "IP {} is down.".format('.'.join([str(elem) for elem in firstIpOfRange]))
    else: # Any OS but Windows (Unix)   
        if os.system("ping -c " + numPing + " " + '.'.join([str(elem) for elem in firstIpOfRange]) + " > /dev/null 2>&1") == 0:
            return "IP {} is up.".format('.'.join([str(elem) for elem in firstIpOfRange]))
        else:
            return "IP {} is down.".format('.'.join([str(elem) for elem in firstIpOfRange]))

def execCheckRange(numPing):
    for i in secondIpOfRange:
        if i < 256:
            isPossible = True
        else:
            isPossible = False
            break
        
    if isPossible:
        if firstIpOfRange[0] == secondIpOfRange[0] and firstIpOfRange[1] == secondIpOfRange[1] and firstIpOfRange[2] == secondIpOfRange[2] and firstIpOfRange[3] <= secondIpOfRange[3]:
            
            for i in range(firstIpOfRange[3], secondIpOfRange[3]+1):
                if interruption == 2:
                    exit()
                else:
                    print(checkRange(numPing))
                    firstIpOfRange[3] += 1
                    
            return ""

        elif firstIpOfRange[0] == secondIpOfRange[0] and firstIpOfRange[1] == secondIpOfRange[1] and firstIpOfRange[2] < secondIpOfRange[2]:
            for i in range(firstIpOfRange[3], 256):
                print(checkRange(numPing))
                firstIpOfRange[3] += 1
            firstIpOfRange[3] = 0
            firstIpOfRange[2] += 1

            for i in range(firstIpOfRange[3], secondIpOfRange[3]):
                print(checkRange(numPing))
                firstIpOfRange[3] += 1
            return ""

        elif firstIpOfRange[0] == secondIpOfRange[0] and firstIpOfRange[1] < secondIpOfRange[1]:
            for i in range(firstIpOfRange[3], 256):
                print(checkRange(numPing))
                firstIpOfRange[3] += 1
            firstIpOfRange[3] = 0
            firstIpOfRange[2] = 0
            firstIpOfRange[1] += 1

            for i in range(firstIpOfRange[3], secondIpOfRange[3]):
                print(checkRange(numPing))
                firstIpOfRange[3] += 1
            return ""
            
        elif firstIpOfRange[0] < secondIpOfRange[0]:
            for i in range(firstIpOfRange[3], 256):
                print(checkRange(numPing))
                firstIpOfRange[3] += 1
            firstIpOfRange[3] = 0
            firstIpOfRange[2] = 0
            firstIpOfRange[1] = 0
            firstIpOfRange[0] += 1

            for i in range(firstIpOfRange[3], secondIpOfRange[3]):
                print(checkRange(numPing))
                firstIpOfRange[3] += 1
            return ""

        else:
            return "\nWrong IP data values.\n"
    else:
        return "\nWrong IP data values.\n"

# Check if host has a specific opened port
def isOpen(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, int(port)))
    if result == 0:
        print("Port {} is open for host {}.\nPort {} belongs to protocol {}.".format(port, ip, port, socket.getservbyport(port)))
        if socket.getservbyport(port) == 'http':
            getWebServerVersion(ip, port)
        else:
            getEmailServiceVersion(ip, port)
            print(getEmailServiceVersion(ip, port))
    else:
        print("Port {} is not open for host {}.".format(port, ip))

def getWebServerVersion(ip, port):
    httpPoolManager = urllib3.PoolManager()
    request = httpPoolManager.request('GET', ip)
    if 'server' in request.headers:
        print(f'Web Server version name:', request.headers['Server'] + '.')
    else:
        print(f'Web Server version name is down although port {port} is open.')

def getEmailServiceVersion(ip, port):
    with smtplib.SMTP(ip) as smtp:
        smtp.verify(ip)

def main():
    if len(sys.argv) > 2:
        if sys.argv[1] == "-np":
            setIpRange(sys.argv[3])
            execCheckRange(sys.argv[2])
        elif sys.argv[1] == "-pc":
            isOpen(sys.argv[3], int(sys.argv[2]))
    elif len(sys.argv) == 2:
        setIpRange(sys.argv[1])
        execCheckRange("1")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    try:
        main()
    except IndexError:
        print("\nAn error ocurred.\n")
    except ValueError:
        print("\nAn error ocurred.\n")