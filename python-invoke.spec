# TODO: system six, yaml
# completions (bash, fish, zsh: invoke/completion/*.completion)
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		invoke
%define		egg_name	invoke
%define		pypi_name	invoke
Summary:	Managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks
Summary(pl.UTF-8):	Zarządzanie podprocesami powłoki i organizowanie kodu Pythona w zadania wywoływane z CLI
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.7.3
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/invoke/
Source0:	https://files.pythonhosted.org/packages/source/i/invoke/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	0ce81c61f5dc2d6297a33b3f3c05869c
URL:		https://www.pyinvoke.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-invocations >= 2.4.0
BuildRequires:	python-mock >= 1.0.1
BuildRequires:	python-pytest >= 4.6.3
BuildRequires:	python-pytest-relaxed >= 1.1.5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-invocations >= 2.4.0
BuildRequires:	python3-pytest >= 4.6.3
BuildRequires:	python3-pytest-relaxed >= 1.1.5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-alabaster >= 0.7
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Invoke is a Python task execution tool & library, drawing inspiration
from various sources to arrive at a powerful & clean feature set.

%description -l pl.UTF-8
Invoke to narzędzie i biblioteka do uruchamiania zadań napisanych w
Pythonie, czerpiąca inspiracje z różnych źródeł, dostarczająca duży i
i czysty zbiór możliwości.

%package -n python3-%{module}
Summary:	Managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks
Summary(pl.UTF-8):	Zarządzanie podprocesami powłoki i organizowanie kodu Pythona w zadania wywoływane z CLI
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
Invoke is a Python task execution tool & library, drawing inspiration
from various sources to arrive at a powerful & clean feature set.

%description -n python3-%{module} -l pl.UTF-8
Invoke to narzędzie i biblioteka do uruchamiania zadań napisanych w
Pythonie, czerpiąca inspiracje z różnych źródeł, dostarczająca duży i
i czysty zbiór możliwości.

%package apidocs
Summary:	API documentation for Python invoke module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona invoke
Group:		Documentation

%description apidocs
API documentation for Python invoke module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona invoke.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} tasks.py test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} tasks.py test
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html sites/docs sites/docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/invoke/vendor/yaml3
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/invoke/vendor/yaml2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/inv
%attr(755,root,root) %{_bindir}/invoke
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc sites/docs/_build/html/{_static,api,concepts,*.html,*.js}
%endif
