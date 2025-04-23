from scapy.all import sniff
import time

bitstream = ""
end_marker_seen = False

def packet_handler(pkt):
    global bitstream, end_marker_seen

    if pkt.haslayer("IP") and pkt.haslayer("TCP"):
        ip = pkt["IP"]
        tcp = pkt["TCP"]
        if ip.src == "173.30.0.3" and ip.dst == "173.30.0.4":
            reserved_bits = tcp.reserved
            seq = tcp.seq
            flags = tcp.flags

            # Xác định đúng gói kết thúc (reserved = 7 và có cờ FIN)
            if reserved_bits == 7 and flags & 0x01:
                print("[+] End-of-transmission marker received.")
                end_marker_seen = True
                return

            bin_str = format(reserved_bits, '03b')
            bitstream += bin_str
            print(f"Received packet (seq={seq}), reserved={reserved_bits} → bits={bin_str}")

def stop_filter(pkt):
    return end_marker_seen

print("[*] Listening for hidden message packets...")
sniff(
    filter="tcp and src host 173.30.0.3 and dst host 173.30.0.4",
    iface="eth0",
    prn=packet_handler,
    stop_filter=stop_filter,
    timeout=300
)

# Chuyển bitstream → ký tự
message = ""
for i in range(0, len(bitstream), 8):
    byte = bitstream[i:i+8]
    if len(byte) < 8:
        break
    char = chr(int(byte, 2))
    message += char

print(f"\n[+] Hidden message extracted: {message}")

