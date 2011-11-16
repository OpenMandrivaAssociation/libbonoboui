# enable_gtkdoc: toggle if gtk-doc stuff should be rebuilt.
#	0 = no
#	1 = yes
%define enable_gtkdoc	1

# End of user configurable section
%{?_without_gtkdoc: %{expand: %%define	enable_gtkdoc 0}}
%{?_with_gtkdoc: %{expand: %%define	enable_gtkdoc 1}}

%define api_version	2
%define lib_major	0
%define lib_name	%mklibname bonoboui %{api_version} %{lib_major}
%define develname	%mklibname -d bonoboui

# define to use Xvfb
%define build_xvfb 1

# Allow --with[out] <feature> at rpm command line build
%{?_without_XVFB: %{expand: %%define	build_xvfb 0}}
%{?_with_XVFB: %{expand: %%define	build_xvfb 1}}


Name:		libbonoboui
Summary:	Library for compound documents in GNOME
Version:	2.24.5
Release:	4
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:	automake
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
BuildRequires:	intltool
BuildRequires:	pkgconfig(bonobo-activation-2.0) >= 2.13.0
BuildRequires:	pkgconfig(libbonobo-2.0) >= 2.13.0
BuildRequires:	pkgconfig(libglade-2.0) >=  2.0.0
BuildRequires:	pkgconfig(gdk-x11-2.0) >= 2.2.0
BuildRequires:	pkgconfig(libgnomecanvas-2.0) >= 1.116.0
BuildRequires:	pkgconfig(libgnome-2.0) >= 2.13.0
BuildRequires:	pkgconfig(libpng12)
BuildRequires:	perl-XML-Parser
%if %{build_xvfb}
BuildRequires:	x11-server-xvfb
%endif

Requires:	%{lib_name} = %{version}-%{release}

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

%description -n %{lib_name}
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides libraries to use Bonobo.


%package -n %{develname}
Summary:	Development libraries, include files and sample code for Bonobo 2
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes:	%mklibname -d bonoboui 2 0
Obsoletes:	%mklibname -d bonoboui 2

%description -n %{develname}
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
rm -rf %{buildroot}
%makeinstall_std

%{find_lang} %{name}-2.0

# remove unpackaged files
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files -f %{name}-2.0.lang
%doc README NEWS changes.txt
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo-2.0
%{_libdir}/libglade/2.0/*.so
%{_datadir}/gnome-2.0
%{_datadir}/applications/bonobo-browser.desktop

%files -n %{lib_name}
%{_libdir}/libbonoboui-%{api_version}.so.%{lib_major}*

%files -n %{develname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libbonobo*.so
%{_libdir}/pkgconfig/*

