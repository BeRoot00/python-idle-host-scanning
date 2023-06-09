#!/usr/bin/python
import os
import sys
from scapy.all import *

#To verify if I'm in root session
def is_root():
    return os.getuid() == 0


def run_scan(zombie, target, port):
    print('Scan %s port %d using %s as zombie' % (target, port, zombie))
    # get zombie's IP id with a SYN/ACK
    p1 = sr1(IP(dst=zombie) / TCP(sport=12345, dport=(321), flags="SA"), verbose=0)
    initial_id = p1.id

    print(' Zombie intial IP id is: ', initial_id)

    # SYN to target with spoofed IP from zombie
    p2 = send(IP(dst=target, src=zombie) / TCP(sport=12345, dport(port), flags="S"), verbose=0)

    # SYN/ACK to zombie to see if it heard back from the target
    p3 = sr1(IP(dst=zombie) / TCP(sport=12345, dport=(321), flags="SA"), verbose=0)
    final_id = p3.id

    print('Zombie final IP id', final_id)

    if final_id - initial_id < 2:
        print(' Port %d: is closed' % port)
    else:
        print(' Port %d: is open' % port)


if __name__ == '__main__':
    if not is_root():
        print('[!] Must be run as root. Quitting')
        sys.exit(1)

    if len(sys.argv) < 4 or sys.argv[1] == '-h':
        print('Usage: fileName.py zombieIP targetIP targetPort')
        sys.exit(1)

    run_scan(sys.argv[1], sys.argv[2], int(sys.argv[3]))
