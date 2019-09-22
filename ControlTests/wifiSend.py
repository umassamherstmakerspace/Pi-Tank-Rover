import os
from socket import *
host = "172.20.10.12" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = [1.0,2.0,3.0]
    s = ""
    for i in data:
        s += str(i) + ","
    s = s.encode()
    UDPSock.sendto(s, addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
