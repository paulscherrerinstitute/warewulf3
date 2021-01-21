# tftp server

I followed [these](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/performing_an_advanced_rhel_installation/preparing-for-a-network-install_installing-rhel-as-an-experienced-user) instructions.

## Installation

When installing the warewulf packages, the ftpf-server is pulled as a depency.

## Firewall
Allow incoming connections to the tftp service in the firewall:
```bash
firewall-cmd --add-service=tftp
```

## Services
warewuld needs `dhcpd`, `tftp.socket` and `httpd` services
```bash
systemctl enable dhcpd
systemctl enable tftp.socket
systemctl enable httpd
```

