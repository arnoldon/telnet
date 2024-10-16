"""
Created on Wed Oct 16 17:31:17 2024

@author: arnol
"""

import pexpect

ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

new_hostname = input("Enter the new hostname: ")

session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=30)
result = session.expect(['Username:', pexpect.TIMEOUT])

if result != 0:
    print('--- FAILURE! creating session for:', ip_address)
    exit()

session.sendline(username)
result = session.expect(['Password:', pexpect.TIMEOUT])

if result != 0:
    print('--- FAILURE! entering username:', username)
    exit()

session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

if result != 0:
    print('--- FAILURE! entering password:', password)
    exit()

print('------------------------------------------------------')
print('--- Success! connecting to:', ip_address)
print('--- Username:', username)
print('--- Password:', password)
print('------------------------------------------------------')

# Enter configuration mode
session.sendline('configure terminal')
result = session.expect(['\(config\)#', '#', pexpect.TIMEOUT])

if result == 0 or result == 1:
    print('--- Entered configuration mode successfully.')
else:
    print('--- FAILURE! entering configuration mode. Result:', result)
    exit()

# Send the hostname change command
session.sendline(f'hostname {new_hostname}')
result = session.expect(['#', pexpect.TIMEOUT])

if result == 0:
    print('--- Hostname changed successfully to:', new_hostname)
else:
    print('--- FAILURE! setting hostname. Result:', result)
    exit()

session.sendline('end')
result = session.expect(['#', pexpect.TIMEOUT])

if result == 0:
    print('--- Exited configuration mode successfully.')
else:
    print('--- FAILURE! exiting configuration mode. Result:', result)
    exit()

# Display success message for hostname change
print('--- Hostname successfully changed to:', new_hostname)

# Exit the program
session.sendline('quit')
session.close()
