Summary:	LiTE is a Toolkit Engine
Summary(pl):	LiTE - silnik toolkitu
Name:		LiTE
Version:	0.6.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.directfb.org/downloads/Libs/%{name}-%{version}.tar.gz
# Source0-md5:	dfdf700c6aafb81499132ecf1229d569
URL:		http://www.directfb.org/
BuildRequires:	DirectFB-devel >= 1:0.9.23
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires(post,postun):	/sbin/ldconfig
Requires:	%{_fontsdir}/TTF
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LiTE is a Toolkit Engine.

%description -l pl
LiTE - silnik toolkitu.

%package devel
Summary:	LiTE header files
Summary(pl):	Pliki nag³ówkowe LiTE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	DirectFB-devel >= 1:0.9.23

%description devel
Header files for LiTE library.

%description devel -l pl
Pliki nag³ówkowe biblioteki LiTE.

%package static
Summary:	LiTE static library
Summary(pl):	Statyczna biblioteka LiTE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
LiTE static library.

%description static -l pl
Statyczna biblioteka LiTE.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static \
	--with-fontdir=%{_fontsdir}/TTF
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/bin/fontpostinst ] || fontpostinst TTF

%postun
/sbin/ldconfig
[ ! -x /usr/bin/fontpostinst ] || fontpostinst TTF

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/dfbspy
%attr(755,root,root) %{_bindir}/literun
%attr(755,root,root) %{_libdir}/liblite.so.*.*.*
%{_datadir}/LiTE
%{_fontsdir}/TTF/*.ttf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblite.so
%{_libdir}/liblite.la
%{_includedir}/lite
%{_pkgconfigdir}/lite.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/liblite.a
