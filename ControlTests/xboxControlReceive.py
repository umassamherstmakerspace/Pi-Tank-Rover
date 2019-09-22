import os
from socket import *
from controls import *
import logging as log

p = argparse.ArgumentParser(description='Process some integers.')
p.add_argument("-v","--verbose", help="increase output verbosity",
                    action="store_true")

args = p.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


####################################################################
####################################################################
####################################################################
####################################################################

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

####################################################################
####################################################################
####################################################################
####################################################################

controls = Controller()

log.info("Waiting to receive messages...")
while 1:
    (data, addr) = UDPSock.recvfrom(buf)
    log.info("Received message: " + data)

    data = list(data.split(","))
    data = [float(i) for i in data]

    print(data)
    if buttons_packet[controls.select] == 1:
        UDPSock.close()
        log.warning("[    MISSION STATUS     ]: System exit")
        raise SystemExit

UDPSock.close()
os._exit(0)
