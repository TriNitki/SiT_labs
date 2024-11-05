from scapy.all import sniff, IP, ICMP, TCP

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        
        if ICMP in packet:
            print(f"[ICMP] Отправитель: {src_ip}")
        
        elif TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            print(f"[TCP] Sender: {src_ip}, source port: {src_port}, destination port: {dst_port}")

sniff(prn=packet_callback, store=0)