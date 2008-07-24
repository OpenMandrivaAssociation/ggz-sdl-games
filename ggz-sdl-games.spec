%define version 0.0.14.1
%define release %mkrel 3

%define libggz_version %{version}
%define ggz_client_libs_version %{version}

# list of game description files
%define games_list ttt3d geekgame

Name:		ggz-sdl-games
Summary:	GGZ Games in SDL user interface
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		http://www.ggzgamingzone.org/
BuildRoot:	%_tmppath/%{name}-%{version}-%{release}-buildroot

Source:		http://prdownload.sourceforge.net/ggz/%{name}-%{version}.tar.bz2

BuildRequires:	libggz-devel = %{libggz_version}
BuildRequires:	ggz-client-libs-devel = %{ggz_client_libs_version}
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	mesagl-devel
Requires:	libggz = %{libggz_version}
Requires:		ggz-client-libs = %{ggz_client_libs_version}
Requires:		libggz = %{libggz_version}
Provides:	ggz-game-modules = %{version}

%description
The complete set of GGZ Gaming Zone games in SDL user interface.
Includes all of the following:

TicTacToe 3D:   OpenGL client compatible to other TicTacToe clients
The Geek Game:  Calculate numbers in all directions and wrap around edges

%prep
%setup -q

%build
#export LDFLAGS=-L%{_prefix}/X11R6/%{_lib}
%configure2_5x --with-libggz-libraries=%{_libdir} --with-ggzmod-libraries=%{_libdir} --with-ggzcore-libraries=%{_libdir}
%make


%install
rm -rf %{buildroot}

# Create a ggz.modules file so we can make install easily
mkdir -p %{buildroot}%{_sysconfdir}
echo "[Games]" > %{buildroot}%{_sysconfdir}/ggz.modules

%makeinstall_std

rm %{buildroot}%{_sysconfdir}/ggz.modules
rmdir %{buildroot}%{_sysconfdir}

# Get a copy of all of our .dsc files
mkdir -p %{buildroot}%{_datadir}/ggz/ggz-config
for i in %games_list; do
  install -m 0644 $i/module.dsc %{buildroot}%{_datadir}/ggz/ggz-config/sdl-$i.dsc
done

%clean
rm -rf %{buildroot}


%post
# Run ggz-config vs. all installed games
if [ -f %{_sysconfdir}/ggz.modules -a -x %{_bindir}/ggz-config ]; then
  for i in %games_list; do
    ggz-config --install --modfile=%{_datadir}/ggz/ggz-config/sdl-$i.dsc --force
  done
fi


%preun
# Run ggz-config to uninstall all the games
if [ $1 = 0 ]; then
  if [ -f %{_sysconfdir}/ggz.modules -a -x %{_bindir}/ggz-config ]; then
    for i in %games_list; do
      ggz-config --remove --modfile=%{_datadir}/ggz/ggz-config/sdl-$i.dsc
    done
  fi
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README README.GGZ QuickStart.GGZ
%{_libdir}/ggz/*
%{_datadir}/ggz/geekgame
%{_datadir}/ggz/ggz-config/*
%{_datadir}/ggz/ttt3d


