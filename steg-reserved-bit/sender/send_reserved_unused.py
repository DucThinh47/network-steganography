from scapy.all import IP, TCP, send
import time

# Convert message to 3-bit groups
def text_to_bit_groups(message):
    bitstream = ''.join(format(ord(c), '08b') for c in message)
    groups = [bitstream[i:i+3] for i in range(0, len(bitstream), 3)]
    if len(groups[-1]) < 3:
        groups[-1] = groups[-1].ljust(3, '0')
    return groups

dst_ip = "173.30.0.4"
src_ip = "173.30.0.3"
dst_port = 80
iface = "eth0"

message = input("Enter the message to hide: ")
bit_groups = text_to_bit_groups(message)
print(f"[+] Total 3-bit groups: {len(bit_groups)}")

for idx, group in enumerate(bit_groups):
    reserved_value = int(group, 2)
    pkt = IP(src=src_ip, dst=dst_ip) / TCP(dport=dst_port, sport=12345, seq=1000 + idx, reserved=reserved_value, flags="A")
    send(pkt, iface=iface, verbose=False)
    print(f"Sent group {idx+1}: bits={group}, reserved={reserved_value}")
    time.sleep(0.3)

for i in range(3):
    end_pkt = IP(src=src_ip, dst=dst_ip) / TCP(dport=dst_port, sport=12345, seq=2000 + i, reserved=7, flags="F")
    send(end_pkt, iface=iface, verbose=False)
    print(f"[+] Sent end-of-transmission marker #{i+1}")
    time.sleep(0.3)

