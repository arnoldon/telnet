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

# Check if we were able to enter config mode
if result == 0:
    print('Entered configuration mode successfully.')
else:
    print('Error entering configuration mode. Result:', result)
    exit()

session.sendline('hostname ' + new_hostname)
result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

if result == 0:
    print('Hostname changed successfully.')
else:
    print('Error setting hostname. Result:', result)
    exit()

session.sendline('end')
result = session.expect(['#', pexpect.TIMEOUT])

if result == 0:
    print('Exited configuration mode.')
else:
    print('Error exiting configuration mode. Result:', result)
    exit()

# Display success message for hostname change
print('Hostname successfully changed to:', new_hostname)

# Exit the program
session.sendline('quit')
session.close()
