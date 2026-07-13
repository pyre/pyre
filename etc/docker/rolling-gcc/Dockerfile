## -*- docker-image-name: "pyre:rolling-gcc" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# the latest ubuntu release; the official {rolling} tag is multi-arch, so it resolves to the host
# architecture with no emulation, and ships GNU make >= 4.4 so no make-from-source is needed
FROM ubuntu:rolling

# set up some build variables
# the image instance; drives every {COPY} path below so a sibling image is a pure copy-and-edit
ARG instance=rolling-gcc
# locations
ARG prefix=/usr/local
ARG srcdir=${prefix}/src
# the build system; {mm} and {pyre} are bind-mounted under {srcdir} at run time, not baked in
ARG mm="python3 ${srcdir}/mm/mm"

# environment
# colorize (for fun)
ENV TERM=xterm-256color
# set up the dynamic linker path
ENV LD_LIBRARY_PATH=${prefix}/lib
# and the path to {mm}
ENV MM=${mm}


# update the package repository
RUN apt update -y
# get the latest
RUN apt dist-upgrade -y

# install the base software stack
#  - {vim} is for interactive use
#  - {openssh}, {zip}, {unzip} are needed for some of the tests
#  - {gcc}/{g++}/{gfortran} are the toolchain; {libhdf5-dev} is the serial hdf5 the dpkg packager
#    registers under the canonical {hdf5} name (the {-openmpi} variant registers as {hdf5-openmpi})
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        git vim zip unzip \
        openssh-server \
        gcc g++ gfortran make \
        python3 python3-dev \
        python3-pybind11 python3-yaml python3-numpy \
        libopenmpi-dev libhdf5-dev libgsl-dev


# setup the interactive environment
# go home
WORKDIR /root
# copy the readline configuration
COPY etc/docker/${instance}/inputrc .inputrc
# the shell startup file
COPY etc/docker/${instance}/bashrc bashrc.in
# expand the source location
RUN sed -e "s:@SRCDIR@:${srcdir}:g" bashrc.in > .bashrc
# clean up
RUN rm bashrc.in

# the prompt generator
COPY etc/docker/${instance}/prompt.py prompt.py.in
# expand the instance name
RUN sed -e "s:@INSTANCE@:${instance}:g" prompt.py.in > prompt.py
# clean up
RUN rm prompt.py.in

# make the pyre configuration directory
WORKDIR /root/.pyre
# the {mm} configuration file
COPY etc/docker/${instance}/mm.yaml mm.yaml

# place the {mm} control file
WORKDIR /root/.mm
# the package location overrides, if any
COPY etc/docker/${instance}/config.mm config.mm

# openmpi refuses to launch as root by default; this container runs as root, so sanction it for
# every launcher — the make-level {mpi.executive} and pyre's mpi shell alike — with openmpi's own
# environment override, which any {mpiexec} it spawns will honor. placed late so it does not bust
# the cache of the expensive apt layers above
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# go to the source directory; {mm} and {pyre} are bind-mounted here at run time
WORKDIR ${srcdir}/pyre
# discover the system packages, build, and test the mounted working tree; {--jobs=2} caps the
# parallelism so the memory-heavy {pyre::grid} binding template expansions do not exhaust RAM,
# matching the CI containers
CMD service ssh start && ${MM} --setup && ${MM} --jobs=2 && ${MM} --jobs=2 tests


# end of file
