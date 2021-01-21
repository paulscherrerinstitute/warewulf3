%{!?_rel:%{expand:%%global _rel 0.%(test "9883afc" != "0000" && echo "9883afc" || git show -s --pretty=format:%h || echo 0000)}}
%define debug_package %{nil}
%{!?wwsrvdir:%{expand:%%define wwsrvdir %{_localstatedir}}}

Name: warewulf-provision
Version: 3.9.0
Release: %{_rel}%{?dist}
Summary: Warewulf - System provisioning core
License: US Dept. of Energy (BSD-like) and BSD-3 Clause
URL: http://warewulf.lbl.gov/
Source: %{name}-%{version}.tar.gz
ExclusiveOS: linux
Requires: warewulf-common
Requires: %{name}-initramfs-%{_arch} = %{version}-%{release}
Conflicts: warewulf < 3
BuildRequires: warewulf-common
BuildRequires: libselinux-devel, libacl-devel, libattr-devel
BuildRequires: libuuid-devel, xz-devel
BuildRequires: libtirpc-devel

%if 0%{?rhel:1}
%global httpsvc httpd
%global httpgrp apache
%global tftpsvc tftp-server
%if %{rhel} >= 8
BuildRequires: systemd
BuildRequires: bsdtar
%global dhcpsrv dhcp-server
%else # rhel < 8
%global dhcpsrv dhcp
%endif # rhel 8
%else # sle_version
BuildRequires: systemd-rpm-macros
%global httpsvc apache2
%global httpgrp www
%global tftpsvc tftp
%global dhcpsrv dhcp-server
%endif # rhel

# If multiple architectures are needed, set
# --define="cross_compile 1" as an rpmbuild option
%if 0%{?cross_compile}
%global CROSS_FLAG --enable-cross-compile
%if "%{_arch}" == "x86_64"
BuildRequires: gcc-aarch64-linux-gnu
%endif # x86_64
%if "%{_arch}" == "aarch64"
BuildRequires: gcc-x86_64-linux-gnu
%endif # aarch64
%else
%undefine CROSS_FLAG
%endif # cross_compile

# New RHEL and SLE include the required FS tools
%if 0%{?rhel} >= 8 || 0%{?sle_version} >= 150000
%global localtools 1
BuildRequires: parted, e2fsprogs
Requires: parted, autofs, e2fsprogs
BuildRequires: libarchive.so.13()(64bit)
Requires: libarchive.so.13()(64bit)
%global CONF_FLAGS --with-local-e2fsprogs --with-local-libarchive --with-local-parted --with-local-partprobe
%else
%global localtools 0
Requires: %{name}-gpl_sources = %{version}-%{release}
Provides: parted = 3.2
Provides: e2fsprogs = 1.42.12
Provides: libarchive = 3.3.1
Provides: libarchive.so.13()(64bit)
%endif

%description
Warewulf is an operating system management toolkit designed to facilitate
large scale deployments of systems on physical, virtual and cloud-based
infrastructures. It facilitates elastic and large deployments consisting
of groups of homogenous systems.

Warewulf Provision contains the core components, extensions, and tools to
administrate system provisioning.  To perform provisioning, the
%{name}-server package is also required.


%prep
%setup -q


%build
%configure --localstatedir=%{wwsrvdir} %{?CONF_FLAGS} %{?CROSS_FLAG}
%{__make} %{?mflags}


%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}


%post
if [ $1 -eq 2 ] ; then
  echo "To update software within existing bootstraps run: wwsh bootstrap rebuild"
fi


