#
# Conditional build:
%bcond_without	tests		# do not perform "make test"

%define	libgit2_version	%(rpm -q --qf '%{VERSION}' libgit2)

%define	pdir	Git
%define	pnam	Raw
Summary:	Git::Raw - Perl bindings to the Git linkable library (libgit2)
Name:		perl-Git-Raw
Version:	0.90
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/J/JA/JACQUESG/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	1ef1bd947245e86c60458a22fbf097b7
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-git_buf_dispose.patch
URL:		http://search.cpan.org/dist/Git-Raw/
BuildRequires:	libgit2-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgit2 is a pure C implementation of the Git core methods provided
as a re-entrant linkable library designed to be fast and portable with
a solid API. This module provides Perl bindings to the libgit2 API.

WARNING: The API of this module is unstable and may change without
warning (any change will be appropriately documented in the changelog)

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1
%patch1 -p1

rm -rf deps
%{__grep} -v '^deps/' MANIFEST > MANIFEST.new
%{__mv} MANIFEST.new MANIFEST

%{__sed} -i -e 's/0\.27\.0/%{libgit2_version}/g' t/02-commit.t

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorarch}/Git
%{perl_vendorarch}/Git/Raw
%{perl_vendorarch}/Git/Raw.pm
%dir %{perl_vendorarch}/auto/Git
%dir %{perl_vendorarch}/auto/Git/Raw
%attr(755,root,root) %{perl_vendorarch}/auto/Git/Raw/*.so
%{_mandir}/man3/Git::Raw.3pm*
%{_mandir}/man3/Git::Raw::*.3pm*
