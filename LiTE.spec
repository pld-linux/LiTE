#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	LiTE is a Toolkit Engine
Summary(pl.UTF-8):	LiTE - silnik toolkitu
Name:		LiTE
Version:	0.8.10
Release:	9
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.directfb.org/downloads/Libs/%{name}-%{version}.tar.gz
# Source0-md5:	b9a28007d38c2b1c51ba1c3841df29ad
Patch0:		%{name}-stat.patch
URL:		http://www.directfb.org/index.php?path=Platform/LiTE
BuildRequires:	DirectFB-devel >= 1:1.0.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	t1utils
Requires(post,postun):	/sbin/ldconfig
Requires:	%{_fontsdir}/TTF
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LiTE is a Toolkit Engine.

%description -l pl.UTF-8
LiTE - silnik toolkitu.

%package devel
Summary:	LiTE header files
Summary(pl.UTF-8):	Pliki nagłówkowe LiTE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	DirectFB-devel >= 1:1.0.0

%description devel
Header files for LiTE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LiTE.

%package static
Summary:	LiTE static library
Summary(pl.UTF-8):	Statyczna biblioteka LiTE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
LiTE static library.

%description static -l pl.UTF-8
Statyczna biblioteka LiTE.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static \
	--with-fontdir=%{_fontsdir}/TTF \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_fontsdir}/Type1
t1binary $RPM_BUILD_ROOT%{_fontsdir}/TTF/Misc-Fixed.pfa \
	$RPM_BUILD_ROOT%{_fontsdir}/Type1/Misc-Fixed.pfb
cat > $RPM_BUILD_ROOT%{_fontsdir}/Type1/fonts.scale.LiTE <<EOF
Misc-Fixed.pfb -misc-fixed-medium-r-normal--0-0-0-0-m-0-ascii-0
Misc-Fixed.pfb -misc-fixed-medium-r-normal--0-0-0-0-m-0-iso10646-1
Misc-Fixed.pfb -misc-fixed-medium-r-normal--0-0-0-0-m-0-iso8859-1
EOF
rm -f $RPM_BUILD_ROOT%{_fontsdir}/TTF/Misc-Fixed.pfa

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ -x /usr/bin/fontpostinst ]; then
	fontpostinst TTF
	fontpostinst Type1
fi

%postun
/sbin/ldconfig
if [ -x /usr/bin/fontpostinst ]; then
	fontpostinst TTF
	fontpostinst Type1
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/lite_*
%attr(755,root,root) %{_libdir}/libleck.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libleck.so.3
%attr(755,root,root) %{_libdir}/liblite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblite.so.3
%{_datadir}/LiTE
%{_fontsdir}/TTF/decker.ttf
%{_fontsdir}/TTF/vera*.ttf
%{_fontsdir}/TTF/whiterabbit.ttf
%{_fontsdir}/Type1/Misc-Fixed.pfb
%{_fontsdir}/Type1/fonts.scale.LiTE

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libleck.so
%attr(755,root,root) %{_libdir}/liblite.so
%{_libdir}/libleck.la
%{_libdir}/liblite.la
%{_includedir}/leck
%{_includedir}/lite
%{_pkgconfigdir}/leck.pc
%{_pkgconfigdir}/lite.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libleck.a
%{_libdir}/liblite.a
%endif
