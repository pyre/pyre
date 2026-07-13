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
#  - {gcc}/{g++}/{gfortran} are the toolchain; {libhdf5-dev} is the serial hdf5
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        git vim zip unzip \
        openssh-server \
        gcc g++ gfortran make \
        python3 python3-dev \
        python3-pybind11 python3-yaml python3-numpy \
        libopenmpi-dev libhdf5-dev libgsl-dev


# allow passwordless {ssh localhost} as root
RUN mkdir -p -m 700 /root/.ssh && \
        ssh-keygen -q -t ed25519 -N "" -f /root/.ssh/id_ed25519 && \
        cp /root/.ssh/id_ed25519.pub /root/.ssh/authorized_keys && \
        chmod 600 /root/.ssh/authorized_keys && \
        printf 'Host localhost\n    StrictHostKeyChecking no\n    UserKnownHostsFile /dev/null\n    LogLevel ERROR\n' \
            > /root/.ssh/config && \
        chmod 600 /root/.ssh/config && \
        echo 'PermitRootLogin prohibit-password' > /etc/ssh/sshd_config.d/00-root-login.conf


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

# let openmpi launch as root
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# go to the source directory; {mm} and {pyre} are bind-mounted here at run time
WORKDIR ${srcdir}/pyre
# discover packages, build, and test the mounted working tree
CMD service ssh start && ${MM} --setup && ${MM} --jobs=2 && ${MM} --jobs=2 tests


# end of file
