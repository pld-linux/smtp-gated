Summary:	Spam/malware transparent SMTP proxy blocker
Summary(pl):	Transparentne proxy SMTP blokuj±ce spam/wirusy
Name:		smtp-gated
Version:	1.4.12
Release:	0.rc3.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://smtp-proxy.klolik.org/%{name}-%{version}-rc3.tar.gz
# Source0-md5:	4cb43aa02307a0c97b46ebd8e63cba8f
Source1:	%{name}.init
URL:		http://smtp-proxy.klolik.org/
BuildRequires:	autoconf
BuildRequires:	automake
#Requires:	kernel(netfilter)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This software block SMTP sessions used by e-mail worms and viruses on
the NA(P)T router. It depends on netfilter framework of Linux.

It acts like proxy, intercepting outgoing SMTP connections and
scanning session data on-the-fly. When messages is infected, the SMTP
session is terminated. It's to be used (mostly) by ISPs, so they can
eliminate infected hosts from their network, and (preferably) educate
their users.

It's similar to clamsmtp and assp.

%description -l pl
To oprogramowanie blokuje sesje SMTP u¿ywane przez robaki i wirusy na
poziomie routerów z NA(P)T. Jest zale¿ne od warstwy netfiltra
linuksowego kernela.

Dzia³a jak proxy, przechwytuj±c wychodz±cy ruch SMTP i skanuj±c dane
w locie. Gdy wiadomo¶æ jest zainfekowana, sesja zostaje przerwana.
Oprogramowanie jest przeznaczone dla ISP, mog± nim wyeliminowaæ
zainfekowane komputery ze swoich sieci.

Pe³ni podobn± funkcjê co clamsmtp i assp.

%prep
%setup -q -n %{name}-%{version}-rc3

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-lang=pl \
	%{?debug:--enable-debugger}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/{rc.d/init.d,sysconfig}}
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name},/var/spool/%{name}/{lock,msg}}
install -d $RPM_BUILD_ROOT/var/run/%{name}

install src/smtp-gated $RPM_BUILD_ROOT%{_sbindir}
install doc/smtp-gated.8 $RPM_BUILD_ROOT%{_mandir}/man8
install doc/smtp-gated.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

install lib/{fixed.conf,local.conf} $RPM_BUILD_ROOT%{_examplesdir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smtp-gated

src/%{name} -t | sed 's/^\([^#]\)/; &/' > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
:> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/%{name} start\" to start smtp-gated server" 1>&2
fi

%preun
if [ "$1" = "0" -a -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} stop
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc/manual*.txt
%attr(640,root,root) %config(noreplace) %verify(not md5,size,mtime) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5,size,mtime) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/smtp-gated
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_examplesdir}/%{name}/*
%attr(750,smtpgw,smtpgw) /var/run/%{name}
%attr(750,smtpgw,smtpgw) /var/spool/%{name}
