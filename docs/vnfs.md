# Debian10 (buster)

## chroot
Create _chroot_ environment. The **mkchroot-debian10.sh** will install several packages in adition to the minbase, including the rt-kernel.
Look into the script for details.
The list of packages is WIP.

```bash
cd warewulf3/vnfs/bin/
mkdir -p /opt/warewulf/chroot/debian-rt
sudo ./mkchroot-debian10.sh /opt/warewulf/chroot/debian-rt
```

verify the chroot is functional
```bash
sudo wwmngchroot -c /opt/warewulf/chroot/debian-rt -s
```
This should enter the chroot-env provide a prompt.

### VNFS

#### install rpm
```bash
cd 
sudo dnf install ~/rpmbuild/RPMS/noarch/warewulf-vnfs-3.9.0-0.9883afc.el8.noarch.rpm 

```

#### create vnfs
```bash
sudo wwvnfs debian-rt --chroot=/opt/warewulf/chroot/debian-rt
```
This should result in someting like.
```bash
_FORTIFY_SOURCE requires compiling with optimization (-O) at /usr/lib64/perl5/features.ph line 207.
Creating VNFS image from debian-rt
Compiling hybridization link tree                           : 0.04 s
Building file list                                          : 0.18 s
Compiling and compressing VNFS                              : 124.87 s
Adding image to datastore                                   : 3.74 s
Total elapsed time                                          : 128.82 s
```

#### bootstrap the vnfs
```bash
sudo wwbootstrap --chroot=/opt/warewulf/chroot/debian-rt 4.19.0-13-rt-amd64
```
The output should be similar to this
```bash
Number of drivers included in bootstrap: 774
Building and compressing bootstrap
Integrating the Warewulf bootstrap: 4.19.0-13-rt-amd64
Including capability: provision-adhoc
Including capability: provision-files
Including capability: provision-selinux
Including capability: provision-vnfs
Including capability: setup-filesystems
Including capability: setup-ipmi
Including capability: transport-http
Compressing the initramfs
Locating the kernel object
Bootstrap image '4.19.0-13-rt-amd64' is ready
Done.
```

### check with `wwsh`

```bash
wwsh
Warewulf> bootstrap list
BOOTSTRAP NAME            SIZE (M)      ARCH
4.19.0-13-rt-amd64        30.0          x86_64
Warewulf> vnfs list 
VNFS NAME            SIZE (M)   ARCH       CHROOT LOCATION
debian-rt            138.1      x86_64     /opt/warewulf/chroot/debian-rt
```

looks good so far!!!
