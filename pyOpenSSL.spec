%if 0%{?fedora} > 12
%global with_python3 1
%endif

Summary: Python wrapper module around the OpenSSL library
Name: pyOpenSSL
Version: 0.13.1
Release: 4%{?dist}
Source0: http://pypi.python.org/packages/source/p/pyOpenSSL/pyOpenSSL-%{version}.tar.gz

# Fedora specific patches

Patch2: pyOpenSSL-elinks.patch
Patch3: pyOpenSSL-nopdfout.patch

Patch10: pyOpenSSL-0.13-check-error.patch
Patch11: pyOpenSSL-0.13.1-test-failure.patch
Patch12: pyOpenSSL-0.13.1-exception.patch
Patch13: pyOpenSSL-0.13.1-digest.patch

License: ASL 2.0
Group: Development/Libraries
Url: http://pyopenssl.sourceforge.net/

BuildRequires: elinks
BuildRequires: openssl-devel
BuildRequires: tetex-dvips
BuildRequires: tetex-latex
BuildRequires: latex2html

BuildRequires: python2-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%description
High-level wrapper around a subset of the OpenSSL library, includes among others
 * SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 * Callbacks written in Python
 * Extensive error-handling mechanism, mirroring OpenSSL's error codes

%if 0%{?with_python3}
%package -n python3-pyOpenSSL
Summary: Python wrapper module around the OpenSSL library

%description -n python3-pyOpenSSL
High-level wrapper around a subset of the OpenSSL library, includes among others
 * SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 * Callbacks written in Python
 * Extensive error-handling mechanism, mirroring OpenSSL's error codes
%endif

%package doc
Summary: Documentation for pyOpenSSL
BuildArch: noarch

%description doc
Documentation for pyOpenSSL

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch}/.*\.so$ 
%endif
%filter_requires_in %{_datadir}/doc/ 
%filter_setup
}

%prep
%setup -q -n pyOpenSSL-%{version}
%patch2 -p1 -b .elinks
%patch3 -p1 -b .nopdfout
%patch10 -p1 -b .error
%patch11 -p1 -b .test-failure
%patch12 -p1 -b .exception
%patch13 -p1 -b .digest

# Fix permissions for debuginfo package
%{__chmod} -x OpenSSL/ssl/connection.c

%build
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

CFLAGS="%{optflags} -fno-strict-aliasing" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python3} setup.py build
popd
%endif

%{__make} -C doc ps
%{__make} -C doc text html

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%files
%{python_sitearch}/OpenSSL/
%{python_sitearch}/pyOpenSSL-*.egg-info

%if 0%{?with_python3}
%files -n python3-pyOpenSSL
%{python3_sitearch}/OpenSSL/
%{python3_sitearch}/pyOpenSSL-*.egg-info
%endif

%files doc
%doc README doc/pyOpenSSL.* doc/html

