Summary:	Smtp-gated is a spam/malware transparent SMTP blocker
Summary(pl):	smtp-gated blokuje spam/wirusya u¿ywaj±c transparentego SMTP
Name:		smtp-gated
Version:	1.4.11
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://smtp-proxy.klolik.org/%{name}-%{version}.tar.gz
# Source0-md5:	ebac2d141ba2ba953fa43211c7905ebc
#Source1:	%{name}.inetd
#Prereq:		rc-inetd >= 0.8.1
URL:		http://smtp-proxy.klolik.org
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	clamsmtp
Requires:	kernel(netfilter)

%description

This software block SMTP sessions used by e-mail worms and viruses on
the NA(P)T router. It depends on netfilter framework of Linux.

It acts like proxy, intercepting outgoing SMTP connections and
scanning session data on-the-fly. When messages is infected, the SMTP
session is terminated. It's to be used (mostly) by ISPs, so they can
eliminate infected hosts from their network, and (preferably) educate
their users.


%description -l pl
To oprogramowanie blokuje sesje smtp u¿ywane przez robaki i wirusy na
poziomie routerów z NA(P)T. Jest zale¿ne od warstwy netfiltra
linuksowego kernela.

Dzia³a jak proxy, przechwytuj±c wychodz±cy ruch SMTP i skanuj±c dane
w-locie. Gdy wiadomo¶æ jest zainfekowana, sesja zostaje przerwana.
Oprogramowanie jest przeznaczone dla ISP, mog± nim wyeliminowaæ
zainfekowane komputery ze swoich sieci.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/sysconfig/rc-inetd,%{_examplesdir}/%{name}}

install src/smtp-gated $RPM_BUILD_ROOT%{_sbindir}
install lib/manual.8  $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8
install lib/manual.conf.5  $RPM_BUILD_ROOT%{_mandir}/man5/%{name}.5

install lib/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

#install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/smtpproxy

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README
#%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/%{name}
%attr(755,root,root) %{_sbindir}/smtp-gated
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_examplesdir}/%{name}/*
