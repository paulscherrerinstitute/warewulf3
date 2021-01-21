# Master node configuration

## Network

### static IP on provisioning NIC
The NIC the provisioning is handled on need a static IP.
I use 10.0.0.1 on `enp2s0` in this setup

```bash
ip a
...
3: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 68:05:ca:b0:8c:4f brd ff:ff:ff:ff:ff:ff
...
```

```bash
vim /etc/sysconfig/network-scripts/ifcfg-enp2s0
```
```sh
TYPE=Ethernet
DEVICE=enp2s0
BOOTPROTO=static
ONBOOT=yes
NAME=enp2s0
UUID=cef48d42-0f82-4def-a200-3858869c7105
IPADDR="10.0.0.1"
PREFEIX="24"
```
reboot
```bash
ip a
...
3: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 68:05:ca:b0:8c:4f brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.1/8 brd 10.255.255.255 scope global noprefixroute enp2s0
       valid_lft forever preferred_lft forever
    inet6 fe80::6a05:caff:feb0:8c4f/64 scope link 
       valid_lft forever preferred_lft forever
...
```

### Configuring the provision package
Make sure /etc/warewulf/provision.conf has "network device" set to your current network device. (The default is eth1.)
Example for /etc/warewulf/provision.conf:
In this case `enp2s0` is the right choise as this device is now on a static IP
```bash
sudo vim /etc/warewulf/provision.conf
...
# What is the default network device that the master will use to
# communicate with the nodes?
network device = enp2s0
...
```

### Add a node
#### Test node
```bash
sudo wwsh node new n0000 --netdev=enp25s0 --hwaddr=00:00:00:00:00:01 --ipaddr=10.0.0.2 --fqdn 'gfa-ecmc-01.psi.ch'
sudo wwsh node list
NAME                GROUPS              IPADDR              HWADDR             
================================================================================
n0000               UNDEF               10.0.0.2            00:00:00:00:00:01  

```
#### `wwsh dhcp`
```bash
sudo wwsh dhcp update
```
Verify the **dhcpd.conf** was created as expected
```bash
sudo cat /etc/dhcp/dhcpd.conf
...
group {
   # Evaluating Warewulf node: n0000 (DB ID:5)
   # Adding host entry for n0000-enp25s0
   host n0000-enp25s0 {
      option host-name n0000;
      hardware ethernet 00:00:00:00:00:01;
      fixed-address 10.0.0.2;
      next-server 10.0.0.1;
   }
}
```
Good to start dhcp server
```bash
sudo wwsh dhcp restart
```
And verify again the dhcpd service is up.
```bash
sudo service dhcpd status
● dhcpd.service - DHCPv4 Server Daemon
   Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2021-01-21 15:54:33 CET; 9min ago
     Docs: man:dhcpd(8)
           man:dhcpd.conf(5)
 Main PID: 2932 (dhcpd)
   Status: "Dispatching packets..."
    Tasks: 1 (limit: 100458)
   Memory: 8.0M
   CGroup: /system.slice/dhcpd.service
           └─2932 /usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid

Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]: 
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]: No subnet declaration for enp0s25 (129.129.144.76).
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]: ** Ignoring requests on enp0s25.  If this is not what
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]:    you want, please write a subnet declaration
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]:    in your dhcpd.conf file for the network segment
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]:    to which interface enp0s25 is attached. **
Jan 21 15:54:33 pc13397.psi.ch systemd[1]: Started DHCPv4 Server Daemon.
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]: 
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]: Sending on   Socket/fallback/fallback-net
Jan 21 15:54:33 pc13397.psi.ch dhcpd[2932]: Server starting service.
```
Nice!
