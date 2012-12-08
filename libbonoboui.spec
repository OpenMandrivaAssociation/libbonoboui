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
Release:	5
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
BuildRequires:	pkgconfig(libpng)
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
Obsoletes:	%{mklibname -d bonoboui 2 0} < 2.24.5-5
Obsoletes:	%{mklibname -d bonoboui 2} < 2.24.5-5

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

%files -n %{lib_name}
%{_libdir}/libbonoboui-%{api_version}.so.%{lib_major}*

%files -n %{develname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libbonobo*.so
%{_libdir}/pkgconfig/*



%changelog
* Wed Nov 16 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.24.5-4
+ Revision: 730805
- rebuild
  cleaned up spec
  removed defattr
  removed dup README & NEWS in lib pkg
  removed old ldconfig scriptlets
  removed clean section
  disabled static build
  removed .la files
  removed reqs for devel pkg in devel pkg
  removed req for main pkg in devel & lib pkgs
  removed extra virtual devel pkg provides
  updated devel pkg summary
  removed req in lib pkg for libbonobo-activation
  converted BRs to pkgconfig provides
  removed mkrel macro
  dropped api from devel pkg name

* Mon Sep 19 2011 Götz Waschk <waschk@mandriva.org> 2.24.5-3
+ Revision: 700345
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.24.5-2
+ Revision: 662350
- mass rebuild

* Mon Apr 04 2011 Götz Waschk <waschk@mandriva.org> 2.24.5-1
+ Revision: 650233
- update to new version 2.24.5

* Tue Dec 14 2010 Funda Wang <fwang@mandriva.org> 2.24.4-2mdv2011.0
+ Revision: 621680
- rebuild for popt

* Tue Sep 28 2010 Götz Waschk <waschk@mandriva.org> 2.24.4-1mdv2011.0
+ Revision: 581724
- update to new version 2.24.4

* Tue Mar 30 2010 Götz Waschk <waschk@mandriva.org> 2.24.3-1mdv2010.1
+ Revision: 529609
- update to new version 2.24.3

* Wed Feb 17 2010 Funda Wang <fwang@mandriva.org> 2.24.2-2mdv2010.1
+ Revision: 506909
- rebuild for new popt

* Wed Sep 23 2009 Götz Waschk <waschk@mandriva.org> 2.24.2-1mdv2010.0
+ Revision: 447641
- update to new version 2.24.2

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.24.1-2mdv2010.0
+ Revision: 425519
- rebuild

* Fri Mar 06 2009 Götz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 349854
- update to new version 2.24.1

* Mon Sep 22 2008 Götz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 286608
- new version

* Tue Aug 05 2008 Götz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 264036
- simplify Xvfb call
- new version
- drop patch

* Mon Jul 14 2008 Adam Williamson <awilliamson@mandriva.org> 2.23.4-2mdv2009.0
+ Revision: 234395
- add patch from upstream SVN to use g_type instead of gtktype - fixes build
  of brasero

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 2.23.4-1mdv2009.0
+ Revision: 230973
- new version
- update license

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 2.22.0-2mdv2008.1
+ Revision: 189663
- Fix groups

* Mon Mar 10 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183620
- new version

* Mon Jan 28 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159184
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Sep 17 2007 Götz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.0
+ Revision: 89111
- new version
- new devel name

* Mon Jul 30 2007 Götz Waschk <waschk@mandriva.org> 2.19.6-1mdv2008.0
+ Revision: 56578
- new version

* Tue Jun 19 2007 Götz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 41458
- new version


* Mon Mar 12 2007 Götz Waschk <waschk@mandriva.org> 2.18.0-1mdv2007.1
+ Revision: 141804
- new version

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 2.17.94-1mdv2007.1
+ Revision: 126139
- new version
- drop merged patch
- new version
- fix syntax error in Makefile

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 2.17.92-1mdv2007.1
+ Revision: 125969
- new version

* Mon Feb 12 2007 Götz Waschk <waschk@mandriva.org> 2.17.91-1mdv2007.1
+ Revision: 119043
- new version

* Mon Jan 22 2007 Götz Waschk <waschk@mandriva.org> 2.17.90-1mdv2007.1
+ Revision: 111932
- new version

* Wed Jan 10 2007 Götz Waschk <waschk@mandriva.org> 2.17.0-1mdv2007.1
+ Revision: 106901
- new version

* Thu Nov 30 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-2mdv2007.1
+ Revision: 88941
- Import libbonoboui

* Thu Nov 30 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-2mdv2007.1
- Rebuild

* Tue Sep 05 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- New release 2.16.0

* Sat Sep 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.1-1mdv2007.0
- Release 2.15.1

* Wed Aug 09 2006 Götz Waschk <waschk@mandriva.org> 2.15.0-1mdv2007.0
- New release 2.15.0

* Thu Aug 03 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-5mdv2007.0
- Rebuild again

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-4mdv2007.0
- Rebuild with latest dbus

* Wed Jul 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-3mdv2007.0
- Rebuild to drop howl requirement in .la file

* Sat Jun 17 2006 G�tz Waschk <waschk@mandriva.org> 2.14.0-2mdv2007.0
- fix check

* Thu Apr 13 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-1mdk
- Release 2.14.0

* Wed Mar 01 2006 Götz Waschk <waschk@mandriva.org> 2.10.1-5mdk
- Rebuild to remove howl dep

* Thu Feb 23 2006 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-4mdk
- Use mkrel

* Thu Nov 17 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-3mdk
- Rebuild with latest openssl

* Fri Sep 02 2005 Götz Waschk <waschk@mandriva.org> 2.10.1-2mdk
- rebuild to remove glitz dep

* Tue Aug 23 2005 Götz Waschk <waschk@mandriva.org> 2.10.1-1mdk
- New release 2.10.1

* Thu Jul 07 2005 G�tz Waschk <waschk@mandriva.org> 2.10.0-1mdk
- New release 2.10.0

* Fri May 20 2005 Austin Acton <austin@mandriva.org> 2.8.1-2mdk
- provide a lib64 compatible provides for devel package

* Sat Feb 05 2005 G�tz Waschk <waschk@linux-mandrake.com> 2.8.1-1mdk
- update file list
- enable gtk-doc
- drop the patch
- New release 2.8.1

* Tue Jan 04 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.0-3mdk 
- Rebuild with latest howl

* Fri Nov 12 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.8.0-2mdk
- add BuildRequires: intltool

* Tue Oct 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.0-1mdk
- New release 2.8.0
- Patch0 (CVS): fix toolbar finalization

* Sat May 15 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.6.1-1mdk
- New release 2.6.1

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-2mdk
- Fix BuildRequires

* Tue Apr 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-1mdk
- Release 2.6.0 (with G�tz help)
- Remove patch0 (merged upstream)

* Thu Mar 18 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.3-3mdk
- Patch0 (Alex) : fix precondition being too agressive, causing wrong
  assert when exiting nautilus

