# Build chroot setup

## chroot base

```bash
cd warewulf3/vnfs/bin/
sudo ./mkchroot-debian10.sh /opt/warewulf/chroot/debian-build
```

## Build essentials and kernel-headers

```bash
sudo wwmngchroot -c /opt/warewulf/chroot/debian-build/ -s
apt install build-essential linux-headers-4.19.0-13-rt-amd64 dh-autoreconf
```

### etherlab master
```bash
sudo wwmngchroot -c /opt/warewulf/chroot/debian-build/ -s
apt install dh-autoreconf hgsubversion
# pull sources
hg clone http://hg.code.sf.net/p/etherlabmaster/code ethercat-hg
cd ethercat-hg
# switch to stable-1/5 branch as this is more up-to-date
hg update stable-1.5
./bootstrap
./configure --enable-generic=yes --enable-e1000=no --enable-e1000e=no --enable-igb=no --enable-8139too=no --enable-r8169=no --enable-hrtimer=yes --disable-debug-if --disable-debug-ring --enable-sii-assign=yes --enable-eoe=no --with-linux-dir=/usr/src/linux-headers-4.19.0-13-rt-amd64 --prefix=/opt/ethercat
make all modules install
```

copy the product (don't forget the kernel modules) to your lean chroot and run wwnvnfs on it.

