Project 9 - Financial Institution Network - Device Configurations

## ROUTERS & L3-SWITCHES ##

## ALL ROUTERS ##

En
Conf t

Enable password cisco
Line console 0
Password cisco
Login
Banner motd *** No authorized access will be punishable ***
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.net
Username admin
Crypto key generate rsa
1024
Line vty 0 15
Login local
Transport input ssh
Ip ssh version 2

//ACL for SSH access only from IT. Remember apply that to SVIs

Access-list 10 permit 192.168.20.224 0.0.0.31 
Access-list 10 deny any
Line vty 0 15
Access-class 10 in
Exit

Do wr

## ALL L3-SWITCHES ##

En
Conf t
Int ran gi1/0/1-7 
No shut
Exit

Enable password cisco
Line console 0
Password cisco
Login
Banner motd *** No authorized access will be punishable ***
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.net
Username admin
Crypto key generate rsa
1024
Line vty 0 15
Login local
Transport input ssh
Ip ssh version 2


//ACL for SSH access only from IT. Remember apply that to SVIs

Access-list 10 permit 192.168.20.224 0.0.0.31 
Access-list 10 deny any
Line vty 0 15
Access-class 10 in
Exit

Do wr

## HQ-Router ##

En
Conf t
Hostname HQ-Router

int gi0/0
no shut
ip address 192.168.21.18 255.255.255.252
exit

int gi0/1
no shut
ip address 192.168.21.22 255.255.255.252
exit

int se0/3/0
no shut
ip address 190.200.100.1 255.255.255.252
exit

int se0/3/1
no shut
ip address 190.200.100.5 255.255.255.252
exit

Router ospf 10
Router-id 4.4.4.4
Auto-cost reference-bandwidth 1000000
Network 192.168.21.16 0.0.0.3 area 0
Network 192.168.21.20 0.0.0.3 area 0
Network 190.200.100.0 0.0.0.3 area 0
Network 190.200.100.4 0.0.0.3 area 0
Exit

//PAT configuration

Int ran g0/0-1
Ip nat inside
Exit
Int se0/3/0
Ip nat outside
Exit
Int se0/3/1
Ip nat outside
Exit

Access-list 50 permit 192.168.20.0 0.0.0.63
Access-list 50 permit 192.168.20.64 0.0.0.63
Access-list 50 permit 192.168.20.128 0.0.0.63
Access-list 50 permit 192.168.20.192 0.0.0.31
Access-list 50 permit 192.168.20.224 0.0.0.31

ip nat inside source list 50 interface se0/3/0 overload
Ip nat inside source list 50 interface se0/3/1 overload
Exit

//GRE over IP-Sec tunnel configuration. HQ <--> Server-Side-Site
//ACL format: ip + source network & WC + destination network & WC

License boot module c2900 technology-package securityk9
Yes
Do wr
Do reload
Yes

Int tunnel 1
Ip address 192.168.0.1 255.255.255.252
Tunnel source serial 0/3/0
Tunnel destination 190.200.100.9
Exit

Access-list 110 permit ip 192.168.20.0 0.0.0.63 192.168.21.0 0.0.0.15
Access-list 110 permit ip 192.168.20.64 0.0.0.63 192.168.21.0 0.0.0.15
Access-list 110 permit ip 192.168.20.128 0.0.0.63 192.168.21.0 0.0.0.15
Access-list 110 permit ip 192.168.20.192 0.0.0.31 192.168.21.0 0.0.0.15
Access-list 110 permit ip 192.168.20.224 0.0.0.31 192.168.21.0 0.0.0.15
Access-list 110 permit gre any any

Crypto isakmp policy 10
Encryption aes 256
Authentication pre-share
Group 5
Exit

Crypto isakmp key vpn-project9 address 190.200.100.9
Crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
Crypto map VPN-MAP 10 ipsec-isakmp
Description VPN connection to Server-Side Site
Set peer 190.200.100.9
Set transform-set VPN-SET
Match address 110
Exit

Int se0/3/0
Crypto map VPN-MAP
Exit
Do wr

## SSS-Router ##

En
Conf t
Hostname SSS-Router

Int se0/3/0
No shut
Ip address 190.200.100.9 255.255.255.252
Exit

Int se0/3/1
No shut
Ip address 190.200.100.13 255.255.255.252
Exit

Int g0/0
No shut
No ip address
Exit

//Inter-Vlan Routing for SSS Network 

Int g0/0.60
Encapsulation dot1q 60
Ip address 192.168.21.1 255.255.255.240
Exit


Router ospf 10
Router-id 5.5.5.5
Auto-cost reference-bandwidth 1000000
Network 192.168.0.1 0.0.0.3 area 0
Network 192.168.21.0 0.0.0.15 area 0
Network 190.200.100.8 0.0.0.3 area 0
Network 190.200.100.12 0.0.0.3 area 0
Exit

