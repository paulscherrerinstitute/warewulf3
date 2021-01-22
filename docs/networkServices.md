# Network services

## Installation

When installing the warewulf packages, the *dhcp-server*, *ftpf-server* and *http* is pulled as a depency.

## dhcp server

Config is completely handled by warewulf.

## tftp server

I followed [these](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/performing_an_advanced_rhel_installation/preparing-for-a-network-install_installing-rhel-as-an-experienced-user) instructions where it made sense.

## http

No changes made to system, worked out-of-the-box.

## Firewall
Allow incoming connections to the tftp service in the firewall:
```bash
sudo firewall-cmd --add-service=tftp --permanent
sudo firewall-cmd --add-service=http --permanent
```

## Services
warewuld needs `dhcpd`, `tftp.socket` and `httpd` services
```bash
systemctl enable dhcpd
systemctl enable tftp.socket
systemctl enable httpd
```

