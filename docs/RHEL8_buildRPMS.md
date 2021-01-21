# RHEL8 build procedure
This documentaion summarizes the steps needed for building _warewulf3_ on a RHEL8 host system.
It utilizes ansible to prepare the host.
Susquently steps are undergone to build RPM packages.

## Prepare
### Ansible
Pull the repo ... obviously.
- Modifiy the **inventory.yml** file in the **ansible** directory to match your target host.
- Run the ansible playbooks for **mariadb** and **build preparation**.
```bash
cd ansible
ansible-playbook installMariaDb_RHEL8.yaml
ansible-playbook prepareWarewulfInstallation_RHEL8.yaml
```
This should prepare your target host for the _warewulf3_ build process.

### Build dependencies not handled by ansible ... yet

#### Device mapper libraries
The 'device-mapper-devel' package is only availble on CentOS in 'powertools'. Either I'm to dumb to find a solution on RHEL8 or it's not there.
So lets just build the lib from the sources.
A submodule can be found in **3rdParty/lvm2**, with instructions how to build just the **device-mapper** lib.
```bash
cd 3rdParty/lvm2/
./configure
make device-mapper
sudo make install_device-mapper
```
This should do the trick.

### Build RPMs
The following steps resemble what's done in the _circleci_ script found in  **.circleci**.

#### Build Common
```bash
cd common
./autogen.sh
make test
make dist-gzip
rpmbuild -D "_sourcedir $PWD" -ba ./warewulf-common.spec
```

#### Install warewulf-common
```bash
GITVERSION=$(git show -s --pretty=format:%h)
DIST=$(rpm --eval '%{dist}')
yum -y install ~/rpmbuild/RPMS/noarch/\
warewulf-common-3.9.0-0.${GITVERSION}${DIST}.noarch.rpm
```

#### Build Cluster
```bash
cd cluster
./autogen.sh
make dist-gzip
rpmbuild -D "_sourcedir $PWD" -ba ./warewulf-cluster.spec
```

### Build IPMI
```bash
cd ipmi
./autogen.sh --with-local-ipmitool=yes
make dist-gzip
rpmbuild -D "_sourcedir $PWD" -ba ./warewulf-ipmi.spec
```

### Build Provision
```bash
cd provision
./autogen.sh --with-local-e2fsprogs --with-local-libarchive \
   --with-local-parted --with-local-partprobe
make dist-gzip
rpmbuild -D "_sourcedir $PWD" -D "cross_compile 0" \
   -D "mflags -j$(/usr/bin/getconf _NPROCESSORS_ONLN)" \
   -ba ./warewulf-provision_RHEL8.spec
```

### Build VNFS
```bash
cd vnfs
./autogen.sh
make dist-gzip
rpmbuild -D "_sourcedir $PWD" -ba ./warewulf-vnfs.spec
```

## Install the RPMs
```bash
cd ~/rpmbuild/RPMS/
sudo dnf install ./noarch/warewulf-*.rpm ./x86_64/warewulf-*.rpm
```
