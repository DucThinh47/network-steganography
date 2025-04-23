from scapy.all import *

pkt = IP(src="173.30.0.3", dst="173.30.0.4") / TCP(dport=80, sport=12345, reserved=5, flags="A")
send(pkt, iface="eth0")

