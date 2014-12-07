%define url_ver %(echo %{version}|cut -d. -f1,2)

%define build_xvfb 1
%define enable_gtkdoc	1
%define api	2
%define major	0
%define libname	%mklibname bonoboui %{api} %{major}
%define devname	%mklibname -d bonoboui

Summary:	Library for compound documents in GNOME
Name:		libbonoboui
Version:	2.24.5
Release:	16
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/libbonoboui/%{url_ver}/%{name}-%{version}.tar.bz2

%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig(bonobo-activation-2.0) >= 2.13.0
BuildRequires:	pkgconfig(gdk-x11-2.0) >= 2.2.0
BuildRequires:	pkgconfig(libbonobo-2.0) >= 2.13.0
BuildRequires:	pkgconfig(libglade-2.0) >=  2.0.0
BuildRequires:	pkgconfig(libgnomecanvas-2.0) >= 1.116.0
BuildRequires:	pkgconfig(libgnome-2.0) >= 2.13.0
BuildRequires:	pkgconfig(libpng)
%if %{build_xvfb}
BuildRequires:	x11-server-xvfb
%endif

%description
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package contains various needed modules and files for bonobo 2
to operate.

%package -n %{libname}
Summary:	Library for compound documents in GNOME
Group:		%{group}

%description -n %{libname}
This package provides a shared library for %{name}.

%package -n %{devname}
Summary:	Development libraries, include files and sample code for Bonobo 2
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname -d bonoboui 2 0} < 2.24.5-5
Obsoletes:	%{mklibname -d bonoboui 2} < 2.24.5-5

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop programs using the Bonobo document model;
it includes demonstration executables and codes as well.


%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
%if %enable_gtkdoc
	--enable-gtk-doc
%endif

%make

%check
%if %{build_xvfb}
xvfb-run -a make check
%else
make check
%endif

%install
%makeinstall_std

%find_lang %{name}-2.0

%files -f %{name}-2.0.lang
%doc README NEWS changes.txt
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo-2.0
%{_libdir}/libglade/2.0/*.so
%{_datadir}/gnome-2.0
%{_datadir}/applications/bonobo-browser.desktop

%files -n %{libname}
%{_libdir}/libbonoboui-%{api}.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libbonobo*.so
%{_libdir}/pkgconfig/*

