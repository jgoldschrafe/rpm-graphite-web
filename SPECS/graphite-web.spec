%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary:    Enterprise scalable realtime graphing
Name:       graphite-web
Version:    0.9.9
Release:    1%{?dist}
Source:     %{name}-%{version}.tar.gz
Patch0:     %{name}-0.9.9-fhs-compliance.patch
License:    Apache Software License 2.0
Group:      Development/Libraries
Prefix:     %{_prefix}
BuildArch:  noarch
Url:        https://launchpad.net/graphite
Requires:   python-carbon = %{version}
Requires:   python-whisper = %{version}
Requires:   Django
Requires:   django-tagging
Requires:   pycairo
Requires:   python-ldap
Requires:   python-memcached
Requires:   python-twisted
Requires:   python-txamqp

%description
UNKNOWN

%prep
%setup -n %{name}-%{version}
%patch0 -p1
sed -i -e 's|%PYTHON_SITELIB%|%{python_sitelib}|g' webapp/graphite/settings.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_prefix}/webapp $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/log/graphite/webapp

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/graphite
mv $RPM_BUILD_ROOT%{python_sitelib}/graphite/local_settings.py.example \
   $RPM_BUILD_ROOT%{_sysconfdir}/graphite/local_settings.py.example

mv $RPM_BUILD_ROOT%{_prefix}/conf/*.example \
   $RPM_BUILD_ROOT%{_sysconfdir}/graphite/
rmdir $RPM_BUILD_ROOT/%{_prefix}/conf

ln -sf %{_sysconfdir}/graphite/local_settings.py \
       $RPM_BUILD_ROOT%{python_sitelib}/graphite/local_settings.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/graphite
%{_sysconfdir}/graphite/dashboard.conf.example
%{_sysconfdir}/graphite/graphTemplates.conf.example
%{_sysconfdir}/graphite/graphite.wsgi.example
%{_sysconfdir}/graphite/local_settings.py.example
%{_bindir}/build-index.sh
%{_bindir}/run-graphite-devel-server.py
%{_datadir}/%{name}
%{python_sitelib}/graphite
%{python_sitelib}/graphite_web-%{version}-py%{pyver}.egg-info
%attr(0755,graphite,graphite) %dir %{_localstatedir}/log/graphite
%attr(0755,graphite,graphite) %dir %{_localstatedir}/log/graphite/webapp

%changelog
* Wed Oct 26 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.9-1
- Bump to version 0.9.9

* Wed Oct 26 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.9.7c-1
- Initial package for Fedora
