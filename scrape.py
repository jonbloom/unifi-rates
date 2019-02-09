import unifiapi
from dotenv import load_dotenv
import os
from pprint import pprint
from tabulate import tabulate

load_dotenv()

UNIFI_SITE_ID = os.getenv('UNIFI_SITE_ID')
UNIFI_ENDPOINT = os.getenv('UNIFI_ENDPOINT')
UNIFI_USERNAME = os.getenv('UNIFI_USERNAME')
UNIFI_PASSWORD = os.getenv('UNIFI_PASSWORD')


controller = unifiapi.controller(endpoint=UNIFI_ENDPOINT, username=UNIFI_USERNAME, password=UNIFI_PASSWORD, verify=False)
site = controller.sites[UNIFI_SITE_ID]()

clients = site.active_clients()

wireless_clients = list(filter(lambda x: x['is_wired'] == False, clients))

to_tabulate = []

for client in wireless_clients:
	if 'name' in client.keys():
		_name = client['name']
	elif 'hostname' in client.keys():
		_name = client['hostname']
	else:
		_name = client['mac']

	client['_name'] = _name

	to_tabulate.append([client['_name'], '{0} dBm'.format(client['rssi']), '{0} Mb/s'.format(client['tx_rate']/1000), '{0} Mb/s'.format(client['rx_rate']/1000),])

print(tabulate(to_tabulate, headers=['Name', 'RSSI', 'TX rate', 'RX rate']))