%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%license COPYING LICENSE
%config(noreplace) %{_sysconfdir}/warewulf/provision.conf
%config(noreplace) %{_sysconfdir}/warewulf/livesync.conf
%config(noreplace) %{_sysconfdir}/warewulf/defaults/provision.conf
%{_sysconfdir}/warewulf/filesystem/examples/*.cmds
%{_mandir}/*
%{perl_vendorlib}/Warewulf/Bootstrap.pm
%{perl_vendorlib}/Warewulf/Provision.pm
%{perl_vendorlib}/Warewulf/Vnfs.pm
%{perl_vendorlib}/Warewulf/DSO/*
%{perl_vendorlib}/Warewulf/Provision
%{perl_vendorlib}/Warewulf/Event/DynamicHosts.pm
%{perl_vendorlib}/Warewulf/Event/Genders.pm
%{perl_vendorlib}/Warewulf/Event/DefaultProvisionNode.pm
%{perl_vendorlib}/Warewulf/Event/ProvisionFileDelete.pm
%{perl_vendorlib}/Warewulf/Module/Cli/Bootstrap.pm
%{perl_vendorlib}/Warewulf/Module/Cli/Provision.pm
%{perl_vendorlib}/Warewulf/Module/Cli/Vnfs.pm


# ====================
%package initramfs-%{_arch}
Summary: Warewulf - initramfs base for %{_arch}
BuildArch: noarch
Requires: warewulf-common

%description initramfs-%{_arch}
Warewulf is an operating system management toolkit designed to facilitate
large scale deployments of systems on physical, virtual and cloud-based
infrastructures. It facilitates elastic and large deployments consisting
of groups of homogenous systems.

This package includes tools and files to create an initramfs
image and to provide boot capability for %{_arch} architecture.

%files initramfs-%{_arch}
%{wwsrvdir}/warewulf/initramfs/%{_arch}


# ====================
%package server
Summary: Warewulf - System provisioning server
Requires: %{name} = %{version}-%{release}
Requires: %{name}-server-ipxe-%{_arch} = %{version}-%{release}
Requires: %{httpsvc}, perl(Apache), %{tftpsvc}, %{dhcpsrv}, tcpdump

%if 0%{?rhel} >= 8
Requires(post): policycoreutils-python-utils
%else # Not RHEL 8+
%if 0%{?sle_version} >= 150100
Requires(post): policycoreutils
%else # Not RHEL 8+ or SLE 15.1+
Requires(post): policycoreutils-python
%endif # sle_version
%endif # rhel

%description server
Warewulf is an operating system management toolkit designed to facilitate
large scale deployments of systems on physical, virtual and cloud-based
infrastructures. It facilitates elastic and large deployments consisting
of groups of homogenous systems.

This package contains the CGI scripts and event components to
provision systems.  Systems used solely for administration of Warewulf
do not require this package.


%post server
# Update users and services on first time installation
if [ $1 -eq 1 ] ; then
usermod -a -G warewulf %{httpgrp} >/dev/null 2>&1 || :
%{__mkdir_p} %{wwsrvdir}/warewulf/ipxe %{wwsrvdir}/warewulf/bootstrap 2>/dev/null || :
%if 0%{?sle_version:1} || 0%{?rhel} >= 8
%systemd_post %{httpdsvc}.service >/dev/null 2>&1 || :
%systemd_post %{tftpsvc}.socket >/dev/null 2>&1 || :
%else
/usr/bin/systemctl --system enable %{httpdsvc}.service &> /dev/null || :
/usr/bin/systemctl --system restart %{httpdsvc}.service  &> /dev/null || :
/usr/bin/systemctl --system enable %{tftpsvc}.socket &> /dev/null || :
/usr/bin/systemctl --system restart %{tftpsvc}.socket  &> /dev/null || :
%endif
fi

# Reset selinux context on any installation or update
/usr/sbin/semanage fcontext -a -t httpd_sys_content_t '%{wwsrvdir}/warewulf/ipxe(/.*)?' 2>/dev/null || :
/usr/sbin/semanage fcontext -a -t httpd_sys_content_t '%{wwsrvdir}/warewulf/bootstrap(/.*)?' 2>/dev/null || :
/sbin/restorecon -R %{wwsrvdir}/warewulf || :


%postun server
# Remove selinux context on package removal. Don't disable web or tftp services.
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_content_t '%{wwsrvdir}/warewulf/ipxe(/.*)?' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_content_t '%{wwsrvdir}/warewulf/bootstrap(/.*)?' 2>/dev/null || :
/sbin/restorecon -R %{wwsrvdir}/warewulf || :
fi
%if 0%{?sle_version:1} || 0%{?rhel} >= 8
%systemd_postun_with_restart %{httpdsvc}.service >/dev/null 2>&1 || :
%systemd_postun_with_restart %{tftpsvc}.socket >/dev/null 2>&1 || :
%else
/usr/bin/systemctl --system restart %{httpdsvc}.service  &> /dev/null || :
/usr/bin/systemctl --system restart %{tftpsvc}.socket  &> /dev/null || :
%endif

%files server
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/warewulf/dhcpd-template.conf
%config(noreplace) %{_sysconfdir}/warewulf/dnsmasq-template.conf
%config(noreplace) %{_sysconfdir}/%{httpsvc}/conf.d/warewulf-httpd.conf
%{_bindir}/*
%attr(0750, root, %{httpgrp}) %{_libexecdir}/warewulf/cgi-bin/
%{perl_vendorlib}/Warewulf/Event/Bootstrap.pm
%{perl_vendorlib}/Warewulf/Event/Dhcp.pm
%{perl_vendorlib}/Warewulf/Event/Pxe.pm
%{perl_vendorlib}/Warewulf/Module/Cli/Pxe.pm
%{perl_vendorlib}/Warewulf/Module/Cli/Dhcp.pm


# ====================
%if "%{_arch}" == "x86_64" || 0%{?CROSS_FLAG:1}
%package server-ipxe-x86_64
Summary: Warewulf - iPXE Bootloader for x86_64
BuildArch: noarch

%description server-ipxe-x86_64
Warewulf is an operating system management toolkit designed to facilitate
large scale deployments of systems on physical, virtual and cloud-based
infrastructures. It facilitates elastic and large deployments consisting
of groups of homogenous systems.

This package provides bundled iPXE binaries for x86_64.

%files server-ipxe-x86_64
%{_datadir}/warewulf/ipxe/bin-i386-efi
%{_datadir}/warewulf/ipxe/bin-i386-pcbios
%{_datadir}/warewulf/ipxe/bin-x86_64-efi
%endif


# ====================
%if "%{_arch}" == "aarch64" || 0%{?CROSS_FLAG:1}
%package server-ipxe-aarch64
Summary: Warewulf - iPXE Bootloader for aarch64
BuildArch: noarch

%description server-ipxe-aarch64
Warewulf is an operating system management toolkit designed to facilitate
large scale deployments of systems on physical, virtual and cloud-based
infrastructures. It facilitates elastic and large deployments consisting
of groups of homogenous systems.

This package provides bundled iPXE binaries for aarch64.

%files server-ipxe-aarch64
%{_datadir}/warewulf/ipxe/bin-arm64-efi
%endif


# ====================
%package gpl_sources
Summary: Warewulf - GPL sources used in Warewulf provisioning
License: GPL+
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description gpl_sources
Warewulf is an operating system management toolkit designed to facilitate
large scale deployments of systems on physical, virtual and cloud-based
infrastructures. It facilitates elastic and large deployments consisting
of groups of homogenous systems.

For user convenience, Warewulf is distributed with some third-party
software.  While Warewulf itself is licensed under a DOE license
(a derivative of the BSD license), the third-party software may have
different licensing terms. To be fully compliant to the GPL open source
license, GPL source files are included in this package.

%files gpl_sources
%defattr(-, root, root)
%{_prefix}/src/warewulf/3rd_party/GPL/


# ====================
%changelog
