%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif
%if "%distro_section" == "tainted"
%global build_plf 1
%endif
%define build_pvm 0
%{?_without_pvm:		%{expand: %%global build_pvm 0}}
%{?_with_pvm:			%{expand: %%global build_pvm 1}}
%define build_dv 1
%define build_freetype 1
%define build_quicktime 1
%define build_theora 1
%define build_faac 0

%global optflags %{optflags} -Ofast

Name:		transcode
Version:	1.1.7
Release:	1
Summary:	A linux video stream processing utility
License: 	GPLv2+
Group: 		Video/Editors and Converters
Url:		https://bitbucket.org/france/transcode-tcforge/
Source0:	https://bitbucket.org/france/transcode-tcforge/downloads/%{name}-%{version}.tar.bz2
Patch0:		transcode-1.1.7-ffmpeg.patch
Patch1:		transcode-1.1.7-ffmpeg-0.10.patch
Patch2:		transcode-1.1.7-ffmpeg-0.11.patch
Patch3:		transcode-1.1.7-preset-free.patch
Patch4:		transcode-1.1.7-libav-9.patch
Patch5:		transcode-1.1.7-libav-10.patch
Patch6:		transcode-1.1.7-preset-force.patch
Patch7:		transcode-1.1.7-ffmpeg2.patch
Patch8:		transcode-1.1.7-freetype.patch
Patch9:		transcode-1.1.7-ffmpeg2.4.patch
Patch10:	transcode-1.1.7-ffmpeg29.patch
Patch11:	transcode-ffmpeg3.patch
Patch12:	transcode-1.1.7-imagemagick7.patch
Patch13:	transcode-1.1.7-ffmpeg4.patch
Patch14:	transcode-1.1.7-disable-tests-that-dont-compile.patch

BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	ffmpeg-devel >= 0.4.9
%if %build_dv
BuildRequires:	pkgconfig(libdv) >= 0.99
%endif
BuildRequires:	pkgconfig(dvdread)
%if %build_freetype
BuildRequires:	pkgconfig(freetype2)
%endif
BuildRequires:	xvid-devel
BuildRequires:	lame-devel
BuildRequires:	a52dec-devel
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	netpbm-devel
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(x264)
BuildRequires:	pkgconfig(mjpegtools)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(libmpeg2)
%if %build_faac
BuildRequires:	libfaac-devel
%endif
%if %build_quicktime
BuildRequires:	pkgconfig(libquicktime) >= 0.9.3
%endif
%if %build_theora
BuildRequires:	pkgconfig(theora)
%endif
%if %build_pvm
BuildRequires:	libpvm-devel >= 3.4
%endif
BuildRequires:	atomic-devel
#gw these are requirements of the plf version of libMagick-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	jbig-devel

%description
transcode is a text-console video stream processing
tool. Decoding and encoding is done by loading shared library modules
that are responsible for feeding transcode with raw RGB/PCM streams
(import module) and encoding the frames (export module). It supports
elementary video and audio frame transformations.
Some example modules are included to enable import
of MPEG program streams (VOB), Digital Video (DV), or YUV video
and export modules for writing DivX;-), OpenDivX, or uncompressed AVI files.
A set of tools is available to extract and decode the sources into
raw video/audio streams for import and to enable post-processing of AVI files.

This package is in tainted as it could violate some patents.

%prep
%setup
%apply_patches

%build
autoreconf -vfi
%ifarch %ix86
export CPPFLAGS="$CPPFLAGS -mmmx"
%endif
%configure \
	--enable-libmpeg2 \
	--enable-libmpeg2convert \
	--enable-a52-default-decoder \
	--with-default-xvid=xvid4 \
%if %build_dv
	--enable-libdv \
%endif
%if %build_pvm
	--with-pvm3-lib=%{_datadir}/pvm3/lib/LINUX/ \
%else
	--disable-pvm3 \
%endif
	--enable-imagemagick \
	--enable-mjpegtools \
	--enable-netstream \
	--enable-ogg \
	--enable-vorbis \
%if %build_theora
	--enable-theora \
%endif
%if %build_quicktime
	--enable-libquicktime \
%endif
	--enable-lzo --with-lzo-includes=%{_includedir}/lzo \
	--enable-libxml2 \
	--enable-a52 \
	--enable-sdl \
	--enable-v4l \
	--enable-libv4l2 \
	--enable-libv4lconvert \
	--enable-libfame \
	--enable-oss \
	--enable-alsa \
	--enable-libpostproc \
%if %{build_faac}
	--enable-faac \
%endif
	--enable-deprecated \
%if %build_freetype
	--enable-freetype2 \
%else
	--disable-freetype2 \
%endif
	--enable-xvid \
	--enable-x264

%make_build

%install
%make_install transform=""

for file in `find %{buildroot} -name "*.la"`; do
	perl -pi -e 's|'%{buildroot}'/%{name}-%{version}/||g' $file
done
mv %{buildroot}%{_datadir}/doc/transcode installed-docs

%files
%doc installed-docs/*
%{_bindir}/transcode
%{_bindir}/tccat
%{_bindir}/aviindex
%{_bindir}/avimerge
%{_bindir}/avisplit
%{_bindir}/tcdemux
%{_bindir}/tcprobe
%{_bindir}/avifix
%{_bindir}/tcscan
%{_bindir}/tcextract
%{_bindir}/avisync
%{_bindir}/tcdecode
%{_bindir}/tcmodinfo
%{_bindir}/tcxmlcheck
%{_bindir}/tcxpm2rgb
%{_bindir}/tcmp3cut
%{_bindir}/tcrequant
%if %build_pvm
%{_bindir}/tcpvmexportd
%endif
%{_bindir}/tcyait
%{_libdir}/%{name}
%{_mandir}/man1/*
