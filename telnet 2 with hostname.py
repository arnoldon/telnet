# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:31:17 2024

@author: arnol
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:08:57 2024

@author: arnol
"""

# Import required modules/packages/library
import pexpect

# Define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

# Prompt user for the new hostname
new_hostname = input("Enter the new hostname: ")

# Create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT])

# Check for error, if it exists, then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session is expecting username, enter details
session.sendline(username)
result = session.expect(['Password:', pexpect.TIMEOUT])

# Check for error, if it exists, then display error and exit
if result != 0:
    print('--- FAILURE! entering username: ', username)
    exit()

# Session is expecting password, enter details
session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

# Check for error, if it exists, then display error and exit
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()

# Display a success message if it works
print('------------------------------------------------------')
print('--- Success! connecting to : ', ip_address)
print('--- Username: ', username)
print('--- Password: ', password)
print('------------------------------------------------------')

# Change the hostname
session.sendline('configure terminal')
session.expect(['\(config\)#', pexpect.TIMEOUT])

# Send the hostname change command
session.sendline(f'hostname {new_hostname}')
result = session.expect([f'{new_hostname}#', pexpect.TIMEOUT])

# Check for error, if it exists, then display error and exit
if result != 0:
    print(f'--- FAILURE! changing hostname to: {new_hostname}')
else:
    print(f'--- Success! Hostname changed to: {new_hostname}')

# Exit configuration mode and quit session
session.sendline('end')
session.expect([f'{new_hostname}#', pexpect.TIMEOUT])
session.sendline('quit')
session.close()
