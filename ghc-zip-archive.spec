#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	zip-archive
Summary:	Library for creating and modifying zip archives
Summary(pl.UTF-8):	Biblioteka do tworzenia i modyfikowania archiwów zip
Name:		ghc-%{pkgname}
Version:	0.4.1
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/zip-archive
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	622fb5b050d4d05771f29d409e0c7f6b
URL:		http://hackage.haskell.org/package/zip-archive
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 4.2
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-binary >= 0.6
BuildRequires:	ghc-bytestring >= 0.10.0
BuildRequires:	ghc-containers
BuildRequires:	ghc-digest >= 0.0.0.1
BuildRequires:	ghc-directory >= 1.2
BuildRequires:	ghc-filepath
BuildRequires:	ghc-mtl
BuildRequires:	ghc-pretty
BuildRequires:	ghc-text >= 0.11
BuildRequires:	ghc-time
BuildRequires:	ghc-zlib
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 4.2
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-binary-prof >= 0.6
BuildRequires:	ghc-bytestring-prof >= 0.10.0
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-digest-prof >= 0.0.0.1
BuildRequires:	ghc-directory-prof >= 1.2
BuildRequires:	ghc-filepath-prof
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-pretty-prof
BuildRequires:	ghc-text-prof >= 0.11
BuildRequires:	ghc-time-prof
BuildRequires:	ghc-zlib-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 4.2
Requires:	ghc-base < 5
Requires:	ghc-binary >= 0.6
Requires:	ghc-bytestring >= 0.10.0
Requires:	ghc-containers
Requires:	ghc-digest >= 0.0.0.1
Requires:	ghc-directory >= 1.2
Requires:	ghc-filepath
Requires:	ghc-mtl
Requires:	ghc-pretty
Requires:	ghc-text >= 0.11
Requires:	ghc-time
Requires:	ghc-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The zip-archive library provides functions for creating, modifying,
and extracting files from zip archives.

%description -l pl.UTF-8
Biblioteka zip-archive udostępnia funkcje do tworzenia, modyfikowania
oraz wydobywania plików z archiwów zip.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 4.2
Requires:	ghc-base-prof < 5
Requires:	ghc-binary-prof >= 0.6
Requires:	ghc-bytestring-prof >= 0.10.0
Requires:	ghc-containers-prof
Requires:	ghc-digest-prof >= 0.0.0.1
Requires:	ghc-directory-prof >= 1.2
Requires:	ghc-filepath-prof
Requires:	ghc-mtl-prof
Requires:	ghc-pretty-prof
Requires:	ghc-text-prof >= 0.11
Requires:	ghc-time-prof
Requires:	ghc-zlib-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzip-archive-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzip-archive-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzip-archive-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Archive
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Archive/Zip.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Archive/Zip.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzip-archive-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Archive/Zip.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
