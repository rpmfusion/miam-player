# https://github.com/MBach/Miam-Player/commit/1a21b01a86c4cbcfe8fc6d99cf6e595838856b11
%global commit0 1a21b01a86c4cbcfe8fc6d99cf6e595838856b11
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%define _name   Miam-Player
Name:           miam-player
Version:        0.8.1
Release:        0.12git%{shortcommit0}%{?dist}
Summary:        A nice music player
License:        GPLv3+ and "BSD (3 clause)"
Url:            http://miam-player.org/
Source0:        https://github.com/MBach/Miam-Player/archive/%{commit0}/%{name}-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  qtav-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5WebSockets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qtsingleapplication-qt5-devel
BuildRequires:  pkgconfig(taglib)
BuildRequires:  libappstream-glib
BuildRequires:  libchromaprint-devel
Requires:       hicolor-icon-theme

%description
Miam Player is a FOSS music player based on Qt5.

Features:
 - Read .mp3, .m4a (MP4), .flac, .ogg, .oga (OGG Vorbis), .asf,
  .ape (Monkey Audio) and more.
 - Read and edit lots of tags using Taglib.
 - Customize everything: user interface, covers, shortcuts,
   buttons, themes.
 - Fast and reliable (audio player is provided by VLC Media Player).

A plugin system makes it possible to extend player possibilities.

%package devel
Summary:        Miam Player development files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for Miam Player.

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
BuildArch:      noarch

%description    doc
The %{name}-doc package contains html documentation
that use %{name}.

%prep
%setup -qn %{_name}-%{commit0}

# remove 3dparty libs an debian, osx and windows part
rm -rf src/Core/3rdparty/{taglib,QtAV}
rm -rf lib/
rm -rf debian osx windows
rm -rf src/Player/release/.moc

# remove bundled QtSingleApplication library
# The qtsingleapplication.h file in miam-player is modified, see line #88
# https://github.com/MBach/Miam-Player/blob/master/src/Player/qtsingleapplication/qtsingleapplication.h#L88
# The fedora provided system lib is never going to work, because upstream uses a modified version.

%build
%{_qt5_qmake} \
    QMAKE_CFLAGS="${RPM_OPT_FLAGS}" \
    QMAKE_CXXFLAGS="${RPM_OPT_FLAGS}" \
    QMAKE_LFLAGS="${RPM_LD_FLAGS} -Wl,--as-needed" \
    LIB_SUFFIX="$(echo %_lib | cut -b4-)" \
    CONFIG+="no_rpath recheck config_libass_link debug" 
%make_build

# update Doxyfile
doxygen -u Doxyfile
# build docs
doxygen

%install
make install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

# As the icon is only in jpg or ico, we need to convert it in png for our desktop file.
for size in 256 64 48 32 16; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
    convert src/player/mp.png -resize $size %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/libmiam-*.so.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files devel
%{_libdir}/libmiam-*.so

%files doc
%doc doc/html

%changelog
* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8.1-0.12git1a21b01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 06 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.11git1a21b01
- Rebuild
- Update to 0.8.1-0.11git1a21b01

* Mon Feb 06 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.10git1a21b01
- Update to 0.8.1-0.10git1a21b01
- Dropped remotecontrol.patch
- Dropped install_acoustid.patch

* Sun Feb 05 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.8.1-0.9gita057928
- Add patch to install libmiam-acoustid.so

* Sat Feb 04 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.8gita057928
- Update to 0.8.1-0.8gita057928
- Add BR libchromaprint-devel

* Wed Dec 28 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.7gitbc63ae5
- Update to 0.8.1-0.7gitbc63ae5

* Sun Sep 18 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.6git8aba652
- Changed license tag added "BSD (3 clause)"
- Added BR qtsingleapplication-qt5-devel

* Sat Sep 17 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.5git8aba652
- Added BR pkgconfig(Qt5X11Extras)

* Sat Sep 17 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.4git8aba652
- Use ${RPM_LD_FLAGS} for QMAKE_LFLAGS

* Sat Sep 17 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.3git8aba652
- Update to 0.8.1-0.3git8aba652
- Added BR libappstream-glib
- Use ${RPM_OPT_FLAGS} instead of %%{optflags}

* Mon Aug 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.2git193ab01
- Removed BR hicolor-icon-theme
- Added Requires hicolor-icon-theme
- Added %%{optflags} to QMAKE_LFLAGS
- Use %%make_build instead of make %%{?_smp_mflags}
- Remove validating desktop-file from %%check section because desktop-file-install
  is already used 

* Fri Aug 19 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-0.1git193ab01
- Update to 0.8.1-0.1git193ab01
- Added BR pkgconfig(Qt5WebSockets)

* Mon Jul 25 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.8gitf327cd8
- Update to last git release

* Sun Jul 10 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.7git3746473
- Update to last git release
- Cleanup spec file

* Thu Mar 24 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.6git6fc21a6
- Update to last git release
- added debug flag

* Wed Feb 10 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.5gitcace477
- Update to last git release
- added QMAKE_LFLAGS flag due unused-direct-shlib-dependency warnings
- dropped BR pkgconfig(libVLCQtCore)
- dropped BR pkgconfig(libVLCQtQml)
- dropped BR pkgconfig(libVLCQtWidgets)
- dropped %%{name}.appdata.xml

* Fri Feb 05 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.4git06d87d6
- added arch-specific macro %%{?_isa} to the package name.
- added %%license tag
- moved doc files to the -doc subpackage
- removed .moc files in %%prep section

* Fri Feb 05 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.3git06d87d6
- Update to last git release
- added %%{name}.appdata.xml file

* Thu Feb 04 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.2gitc552b40
- Update to last git release
- dropped %%{name}-0.9.0-libsuffix.patch

* Thu Feb 04 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-0.1git458b183
- initial build
