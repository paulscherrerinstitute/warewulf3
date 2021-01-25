# nfs server

I followed [this](https://computingforgeeks.com/install-and-configure-nfs-server-on-centos-rhel/) guide.

## exports

Create directory `/opt/apps/ethercat` and export it via nfs read-only

```bash
$ sudo mkdir -p /opt/apps/ethercat
$ vim /etc/exports

# /opt/apps
/opt/apps *(ro,sync)
```

## restart nfs server

```bash
$ sudo exportfs -rav
exporting *:/opt/apps
```

## firewall

Of course, the firewall is in the way, so lets poke a hole.

```bash
sudo firewall-cmd --add-service=nfs --permanent
sudo firewall-cmd --add-service={nfs3,mountd,rpc-bind} --permanent 
sudo firewall-cmd --reload 
```

## mount on the node(s)

```bash
ssh root@n0000
mount -t nfs4 10.0.0.1:/opt/apps /opt/apps

$ ls /opt/ -la
total 0
drwxr-xr-x  5 root  root  100 Jan 25 08:50 .
drwxrwxr-x 19 kivel kivel 580 Jan 22 21:21 ..
drwxr-xr-x  3 root  root   22 Jan 25  2021 apps
```

