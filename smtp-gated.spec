Summary:	Spam/malware transparent SMTP proxy blocker
Summary(pl):	Transparentne proxy SMTP blokuj±ce spam/wirusy
Name:		smtp-gated
Version:	1.4.15.1
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://smtp-proxy.klolik.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	230e34409b194cc1260a8bf42f3e3d94
Source1:	%{name}.init
Source2:	%{name}.conf
URL:		http://smtp-proxy.klolik.org/
BuildRequires:	autoconf
BuildRequires:	automake
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	clamav
#Requires:	kernel(netfilter)
Provides:	user(smtpgw)
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

Dzia³a jak proxy, przechwytuj±c wychodz±cy ruch SMTP i skanuj±c dane w
locie. Gdy wiadomo¶æ jest zainfekowana, sesja zostaje przerwana.
Oprogramowanie jest przeznaczone dla ISP, mog± nim wyeliminowaæ
zainfekowane komputery ze swoich sieci.

Pe³ni podobn± funkcjê co clamsmtp i assp.

%prep
%setup -q

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

install contrib/{fixed.conf,nat.conf} $RPM_BUILD_ROOT%{_examplesdir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smtp-gated
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
:> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 147 -r -d %{_var}/spool/%{name} -s /bin/false -c "SMTP gateway" -g clamav smtpgw

%postun
if [ "$1" = "0" ]; then
	%userremove smtpgw
fi

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Type \"/etc/rc.d/init.d/%{name} start\" to start %{name} server"
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README README.PL
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,clamav) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/smtp-gated
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_examplesdir}/%{name}/*
%attr(750,smtpgw,clamav) /var/run/%{name}
%attr(750,smtpgw,clamav) /var/spool/%{name}
