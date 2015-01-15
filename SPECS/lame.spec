Name:           %{name}
Version:        %{ver}
Release:        %{rel}%{?dist}
Summary:        LAME Ain't an MP3 Encoder... but it's the best of all
BuildArch:      %{arch}
Group:          Applications/Multimedia
License:        LGPL
URL:            http://lame.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-c++
BuildRequires:  gtk2-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  ncurses-devel
BuildRequires:  prelink
%ifarch %{ix86} x86_64
BuildRequires:  nasm
%endif

Provides:       mp3encoder = %{version}-%{release}

Source:         lame-%{version}.tar.gz

%description
LAME is an educational tool to be used for learning about MP3 encoding.  The
goal of the LAME project is to use the open source model to improve the
psychoacoustics, noise shaping and speed of MP3. Another goal of the LAME
project is to use these improvements for the basis of a patent-free audio
compression codec for the GNU project.

%package devel
Summary:        Header files, libraries and development documentation for %{name}.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q

%build
%configure \
    --disable-dependency-tracking \
    --disable-static \
	 --disable-rpath \
    --program-prefix="%{?_program_prefix}" \
%ifarch %{ix86} x86_64
    --enable-nasm \
%endif
    --enable-analyser="no" \
    --enable-brhist \
    --enable-decoder \
    --with-vorbis

# remove rpath
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} all CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

### Some apps still expect to find <lame.h>
%{__ln_s} -f lame/lame.h %{buildroot}%{_includedir}/lame.h

### Clean up documentation to be included
find doc/html -name "Makefile*" | xargs rm -f
%{__rm} -rf %{buildroot}%{_docdir}/lame/

### Clear not needed executable stack flag bit
execstack -c %{buildroot}%{_libdir}/*.so.*.*.* || :

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING INSTALL* doc/html/
%doc LICENSE README TODO USAGE
%doc %{_mandir}/man1/lame.1*
%{_bindir}/lame
%{_libdir}/libmp3lame.so.*

%files devel
%defattr(-, root, root, 0755)
%doc API DEFINES HACKING STYLEGUIDE
%{_includedir}/lame/
%{_includedir}/lame.h
%{_libdir}/libmp3lame.so
%exclude %{_libdir}/libmp3lame.la

%changelog
* Thu Jan 15 2015 Daniel Menet <daniel.menet@swisstxt.ch> -3.99.5-1
- Initial release based on https://github.com/lkiesow/matterhorn-rpms/blob/master/specs/lame.spec