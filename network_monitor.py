import nmap
import json
import time

nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24', arguments='-sn')

devices = []
for host in nm.all_hosts():
    if nm[host]['status']['state'] == 'up':
        devices.append({'ip': host, 'hostname': nm[host].hostname()})

filename = f"network_scan_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
print("Devices Found:")
for x in range(0,len(devices)):
    print(devices[x])
with open(filename, 'w') as file:
    json.dump(devices, file)

prev_scan = None
try:
    with open('previous_network_scan.json', 'r') as file:
        prev_scan = json.load(file)
except FileNotFoundError:
    pass

if prev_scan:
    prev_devices = set((d['ip'], d['hostname']) for d in prev_scan)
    curr_devices = set((d['ip'], d['hostname']) for d in devices)
    new_devices = curr_devices - prev_devices
    if new_devices:
        print('New devices detected:')
        for ip, hostname in new_devices:
            print(f'{ip} ({hostname})')

with open('previous_network_scan.json', 'w') as file:
    json.dump(devices, file)