import napalm, paramiko, netmiko, getpass, sqlite3, csv

driverios = napalm.get_network_driver('ios')

currentSwitch = []

def switchLogin(ip, u, p):
	global device
	try:
		device = driverios(hostname=ip, username=u, password=p, optional_args={'secret': p})
		device.open()
		print('\n[+] - Connection Open ({})\n'.format(ip))
		currentSwitch.append(u)
		currentSwitch.append(ip)
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
	currentSwitch.append(hostname)
	currentSwitch.append(serialNumber)
	currentSwitch.append(osVersion)

def switchinterfaces():
	print('-'*40)
	interfaces = device.get_interfaces()
	for e in interfaces:
		if interfaces.get(e, '')['is_enabled'] == True and interfaces.get(e, '')['is_up'] == True:
			msg = "{} - {}".format(e, 'Enabled and Connected')
			print('Interface: {}'.format(msg))
			currentSwitch.append(msg)
		elif interfaces.get(e, '')['is_enabled'] == True and interfaces.get(e, '')['is_up'] == False:
			msg = "{} - {}".format(e, 'Enabled and Disconnected')
			print('Interface: {}'.format(msg))
			currentSwitch.append(msg)
		elif interfaces.get(e, '')['is_enabled'] == False:
			msg = "{} - {}".format(e, 'Disabled')
			print('Interface: {}'.format(msg))
			currentSwitch.append(msg)
	print('-'*40)

def outputCSVfile(details):
	global currentSwitch
	with open('output.csv', 'a', newline='') as csvfile:
		csvWriter = csv.writer(csvfile)
		csvWriter.writerow(details)
	currentSwitch = []

def main():
	try:
		with open('iplist.conf', 'r') as f:
			l = f.read().splitlines()
	except Exception as e:
		raise

	uname = input('Username: ')
	pword = getpass.getpass(prompt='Password: ')
	## impliment somekind of mass ip to list - ipList

	ipList = l
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
		outputCSVfile(currentSwitch)

if __name__ == '__main__':
	main()
