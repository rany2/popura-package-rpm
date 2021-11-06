Name:           popura
Version:        0.4.2+popura1
Release:        1%{?dist}
Summary:        Popura ポプラ: alternative Yggdrasil network client

License:        GPLv3
URL:            https://popura-network.github.io
Source:         https://codeload.github.com/popura-network/Popura/tar.gz/v%{version}

%{?systemd_requires}
BuildRequires:  systemd golang >= 1.13 git
Requires(pre):  shadow-utils
Conflicts:      popura-develop yggdrasil yggdrasil-develop

%description
Popura uses the same Yggdrasil core API internally, but adds some useful and
experimental features which the original client lacks.

%define debug_package %{nil}

%pre
getent group yggdrasil >dev/null || groupadd -r yggdrasil
exit 0

%prep
%setup -qn Popura-%(echo %{version} | sed -e 's/+/-/g')

%build
export PKGNAME="%{name}"
export PKGVER="%{version}"
export GOPROXY="https://proxy.golang.org,direct"
./build -t -l "-linkmode=external"

%install
rm -rf %{buildroot}
install -m 0755 -D yggdrasil %{buildroot}/%{_bindir}/yggdrasil
install -m 0755 -D yggdrasilctl %{buildroot}/%{_bindir}/yggdrasilctl
install -m 0644 -D contrib/systemd/yggdrasil.service %{buildroot}/%{_sysconfdir}/systemd/system/yggdrasil.service
install -m 0644 -D contrib/systemd/yggdrasil-default-config.service %{buildroot}/%{_sysconfdir}/systemd/system/yggdrasil-default-config.service

%files
%{_bindir}/yggdrasil
%{_bindir}/yggdrasilctl
%{_sysconfdir}/systemd/system/yggdrasil.service
%{_sysconfdir}/systemd/system/yggdrasil-default-config.service

%post
%systemd_post yggdrasil.service

%preun
%systemd_preun yggdrasil.service

%postun
%systemd_postun_with_restart yggdrasil.service
