%define api 2.0
%define major 1
%define libname %mklibname %{name}_ %{api} %{major}
%define devname %mklibname %{name} -d

%global optflags %{optflags} -O3

Summary:	Simple DirectMedia Layer
Name:		SDL2
Version:	2.0.12
Release:	1
License:	Zlib
Group:		System/Libraries
Url:		http://www.libsdl.org/
Source0:	http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:	FindSDL2.cmake
Patch0:		SDL2-2.0.3-cmake.patch
Patch1:		SDL2-2.0.3-cmake-joystick.patch
Patch2:		https://src.fedoraproject.org/rpms/SDL2/raw/master/f/SDL2-2.0.9-khrplatform.patch
%ifnarch %{riscv}
BuildRequires:	nas-devel
%endif
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libusb-1.0)
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
BuildRequires:	pkgconfig(gbm)
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

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%files -n %{devname}
%doc README.txt README-SDL.txt CREDITS.txt COPYING.txt BUGS.txt WhatsNew.txt
%{_bindir}/sdl2-config
%{_libdir}/pkgconfig/sdl2.pc
%{_libdir}/libSDL2-%{api}.so
%{_libdir}/libSDL2.so
%{_libdir}/libSDL2main.a
%dir %{_includedir}/SDL2
%{_includedir}/SDL2/*.h
%{_datadir}/aclocal/sdl2.m4
%{_datadir}/cmake/Modules/FindSDL2.cmake
%{_libdir}/cmake/SDL2/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
%ifnarch %{ix86} %{x86_64}
	-DSSEMATH:BOOL=OFF \
%endif
%ifarch znver1
	-DSSEMATH:BOOL=ON \
%endif
	-DESD:BOOL=OFF \
	-DESD_SHARED:BOOL=OFF \
	-DSDL_STATIC:BOOL=OFF \
	-DVIDEO_VULKAN:BOOL=ON \
	-DRPATH:BOOL=OFF


%make_build

%install
%make_install -C build
install -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/cmake/Modules/FindSDL2.cmake

ln -s libSDL2-%{api}.so.0 %{buildroot}%{_libdir}/libSDL2-%{api}.so.1