%changelog
* Fri May  4 2018 Tomáš Mráz <tmraz@redhat.com> - 0.13.1-4
- fix various testsuite failures
- fix exception propagation from private key passphrase callback (#1227505)
- add optional digest parameter to CRL.export method (#1523772)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.13.1-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.13.1-2
- Mass rebuild 2013-12-27

* Thu Sep  5 2013 Tomáš Mráz <tmraz@redhat.com> - 0.13.1-1
- new upstream release fixing a security issue with string
  formatting subjectAltName of a certificate

* Tue Aug 06 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13-8
- Python 3 subpackage
- Split documentation off into noarch subpackage

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Tomáš Mráz <tmraz@redhat.com> - 0.13-6
- Check for error returns which cause segfaults in FIPS mode
- Fix missing error check and leak found by gcc-with-cpychecker (#800086)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 12 2012 Petr Pisar <ppisar@redhat.com> - 0.13-4
- Do not scan documentation for dependencies (bug #865806)

* Mon Oct 08 2012 Dan Horák <dan[at]danny.cz> - 0.13-3
- rebuilt because ARM packages had wrong Requires autodetected

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Tomas Mraz <tmraz@redhat.com> - 0.13-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Tomas Mraz <tmraz@redhat.com> - 0.12-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-2
- Fix incompatibility with python-2.7's socket module.

* Mon Oct  4 2010 Tomas Mraz <tmraz@redhat.com> - 0.10-1
- Merge-review cleanup by Parag Nemade (#226335)
- New upstream release

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Sep 29 2009 Matěj Cepl <mcepl@redhat.com> - 0.9-1
- New upstream release
- Fix BuildRequires to make Postscript documentation buildable

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.7-7
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Dennis Gilmore <dennis@ausil.us> - 0.7-4
- rebuild against now openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.7-3
- Rebuild for Python 2.6

* Fri Sep 19 2008 Dennis Gilmore <dennis@ausil.us> - 0.7-2
- update threadsafe  patch 
- bug#462807

* Mon Sep 15 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.7-1
- bump to new release
- the inevitable patch fixes


* Wed Mar 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6-4
- fix horrific release tag
- fix license tag
- add egg-info

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6-3.p24.9
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Jeremy Katz <katzj@redhat.com> - 0.6-2.p24.9
- rebuild for new openssl

* Mon Dec 11 2006 Paul Howarth <paul@city-fan.org> - 0.6-1.p24.9
- add missing buildreq latex2html, needed to build HTML docs
- rewrite to be more in line with Fedora python spec template and use
  %%{python_sitearch} rather than a script-generated %%files list
- package is not relocatable - drop Prefix: tag
- buildreq perl not necessary
- fix permissions for files going into debuginfo package

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.6-1.p24.8
- rebuild for python 2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6-1.p24.7.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6-1.p24.7.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6-1.p24.7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Mihai Ibanescu <misa@redhat.com> - 0.6-1.p24.7
- rebuilt against newer openssl

* Wed Aug 24 2005 Jeremy Katz <katzj@redhat.com> - 0.6-1.p24.6
- add dcbw's patch to fix some threading problems

* Wed Aug 03 2005 Karsten Hopp <karsten@redhat.de> 0.6-1.p24.5
- current rpm creates .pyo files, include them in filelist

* Thu Mar 17 2005 Mihai Ibanescu <misa@redhat.com> 0.6-1.p24.4
- rebuilt

* Mon Mar 14 2005 Mihai Ibanescu <misa@redhat.com> 0.6-1.p24.3
- rebuilt

* Mon Mar  7 2005 Tomas Mraz <tmraz@redhat.com> 0.6-1.p23.2
- rebuild with openssl-0.9.7e

* Tue Nov  9 2004 Nalin Dahyabhai <nalin@redhat.com> 0.6-1.p23.1
- rebuild

* Fri Aug 13 2004 Mihai Ibanescu <misa@redhat.com> 0.6-1
- 0.6 is out

* Tue Aug 10 2004 Mihai Ibanescu <misa@redhat.com> 0.6-0.90.rc1
- release candidate

* Thu Jun 24 2004 Mihai Ibanescu <misa@redhat.com> 0.5.1-24
- rebuilt

* Mon Jun 21 2004 Mihai Ibanescu <misa@redhat.com> 0.5.1-23
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov  5 2003 Mihai Ibanescu <misa@redhat.com> 0.5.1-20
- rebuilt against python 2.3.2

* Fri Aug  8 2003 Mihai Ibanescu <misa@redhat.com> 0.5.1-12
- lynx no longer supported, using elinks instead (patch from
  Michael Redinger <michael.redinger@uibk.ac.at>, bug #101947 )

* Wed Jun  4 2003 Elliot Lee <sopwith@redhat.com> 0.5.1-11
- Rebuilt

* Wed Jun  4 2003 Mihai Ibanescu <misa@redhat.com> 0.5.1-10.7.x
- Built on 7.x

* Mon Mar  3 2003 Mihai Ibanescu <misa@redhat.com> 0.5.1-9
- bug #73967: Added Requires: python 

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Mihai Ibanescu <misa@redhat.com> 0.5.1-7
- bug #84803: Added patch to expose more flags

* Fri Jan 31 2003 Mihai Ibanescu <misa@redhat.com> 0.5.1-5
- installing to %%{_libdir}

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.5.1-3
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- Add -I and -L flags for finding Kerberos headers and libraries, in case
  they're referenced

* Tue Dec  3 2002 Mihai Ibanescu <misa@redhat.com>
- Fix for bug 73967: site-packages/OpenSSL not owned by this package
- Adding hacks around the lack of latex2html on ia64

* Tue Sep 24 2002 Mihai Ibanescu <misa@redhat.com>
- 0.5.1

* Thu Aug 29 2002 Mihai Ibanescu <misa@redhat.com>
- Building 0.5.1rc1 with version number 0.5.0.91 (this should also fix the big
  error of pushing 0.5pre previously, since it breaks rpm's version comparison
  algorithm).
- We use %%{__python}. Too bad I can't pass --define's to distutils.

* Fri Aug 16 2002 Mihai Ibanescu <misa@redhat.com>
- Building 0.5

* Fri Jun 14 2002 Mihai Ibanescu <misa@redhat.com>
- Added documentation
