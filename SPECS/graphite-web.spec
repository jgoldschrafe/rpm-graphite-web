%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}
%if 0%{?rhel} < 6
%define python_sitelib  %(%{__python} -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib())")
%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")
%define python_version  %(%{__python} -c "import sys; sys.stdout.write(sys.version[:3])")
%endif

Summary:    Enterprise scalable realtime graphing
Name:       graphite-web
Version:    0.9.10
Release:    1%{?dist}
Source:     %{name}-%{version}.tar.gz
Source1:    local_settings.py.default
Source2:    graphite-web.logrotate
Patch0:     %{name}-0.9.10-fhs-compliance.patch
License:    Apache Software License 2.0
Group:      Development/Libraries
Prefix:     %{_prefix}
BuildArch:  noarch
Url:        https://launchpad.net/graphite
Requires:   carbon = %{version}
Requires:   whisper = %{version}
# Django 1.2 required for default local_settings.py to work correctly, but this
# is not a requirement otherwise
Requires:   Django >= 1.2 
Requires:   django-tagging
Requires:   pycairo
Requires:   python-ldap
Requires:   python-memcached
Requires:   python-twisted
Requires:   python-txamqp


%description
Enterprise scalable realtime graphing


%prep
%setup -n %{name}-%{version}
%patch0 -p1
sed -i -e 's|%PYTHON_SITELIB%|%{python_sitelib}|g' \
       -e 's|%DATADIR%|%{_datadir}|g' \
       -e 's|%LOCALSTATEDIR%|%{_localstatedir}|g' \
       -e 's|%SHAREDSTATEDIR%|%{_sharedstatedir}|g' \
       -e 's|%SYSCONFDIR%|%{_sysconfdir}|g' \
           webapp/graphite/settings.py %{SOURCE1}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}

%{__python} setup.py install --root=%{buildroot} --record=INSTALLED_FILES

install -d -m 0755 %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_prefix}/webapp %{buildroot}%{_datadir}/%{name}/webapp

install -d -m 0755 %{buildroot}%{_localstatedir}/log/graphite/webapp
install -d -m 0755 %{buildroot}%{_sharedstatedir}/graphite

install -d -m 0755 %{buildroot}%{_sysconfdir}
mv %{buildroot}%{_prefix}/conf %{buildroot}%{_sysconfdir}/graphite

# Move local_settings.py back under /etc and put a symlink in its place so
# graphite-web can find it
mv %{buildroot}%{python_sitelib}/graphite/local_settings.py.example \
   %{buildroot}%{_sysconfdir}/graphite/local_settings.py.example
ln -sf %{_sysconfdir}/graphite/local_settings.py \
       %{buildroot}%{python_sitelib}/graphite/local_settings.py

# We're done with examples
rm -rf %{buildroot}%{_prefix}/examples

# Install default configurations
cp -a %{buildroot}%{_sysconfdir}/graphite/{dashboard.conf.example,dashboard.conf}
cp -a %{buildroot}%{_sysconfdir}/graphite/{graphite.wsgi.example,graphite.wsgi}
cp -a %{buildroot}%{_sysconfdir}/graphite/{graphTemplates.conf.example,graphTemplates.conf}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/graphite/local_settings.py

# Logrotate fragment
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/graphite-web


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{_sysconfdir}/graphite/*.example
%dir %{_sysconfdir}/graphite
%config(noreplace) %{_sysconfdir}/graphite/*.conf
%config(noreplace) %{_sysconfdir}/graphite/*.py*
%config(noreplace) %{_sysconfdir}/graphite/*.wsgi
%config(noreplace) %{_sysconfdir}/logrotate.d/graphite-web
%{_bindir}/build-index.sh
%{_bindir}/run-graphite-devel-server.py
%{_datadir}/%{name}
%attr(0775,graphite,graphite) %{_sharedstatedir}/graphite
%{python_sitelib}/graphite
%{python_sitelib}/graphite_web-%{version}-py%{pyver}.egg-info
%attr(0755,graphite,graphite) %dir %{_localstatedir}/log/graphite

%changelog
* Tue Jul 10 2012 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.10-1
- Update to 0.9.10
- Added logrotate.d fragment

* Sun Nov  6 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.9-3
- Update dependency list

* Wed Oct 26 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.9-2
- Minor fixes to configuration templates

* Wed Oct 26 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.9-1
- Bump to version 0.9.9

* Wed Oct 26 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.7c-1
- Initial package for Fedora
