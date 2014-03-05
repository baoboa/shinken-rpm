%global with_systemd 0%{?fedora} >= 17
%global shinken_user nagios
%global shinken_group nagios

Summary:        Python Monitoring tool
Name:           shinken
Version:        2.0 
Release:        rc2%{?dist}
URL:            http://www.%{name}-monitoring.org
Source0:        http://www.%{name}-monitoring.org/pub/%{name}-%{version}.tar.gz
License:        AGPLv3+
Requires:       python 
Requires:       python-simplejson 
Requires:       python-pycurl  
Requires:       python-cherrypy 
%if %{with_systemd}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif
Requires:       nmap 
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if %{with_systemd}
BuildRequires:  systemd-units
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
Buildarch:      noarch

%description 
Shinken is a new monitoring tool written in Python. 
The main goal of Shinken is to allow users to have a fully flexible 
architecture for their monitoring system that can easily scale to large 
environments.
Shinken also provide interfaces with NDODB and Merlin database, 
Livestatus connector Shinken does not include any human interfaces.

%package arbiter
Summary: Shinken Arbiter 
Requires: %{name} = %{version}-%{release}

%description arbiter
Shinken arbiter daemon

%package reactionner
Summary: Shinken Reactionner
Requires: %{name} = %{version}-%{release}

%description reactionner
Shinken reactionner daemon

%package scheduler
Summary: Shinken Scheduler
Requires: %{name} = %{version}-%{release}

%description scheduler
Shinken scheduler daemon

%package poller
Summary: Shinken Poller
Requires: %{name} = %{version}-%{release}
Requires: nagios-plugins-all

%description poller
Shinken poller daemon

%package broker
Summary: Shinken Broker
Requires: %{name} = %{version}-%{release}
Requires: mysql-connector-python
Requires: python-redis
Requires: python-memcached

%description broker
Shinken broker daemon

%package receiver
Summary: Shinken Poller
Requires: %{name} = %{version}-%{release}

%description receiver
Shinken receiver daemon

%prep

%setup -q


# clean git files/
find . -name '.gitignore' -exec rm -f {} \;

# Check confuguration files 
sed -i -e 's!./$SCRIPT!python ./$SCRIPT!' test/quick_tests.sh
sed -i -e 's!include var/void_for_git!exclude var/void_for_git!'  MANIFEST.in

%build

%{__python} setup.py build 

%install

find %{buildroot} -size 0 -delete

%{__python} setuppackage.py install -O1 --root=%{buildroot} --install-scripts=/usr/sbin/ --owner=nagios --group=nagios

install -d -m0755 %{buildroot}%{_sbindir}
install -p -m0755 bin/shinken-{arbiter,admin,discovery,broker,poller,reactionner,receiver,scheduler} %{buildroot}%{_sbindir}