//GRE over IP-Sec tunnel configuration - HQ <--> Server-Side-Site
//ACL format: ip + source network & WC + destination network & WC

License boot module c2900 technology-package securityk9
Yes
Do reload
Yes

Int tunnel 1
Ip address 192.168.0.2 255.255.255.252
Tunnel source serial 0/3/0
Tunnel destination 190.200.100.1
Exit

Access-list 110 permit ip 192.168.21.0 0.0.0.15 192.168.20.0 0.0.0.63
Access-list 110 permit ip 192.168.21.0 0.0.0.15 192.168.20.64 0.0.0.63
Access-list 110 permit ip 192.168.21.0 0.0.0.15 192.168.20.128 0.0.0.63
Access-list 110 permit ip 192.168.21.0 0.0.0.15 192.168.20.192 0.0.0.31
Access-list 110 permit ip 192.168.21.0 0.0.0.15 192.168.20.224 0.0.0.31
Access-list 110 permit gre any any

Crypto isakmp policy 10
Encryption aes 256
Authentication pre-share
Group 5
Exit

Crypto isakmp key vpn-project9 address 190.200.100.1
Crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
Crypto map VPN-MAP 10 ipsec-isakmp
Description VPN connection to HQ Network
Set peer 190.200.100.1
Set transform-set VPN-SET
Match address 110
Exit

Int se0/3/0
Crypto map VPN-MAP
Exit
Do wr

## HQ-VoIP-Router ##

En 
Conf t
Hostname HQ-VoIP-Router

Int fa0/0
No shut

Int fa0/0.120
No shut
Encapsulation dot1q 120
Ip address 10.10.10.1 255.255.255.0
Exit

Router ospf 10
Router-id 3.3.3.3
Auto-cost reference-bandwidth 1000000
Network 10.10.10.0 0.0.0.255 area 0
Exit

//DHCP server for IP phones + telephony service

Service dhcp
Ip dhcp pool VoIP
Network 10.10.10.0 255.255.255.0
Default-router 10.10.10.1
Option 150 ip 10.10.10.1
Dns-server 10.10.10.1
Ip dhcp excluded-address 10.10.10.1

Telephony-service
Max-ephones 20
Max-dn 20
Ip source-address 10.10.10.1 port 2000
Auto assign 1 to 20
Exit

Ephone-dn 1
Number 401
Exit
Ephone-dn 2
Number 402
Exit
Ephone-dn 3
Number 403
Exit
ephone-dn 4
number 404
exit
ephone-dn 5
number 405
exit
ephone-dn 6
Number 406
Exit
Ephone-dn 7
Number 407
Exit
Ephone-dn 8
Number 408
Exit
ephone-dn 9
number 409
exit
ephone-dn 10
number 410
exit
do wr

## HQ-L3-Switch1 ##

En
Conf t
Hostname HQ-L3-Switch1

Vlan 10
Name HR
Vlan 20
Name CS
Vlan 30
Name MK
Vlan 40
Name LM
Vlan 50
Name IT
Vlan 120
Name Voice
Vlan 99
Name native
Exit

//Inter-VLAN Routing + DHCP helper-address
//Remember: in L3-SW it is no necessary to create sub interfaces
//			Just invoke respective VLAN interface.

int vlan 10
ip address 192.168.20.1 255.255.255.192
ip helper-address 192.168.21.5
exit

int vlan 20
ip address 192.168.20.65 255.255.255.192
ip helper-address 192.168.21.5
exit

int vlan 30
ip address 192.168.20.129 255.255.255.192
ip helper-address 192.168.21.5
exit

int vlan 40
ip address 192.168.20.193 255.255.255.224
ip helper-address 192.168.21.5
exit

int vlan 50
ip address 192.168.20.225 255.255.255.224
ip helper-address 192.168.21.5
exit

Int ran gi1/0/2-7
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int g1/0/1
No shut
No switchport
Ip address 192.168.21.17 255.255.255.252
Exit

Ip routing
Router ospf 10
Router-id 1.1.1.1
Auto-cost reference-bandwidth 1000000
Network 192.168.20.0 0.0.0.63 area 0
Network 192.168.20.64 0.0.0.63 area 0
Network 192.168.20.128 0.0.0.63 area 0
Network 192.168.20.193 0.0.0.31 area 0
Network 192.168.20.224 0.0.0.31 area 0
Network 10.10.10.0 0.0.0.255 area 0
Network 192.168.21.16 0.0.0.3 area 0
Exit

Do wr

## HQ-L3-Switch2 ##

En
Conf t
Hostname HQ-L3-Switch2

