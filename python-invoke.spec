# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		invoke
%define		egg_name	invoke
%define		pypi_name	invoke
Summary:	Managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks
Name:		python-%{module}
Version:	1.3.0
Release:	4
License:	BSD
Group:		Libraries/Python
# if pypi:
Source0:	https://pypi.debian.net/invoke/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	4404e8aa4e3f5c5b511f79e428f17dc9
URL:		https://www.pyinvoke.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Invoke is a Python task execution tool & library, drawing inspiration
from various sources to arrive at a powerful & clean feature set.

%package -n python3-%{module}
Summary:	Managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Invoke is a Python task execution tool & library, drawing inspiration
from various sources to arrive at a powerful & clean feature set.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/inv
%attr(755,root,root) %{_bindir}/invoke
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