install -d -m0755 %{buildroot}%{python2_sitelib}/%{name}
install -p %{name}/*.py %{buildroot}%{python2_sitelib}/%{name}
#cp -rf %{name}/{clients,core,misc,modules,objects,plugins,webui} %{buildroot}%{python2_sitelib}/%{name}

install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/
rm -rf %{buildroot}%{_sysconfdir}/%{name}/*

install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/objects
install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/objects/{contacts,discovery,hosts,services}

#install -p -m0644 for_fedora/etc/objects/contacts/nagiosadmin.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/contacts/nagiosadmin.cfg
#install -p -m0644 for_fedora/etc/objects/hosts/localhost.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/hosts/localhost.cfg
#install -p -m0644 for_fedora/etc/objects/services/linux_disks.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/services/linux_disks.cfg
#install -p -m0644 for_fedora/etc/htpasswd.users %{buildroot}%{_sysconfdir}/%{name}/htpasswd.users
#install -p -m0644 for_fedora/etc/%{name}-specific.cfg %{buildroot}%{_sysconfdir}/%{name}/
#install -p -m0644 for_fedora/etc/discovery*.cfg %{buildroot}%{_sysconfdir}/%{name}/
#install -p -m0644 for_fedora/etc/{contactgroups,nagios,timeperiods,%{name}-specific,escalations,servicegroups,resource,templates}.cfg %{buildroot}%{_sysconfdir}/%{name}/
#install -p -m0644 for_fedora/etc/{brokerd,pollerd,reactionnerd,receiverd,schedulerd}.ini %{buildroot}%{_sysconfdir}/%{name}/


%if %{with_systemd}
  install -d -m0755 %{buildroot}%{_unitdir}
  install -p -m0644 for_fedora/systemd/%{name}-arbiter.service %{buildroot}%{_unitdir}/%{name}-arbiter.service
  install -p -m0644 for_fedora/systemd/%{name}-broker.service %{buildroot}%{_unitdir}/%{name}-broker.service
  install -p -m0644 for_fedora/systemd/%{name}-reactionner.service %{buildroot}%{_unitdir}/%{name}-reactionner.service
  install -p -m0644 for_fedora/systemd/%{name}-scheduler.service %{buildroot}%{_unitdir}/%{name}-scheduler.service
  install -p -m0644 for_fedora/systemd/%{name}-receiver.service %{buildroot}%{_unitdir}/%{name}-receiver.service
  install -p -m0644 for_fedora/systemd/%{name}-poller.service %{buildroot}%{_unitdir}/%{name}-poller.service
%else
  install -d -m0755 %{buildroot}%{_initrddir}
  install -p -m0644 for_fedora/init.d/%{name}-arbiter %{buildroot}%{_initrddir}/%{name}-arbiter
  install -p -m0644 for_fedora/init.d/%{name}-scheduler %{buildroot}%{_initrddir}/%{name}-scheduler
  install -p -m0644 for_fedora/init.d/%{name}-poller %{buildroot}%{_initrddir}/%{name}-poller
  install -p -m0644 for_fedora/init.d/%{name}-broker %{buildroot}%{_initrddir}/%{name}-broker
  install -p -m0644 for_fedora/init.d/%{name}-reactionner %{buildroot}%{_initrddir}/%{name}-reactionner
  install -p -m0644 for_fedora/init.d/%{name}-receiver %{buildroot}%{_initrddir}/%{name}-receiver
%endif

install -d -m0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m0644 for_fedora/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/shinken

install -d -m0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m0644  for_fedora/%{name}-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}/archives
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}

mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m0755 %{buildroot}%{_localstatedir}/run/%{name}

#install -d -m0755 %{buildroot}%{_mandir}/man3
#install -p -m0644 doc/man/* %{buildroot}%{_mandir}/man3

#install -d -m0755 %{buildroot}%{_usr}/lib/%{name}/plugins/discovery
#install  -m0755 libexec/*.py %{buildroot}%{_usr}/lib/%{name}/plugins
#install  -m0644 libexec/*.ini %{buildroot}%{_usr}/lib/%{name}/plugins
#install  -m0755 libexec/discovery/*.py %{buildroot}%{_usr}/lib/%{name}/plugins/discovery


#for lib in %{buildroot}%{python_sitearch}/%{name}/*.py; do
# sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
# touch -r $lib $lib.new &&
# mv $lib.new $lib
#done

#for Files in %{buildroot}%{python2_sitelib}/%{name}/__init__.py %{buildroot}%{python2_sitelib}/%{name}/core/__init__.py %{buildroot}%{python2_sitelib}/%{name}/daemons/*.py %{buildroot}%{python2_sitelib}/%{name}/modules/{openldap_ui.py,nrpe_poller.py,livestatus_broker/livestatus_query_cache.py} ; do
#  %{__sed} -i.orig -e 1d ${Files}
#  touch -r ${Files}.orig ${Files}
#  %{__rm} ${Files}.orig
#done

#sed -i -e 's!/usr/local/shinken/libexec!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
#sed -i -e 's!/usr/lib/nagios/plugins!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
#sed -i -e 's!/usr/local/shinken/var/arbiterd.pid!/var/run/shinken/arbiterd.pid!' %{buildroot}%{_sysconfdir}/%{name}/nagios.cfg
#sed -i -e 's!command_file=/usr/local/shinken/var/rw/nagios.cmd!command_file=/var/log/shinken/nagios.cmd!' %{buildroot}%{_sysconfdir}/%{name}/nagios.cfg
#sed -i -e 's!cfg_file=hostgroups.cfg!!' %{buildroot}%{_sysconfdir}/%{name}/nagios.cfg
#sed -i -e 's!,Windows_administrator!!' %{buildroot}%{_sysconfdir}/%{name}/contactgroups.cfg
#sed -i -e 's!/usr/local/shinken/src/!/usr/sbin/!' FROM_NAGIOS_TO_SHINKEN
#sed -i -e 's!/usr/local/nagios/etc/!/etc/shinken/!' FROM_NAGIOS_TO_SHINKEN
#sed -i -e 's!/usr/local/shinken/src/etc/!/etc/shinken/!' FROM_NAGIOS_TO_SHINKEN
#sed -i -e 's!(you can also be even more lazy and call the bin/launch_all.sh script).!!' FROM_NAGIOS_TO_SHINKEN

rm -rf %{buildroot}%{_localstatedir}/{log,run,lib}/%{name}/void_for_git
rm %{buildroot}%{_sysconfdir}/default/shinken
rm -rf %{buildroot}%{_sysconfdir}/init.d/shinken*
rm -rf %{buildroot}%{_usr}/lib/%{name}/plugins/*.{pyc,pyo}
rm -rf %{buildroot}%{_sbindir}/shinken-{arbiter,discovery,broker,poller,reactionner,receiver,scheduler}.py

#find  %{buildroot}%{python2_sitelib}/%{name} -type f | xargs sed -i 's|#!/usr/bin/python||g' 
#sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python2_sitelib}/%{name}/webui/plugins/mobile/mobile.py

rm -rf  %{buildroot}%{python2_sitelib}/modules

find %{buildroot} -maxdepth 5 -name '*.pyc' -exec rm -f {} \;
find %{buildroot} -maxdepth 5 -name '*.pyo' -exec rm -f {} \;


%clean

%pre 
getent group %{shinken_group} >/dev/null || groupadd -r %{shinken_group}
getent passwd %{shinken_user} >/dev/null || useradd -r -g %{shinken_group} -d %{_localstatedir}/spool/nagios -s /sbin/nologin %{shinken_user}
exit 0

%post arbiter
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-arbiter || :
  %endif
fi

%post broker
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-broker || :
%endif
fi

%post poller
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-poller || :
  %endif
fi

%post reactionner
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-reactionner || :
%endif
fi

%post scheduler
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-scheduler || :
  %endif
fi

%post receiver
if [ $1 -eq 1 ] ; then 
  %if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}-receiver || :
  %endif
fi

%preun arbiter 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-arbiter.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-arbiter.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-arbiter stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-arbiter || :
  %endif
fi

%preun broker 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-broker.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-broker.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-broker stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-broker || :
  %endif
fi

%preun poller 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-poller.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-poller.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-poller stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-poller || :
  %endif
fi

%preun reactionner 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-reactionner.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-reactionner.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-reactionner stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-reactionner || :
  %endif
fi

%preun scheduler 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-scheduler.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-scheduler.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-scheduler stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-scheduler || :
  %endif
fi

%preun receiver 
if [ $1 -eq 0 ] ; then
  %if %{with_systemd}
    /bin/systemctl --no-reload disable %{name}-receiver.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}-receiver.service > /dev/null 2>&1 || :
  %else
    /sbin/service %{name}-receiver stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-receiver || :
  %endif
fi

%postun arbiter
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-arbiter.service >/dev/null 2>&1 || :
  fi
%endif

%postun broker
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-broker.service >/dev/null 2>&1 || :
  fi
%endif

%postun poller
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-poller.service >/dev/null 2>&1 || :
  fi
%endif

%postun reactionner
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-reactionner.service >/dev/null 2>&1 || :
  fi
%endif

%postun scheduler
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-scheduler.service >/dev/null 2>&1 || :
  fi
%endif

%postun receiver
%if %{with_systemd}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart %{name}-receiver.service >/dev/null 2>&1 || :
  fi
%endif

%files arbiter
%if %{with_systemd}
  %{_unitdir}/%{name}-arbiter.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-arbiter
%endif
%{_sbindir}/%{name}-arbiter*
#%{_mandir}/man3/%{name}-arbiter*

%files reactionner
%if %{with_systemd}
  %{_unitdir}/%{name}-reactionner.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-reactionner
%endif
%{_sbindir}/%{name}-reactionner*
#%{_mandir}/man3/%{name}-reactionner*

%files scheduler
%if %{with_systemd}
  %{_unitdir}/%{name}-scheduler.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-scheduler
%endif
%{_sbindir}/%{name}-scheduler*
#%{_mandir}/man3/%{name}-scheduler*

%files poller
%if %{with_systemd}
  %{_unitdir}/%{name}-poller.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-poller
%endif
%{_sbindir}/%{name}-poller*
#%{_mandir}/man3/%{name}-poller*

%files broker
%if %{with_systemd}
  %{_unitdir}/%{name}-broker.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-broker
%endif
%{_sbindir}/%{name}-broker*
#%{_mandir}/man3/%{name}-broker*

%files receiver
%if %{with_systemd}
  %{_unitdir}/%{name}-receiver.service
%else
  %attr(0755,root,root) %{_initrddir}/%{name}-receiver
%endif
%{_sbindir}/%{name}-receiver*
#%{_mandir}/man3/%{name}-receiver*

%files
%{python2_sitelib}/%{name}
%if %{with_systemd}
#%{python2_sitelib}/Shinken-1.4-py2.7.egg-info
%{python2_sitelib}/Shinken-2*.egg-info
%else
#%{python2_sitelib}/Shinken-1.4-py2.6.egg-info
%{python2_sitelib}/Shinken-2*.egg-info
%endif
%{_sbindir}/%{name}-receiver*
%{_sbindir}/%{name}-discovery
%{_sbindir}/%{name}-admin
#%{_sbindir}/%{name}-hostd
#%{_sbindir}/%{name}-packs
%{_sbindir}/%{name}
#%{_usr}/lib/%{name}/plugins
%doc etc/packs COPYING THANKS 
#%{_mandir}/man3/%{name}-*
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %{_localstatedir}/lib/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/run/%{name}

%changelog
* Wed Mar 05 2014 baoboa <baoboa@gmail.com> - 2.0-1
- Update from upstream.
- change setup.py to setuppackage.py and minor corrections 

* Mon Aug 19 2013 David Hannequin <david.hannequin@gmail.com> - 2.0-1
- Update from upstream.
- Add requires. 

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 27 2013 David Hannequin <david.hannequin@gmail.com> - 1.4-1
- Update from upstream.

* Mon Mar 11 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-6
- Fix broker summary.

* Sat Mar 9 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-5
- Add Webui menu patch.

* Wed Mar 6 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-2
- Fix discovery rules.

* Sun Feb 24 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-1
- Update from upstream.

* Wed Jan 30 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.3-1
- Update from upstream.

* Sat Dec 15 2012 David Hannequin <david.hannequin@gmail.com> - 1.2.2-1
- Update from upstream,
- Delete eue module,
- Fix web site url, 
- Fix Bug 874092 (thanks Sébastien Andreatta).

* Fri Dec 14 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-7
- Fix uninstall receiver.  

* Mon Nov 5 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-6
- Fix bug 874089.  

* Sun Sep 16 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-5
- Add support of el6,
- Remove shebang from Python libraries,
- Delete echo printing,
- Remove CFLAGS.

* Mon Sep 10 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-4
- Add COPYING README THANKS file,
- delete defattr.

* Sun Sep 09 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-3
- Delete require python-sqlite2.

* Sun Jul 22 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-2
- Add build patch. 

* Tue Mar 13 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-1
- Update from upstream,
- Add shinken packs

* Mon Oct 24 2011 David Hannequin <david.hannequin@gmail.com> - 0.8.1-1
- Update from upstream,
- Add manpage, 
- Add require nagios plugins.  

* Mon May 30 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.5-1
- Update from upstream,
- Add require python-redis, 
- Add require python-memcached.

* Mon May 30 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-3
- Fix path in default shinken file,
- Fix path in setup.cfg, 
- Add file FROM_NAGIOS_TO_SHINKEN.

* Sun May 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-2
- Fix shinken configuration,
- Replace macro,
- Update from upstreamr.

* Fri May 20 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-1
- Update from upstream. 

* Fri Apr 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6-1
- Fisrt release for fedora.