Vlan 10
Name HR
Vlan 20
Name CS
Vlan 30
Name MK
Vlan 40
Name LM
Vlan 50
Name IT
Vlan 120
Name Voice
Vlan 99
Name native
Exit

//Inter-VLAN Routing + DHCP helper-address
//Remember: in L3-SW it is no necessary to create sub interfaces
//			Just invoke respective VLAN interface.

int vlan 10
ip address 192.168.20.1 255.255.255.192
ip helper-address 192.168.21.5
exit

int vlan 20
ip address 192.168.20.65 255.255.255.192
ip helper-address 192.168.21.5
exit

int vlan 30
ip address 192.168.20.129 255.255.255.192
ip helper-address 192.168.21.5
exit

int vlan 40
ip address 192.168.20.193 255.255.255.224
ip helper-address 192.168.21.5
exit

int vlan 50
ip address 192.168.20.225 255.255.255.224
ip helper-address 192.168.21.5
exit

Int ran gi1/0/2-6
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int gi1/0/1
No shut
No switchport
Ip address 192.168.21.21 255.255.255.252
Exit

Ip routing
Router ospf 10
Router-id 2.2.2.2
Auto-cost reference-bandwidth 1000000
Network 192.168.20.0 0.0.0.63 area 0
Network 192.168.20.64 0.0.0.63 area 0
Network 192.168.20.128 0.0.0.63 area 0
Network 192.168.20.193 0.0.0.31 area 0
Network 192.168.20.224 0.0.0.31 area 0
Network 192.168.21.20 0.0.0.3 area 0
Exit

## SafariCOM-ISP ##

En
Conf t
Hostname SafariCOM-ISP

Int se0/3/0
No shut
Ip address 190.200.100.2 255.255.255.252
Exit

Int se0/3/1
No shut
Ip address 190.200.100.10 255.255.255.252
Exit


Router ospf 10
Router-id 6.6.6.6
Auto-cost reference-bandwidth 1000000
Network 190.200.100.0 0.0.0.3 area 0
Network 190.200.100.8 0.0.0.3 area 0
Exit
Do wr

## JTL-ISP ##

En
Conf t
Hostname JTL-ISP

Int se0/3/0
No shut
Ip address 190.200.100.14 255.255.255.252
Exit

Int se0/3/1
No shut
Ip address 190.200.100.6 255.255.255.252
Exit

Router ospf 10
Router-id 7.7.7.7
Auto-cost reference-bandwidth 1000000
Network 190.200.100.4 0.0.0.3 area 0
Network 190.200.100.12 0.0.0.3 area 0
Exit

### SWITCHES ###

## ALL SWITCHES ##

En
Conf t
Enable password cisco
Line console 0
Password cisco
Login
Banner motd *** No authorized access will be punishable ***
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.net
Username admin
Crypto key generate rsa
1024
Line vty 0 15
Login local
Transport input ssh
Ip ssh version 2

Vlan 10
Name HR
Vlan 20
Name CS
Vlan 30
Name MK
Vlan 40
Name LM
Vlan 50
Name IT
Vlan 60
Name SSS
Vlan 120
Name Voice
Vlan 99
Name native
Exit

Do wr

## HR-Switch ##
En
Conf t
Hostname HR-Switch

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int ran fa0/1-24
No shut
Switchport mode access
Switchport access vlan 10
Switchport voice vlan 120
Exit
Do wr

## CS-Switch ##

En
Conf t
Hostname CS-Switch

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int ran fa0/1-24
No shut
Switchport mode access
Switchport access vlan 10
Switchport voice vlan 120
Exit
Do wr

## MK-Switch ##
En
Conf t
Hostname MK-Switch

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int ran fa0/1-24
No shut
Switchport mode access
Switchport access vlan 30
Switchport voice vlan 120
Exit
Do wr

## LM-Switch ##

En
Conf t
Hostname LM-Switch

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int ran fa0/1-24
No shut
Switchport mode access
Switchport access vlan 40
Switchport voice vlan 120
Exit
Do wr

## IT-Switch ##

En
Conf t
Hostname IT-Switch

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int ran fa0/1-24
No shut
Switchport mode access
Switchport access vlan 50
Switchport voice vlan 120
Exit
Do wr

## SSS-Switch ##

En
Conf t
Hostname SSS-Switch

Vlan 60
Name SSS

Int ran fa0/1-5
No shut
Switchport mode access
Switchport access vlan 60
Switchport port-security maximum 1
Switchport port-security mac-address sticky
Switchport port-security violation restrict
Exit

Int g0/1
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int g0/2
Switchport mode access
Switchport access vlan 99
Shut
Exit

Int ran fa0/6-24
Switchport mode access
Switchport access vlan 99
Shut
Exit

Do wr
