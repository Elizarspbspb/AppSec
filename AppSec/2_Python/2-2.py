# список найденных URL
white_port = [80, 22, 443, 3389]
black_port = [21, 23, 135]

try:
   port = int(input())
except ValueError:
   print('Enter only integer, please')

# «Сканер портов (симуляция)»
def scan_ports(port):
    for p in white_port:
        if port == p:
            print("Port", port, "is OPEN.")
            return
    for p in black_port:
        if port == p:
            print("Port", port, "is OPEN and considered VULNERABLE!")
            return
    print("Port", port, "is closed.")

scan_ports(port)