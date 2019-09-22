import napalm, paramiko, netmiko, getpass
driverios = napalm.get_network_driver('ios')

def switchLogin(ip, u, p):
	global device
	try:
		device = driverios(hostname=ip, username=u, password=p, optional_args={'secret': p})
		device.open()
		print('\n[+] - Connection Open\n')
		return True
	except paramiko.AuthenticationException as auth:
		print('Incorrect Username / Password')
		return False
	except Exception as e:
		raise

def switchClose():
	device.close()
	print('\n[+] - Connection Closed')

def switchDetails():
	hostname = device.get_facts()['hostname']
	serialNumber = device.get_facts()['serial_number']
	osVersion = device.get_facts()['os_version']

	print('-'*40)
	print('Hostname: {}\nSerial Number: {}\nOS Version: {}'.format(hostname, serialNumber, osVersion))
	print('-'*40)

def switchinterfaces():
	print('-'*40)
	interfaces = device.get_interfaces()
	for e in interfaces:
		if interfaces.get(e, '')['is_enabled'] == True and interfaces.get(e, '')['is_up'] == True:
			print("Interface: {} - {}".format(e, 'Enabled and connected'))
		elif interfaces.get(e, '')['is_enabled'] == True and interfaces.get(e, '')['is_up'] == False:
			print("Interface: {} - {}".format(e, 'Enabled and Disconnected'))
		elif interfaces.get(e, '')['is_enabled'] == False:
			print("Interface: {} - {}".format(e, 'Disabled'))
	print('-'*40)

def main():
	uname = input('Username: ')
	pword = getpass.getpass(prompt='Password: ')
	## impliment somekind of mass ip to list - ipList
	ipList = ['192.168.1.1', '192.168.0.1']
	for ip in ipList:
		while True:
			if switchLogin(ip, uname, pword) == True:
				break
			else:
				uname = input('Username: ')
				pword = getpass.getpass(prompt='Password: ')
		switchDetails()
		switchinterfaces()
		switchClose()

if __name__ == '__main__':
	main()
