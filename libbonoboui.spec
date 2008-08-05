# enable_gtkdoc: toggle if gtk-doc stuff should be rebuilt.
#	0 = no
#	1 = yes
%define enable_gtkdoc	1

# End of user configurable section
%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}

%define req_bonobo_activation_version	0.9.3
%define req_libbonobo_version			2.13.0
%define req_libgnomecanvas_version		1.116.0
%define req_libgnome_version			2.13.0
%define req_libglade_version			2.0.0
%define req_gtk_version					2.2.0

%define api_version	2
%define lib_major	0
%define lib_name	%mklibname bonoboui %{api_version} %{lib_major}
%define develname %mklibname -d bonoboui %{api_version}

# define to use Xvfb
%define build_xvfb 1

# Allow --with[out] <feature> at rpm command line build
%{?_without_XVFB: %{expand: %%define build_xvfb 0}}
%{?_with_XVFB: %{expand: %%define build_xvfb 1}}


Name:		libbonoboui
Summary:	Library for compound documents in GNOME
Version: 	2.23.5
Release:	%mkrel 1
License:	GPLv2+ and LGPLv2+
URL:		http://www.gnome.org/
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:	libgnomecanvas2-devel >= %{req_libgnomecanvas_version}
BuildRequires:	libgnome2-devel >= %{req_libgnome_version}
BuildRequires:	libbonobo2_x-devel >= %{req_libbonobo_version}
BuildRequires:  libglade2.0-devel >= %{req_libglade_version}
BuildRequires:  gtk+2-devel >= %{req_gtk_version}
BuildRequires:	perl-XML-Parser
BuildRequires:  automake1.8
BuildRequires:	intltool
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
%if %{build_xvfb}
%if %mdkversion <= 200600
BuildRequires:  XFree86-Xvfb
%else
BuildRequires:  x11-server-xvfb
%endif
%endif

Requires:	%{lib_name} = %{version}
Requires:   gtk+2.0 >= %{req_gtk_version}

%description
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package contains various needed modules and files for bonobo 2
to operate.


%package -n %{lib_name}
Summary:	Library for compound documents in GNOME
Group:		%{group}
Provides:	%{name}%{api_version} = %{version}-%{release}
Requires:	%{name} >= %{version}
Requires:	libbonobo-activation >= %{req_bonobo_activation_version}

%description -n %{lib_name}
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides libraries to use Bonobo.


%package -n %develname
Summary:	Static libraries, include files and sample code for Bonobo 2
Group:		Development/GNOME and GTK+
Provides:	%{name}%{api_version}-devel = %{version}-%{release}
Provides:	bonoboui-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}
Requires:	%{name} = %{version}
Requires:	libgnomecanvas2-devel >= %{req_libgnomecanvas_version}
Requires:	libgnome2-devel >= %{req_libgnome_version}
Requires:	libbonobo2_x-devel >= %{req_libbonobo_version}
Requires:	gtk+2-devel >= %{req_gtk_version}
Obsoletes: %mklibname -d bonoboui 2 0

%description -n %develname
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides the necessary development libraries and include
files to allow you to develop programs using the Bonobo document model;
it includes demonstration executables and codes as well.


%prep
%setup -q

%build

%configure2_5x \
%if %enable_gtkdoc
--enable-gtk-doc
%endif

%make

%check
%if %{build_xvfb}
XDISPLAY=$(i=0; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
Xvfb :$XDISPLAY >& /dev/null &
DISPLAY=:$XDISPLAY make check
kill $(cat /tmp/.X$XDISPLAY-lock)
%else
make check
%endif

%install
rm -rf %{buildroot}
%makeinstall_std

%{find_lang} %{name}-2.0

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.{la,a}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
  
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc README NEWS changes.txt
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo-2.0
%{_libdir}/libglade/2.0/*.so
%{_datadir}/gnome-2.0
%{_datadir}/applications/bonobo-browser.desktop

%files -n %{lib_name}
%defattr(-, root, root)
%doc README NEWS
%{_libdir}/libbonoboui-%{api_version}.so.%{lib_major}*

%files -n %develname
%defattr(-, root, root)
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libbonobo*.so
%{_libdir}/libbonobo*.a
%attr(644,root,root) %{_libdir}/libbonobo*.la
%{_libdir}/pkgconfig/*


