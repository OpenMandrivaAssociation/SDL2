%define	api	2.0
%define	major	0
%define	libname	%mklibname %{name}_ %{api} %{major}
%define	devname	%mklibname %{name} -d

Summary:	Simple DirectMedia Layer
Name:		SDL2
Version:	2.0.0
Release:	0.3
License:	Zlib
Group:		System/Libraries
Url:		http://www.libsdl.org/
Source0:	http://www.libsdl.org/release/%{name}-%{version}.tar.gz

BuildRequires:	nas-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zlib)

#----------------------------------------------------------------------------

%description
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%files -n %{libname}
%doc README.txt README-SDL.txt CREDITS.txt COPYING.txt BUGS.txt WhatsNew.txt
%{_libdir}/libSDL2-%{api}.so.%{major}*

#----------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%files -n %{devname}
%doc README.txt README-SDL.txt CREDITS.txt COPYING.txt BUGS.txt WhatsNew.txt
%{_bindir}/sdl2-config
%{_libdir}/pkgconfig/sdl2.pc
%{_libdir}/*.so
%dir %{_includedir}/SDL2
%{_includedir}/SDL2/*.h
%{_datadir}/aclocal/sdl2.m4

#----------------------------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--disable-esd \
	--disable-oss \
	--enable-pulseaudio \
	--enable-pulseaudio-shared \
	--enable-alsa \
	--enable-alsa-shared

sed -i s,"objdir=.libs","objdir=",g libtool
%make

%install
rm build/libSDL2.la
cp build/libSDL2.lai build/libSDL2.la
%makeinstall_std

rm -f %{buildroot}%{_libdir}/*.a

