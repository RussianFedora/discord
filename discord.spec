%global privlibs libffmpeg|libnode
%global __requires_exclude ^(%{privlibs})\\.so
%global __provides_exclude_from .*\\.so
%global debug_package %{nil}

Name: discord
Version: 0.0.2
Release: 1%{?dist}

Summary: Free voice and text chats for gamers
URL: https://discordapp.com/
License: Proprietary
ExclusiveArch: x86_64

Source0: https://dl.discordapp.net/apps/linux/%{version}/%{name}-%{version}.tar.gz
Source1: %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: %{_bindir}/convert

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires: hicolor-icon-theme

%description
All-in-one voice and text chat for gamers that's free, secure, and
works on both your desktop and phone. Stop paying for TeamSpeak
servers and hassling with Skype. Simplify your life.

%prep
%autosetup -n Discord

%build
# Do nothing...

%install
# Creating general directories...
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}/opt/%{name}/

# Creating ghost file for alternatives system...
touch %{buildroot}%{_bindir}/%{name}

# Installing to working directory from official package...
cp -r %_builddir/Discord %{buildroot}/opt

# Installing icons...
for size in 16 32 48 64 128 256 512; do
    dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
    mkdir -p $dir
    convert -resize ${size}x${size} %_builddir/Discord/%{name}.png "$dir/%{name}.png"
done

# Removing some unused files...
rm -f %{buildroot}/opt/%{name}/*.sh
rm -f %{buildroot}/opt/%{name}/%{name}.desktop
rm -f %{buildroot}/opt/%{name}/%{name}.png

# Marking as executable...
chmod +x %{buildroot}/opt/%{name}/%{name}

# Creating desktop icon...
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} %{name} /opt/%{name}/%{name} 10
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{name} /opt/%{name}/%{name}
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
/opt/%{name}
%ghost %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Wed Nov 29 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.0.2-1
- Initial SPEC release.