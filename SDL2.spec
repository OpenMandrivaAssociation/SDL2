%define api 2.0
%define major 1
%define libname %mklibname %{name}_ %{api} %{major}
%define devname %mklibname %{name} -d

Summary:	Simple DirectMedia Layer
Name:		SDL2
Version:	2.0.7
Release:	1
License:	Zlib
Group:		System/Libraries
Url:		http://www.libsdl.org/
Source0:	http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:	FindSDL2.cmake
Patch0:		SDL2-2.0.3-cmake.patch
Patch1:		SDL2-2.0.3-cmake-joystick.patch
BuildRequires:	nas-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libpulse-simple)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(samplerate)
%ifnarch %{armx}
BuildRequires:	vulkan-devel
%endif
BuildRequires:	cmake

#----------------------------------------------------------------------------

%description
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
# SDL 2.0's soname went from 1 to 0...
# Let's provide .so.1 as well for compatibility
%if "%{_lib}" == "lib64"
Provides:	libSDL2-%{api}.so.1()(64bit)
%else
Provides:	libSDL2-%{api}.so.1
%endif

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%files -n %{libname}
%{_libdir}/libSDL2-%{api}.so.0*
%{_libdir}/libSDL2-%{api}.so.1*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	pkgconfig(alsa)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(egl)

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%files -n %{devname}
%doc README.txt README-SDL.txt CREDITS.txt COPYING.txt BUGS.txt WhatsNew.txt
%{_bindir}/sdl2-config
%{_libdir}/pkgconfig/sdl2.pc
%{_libdir}/libSDL2-%{api}.so
%{_libdir}/libSDL2.so
%dir %{_includedir}/SDL2
%{_includedir}/SDL2/*.h
%{_datadir}/aclocal/sdl2.m4
%{_datadir}/cmake/Modules/FindSDL2.cmake
%{_prefix}/lib/cmake/SDL2

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

%build
# all programs using SDL2 hang when built with clang
export CC=gcc
%cmake \
%ifnarch %{ix86}
	-DSSEMATH:BOOL=OFF \
%endif
%ifnarch %{armx}
	-DVIDEO_VULKAN:BOOL=ON \
%endif
	-DRPATH:BOOL=OFF


%make

%install
%makeinstall_std -C build
install -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/cmake/Modules/FindSDL2.cmake

ln -s libSDL2-%{api}.so.0 %{buildroot}%{_libdir}/libSDL2-%{api}.so.1

rm -f %{buildroot}%{_libdir}/*.a
