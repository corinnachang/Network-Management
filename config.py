import getpass
import telnetlib

# user input
HOST = input ("Enter Router IP: ")
user = input ("Enter your telnet username: ")
fa = input ("Enter interface: ")
ipadd = input ("Enter ip address for interface: ")
protocol = input ("Enter protocol (RIP or OSPF): ")

password = getpass.getpass()
tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(b"cisco\n")

# set ip address
tn.write(b"conf t\n")
tn.write(bytes("inter " + fa +"\n", 'utf-8'))
tn.write(b"no shut\n")
tn.write(bytes("ip address " + ipadd + " 255.255.255.0\n", 'utf-8'))
tn.write(b"exit\n")

# define RIP protocol
if protocol == "RIP":
    tn.write(b"router rip\n")
    tn.write(b"version  2\n")
    tn.write(b"no auto-summary\n")
    tn.write(bytes("network "+ ipadd +"\n", 'utf-8'))

# define OSPF protocol
if protocol == "OSPF":
    tn.write(b"ip routing\n")
    tn.write(b"router ospf 1\n")
    tn.write(bytes("network" + ipadd + " 0.0.0.255 area 0\n", 'utf-8'))

tn.write(b"end\n")
tn.write(b"wr mem\n")

print (tn.read_all().decode('ascii'))
