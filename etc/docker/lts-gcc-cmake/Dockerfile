## -*- docker-image-name: "pyre:lts-gcc-cmake" -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the current ubuntu LTS; the official tag is multi-arch, so it resolves to the host
# architecture with no emulation
FROM ubuntu:latest

# set up some build variables
# the image instance; drives every {COPY} path below so a sibling image is a pure copy-and-edit
ARG instance=lts-gcc-cmake
# locations
ARG prefix=/usr/local
ARG srcdir=${prefix}/src
# the build directory; cmake configures here and installs into {installdir}
ARG builddir=/tmp/build
ARG installdir=/tmp/install
# the compilers cmake should drive
ARG cc=gcc
ARG cxx=g++
# where the apt {python3-pybind11} package drops its cmake config
ARG pybind11_dir=/usr/lib/python3/dist-packages/pybind11/share/cmake/pybind11

# environment
# colorize (for fun)
ENV TERM=xterm-256color
# set up the dynamic linker path so the freshly installed libraries are found at test time
ENV LD_LIBRARY_PATH=${installdir}/lib


# update the package repository
RUN apt update -y
# get the latest
RUN apt dist-upgrade -y

# install the base software stack
#  - {vim} is for interactive use
#  - {openssh}, {zip}, {unzip} are needed for some of the tests
#  - {cmake} drives the build; {gcc}/{g++}/{gfortran} are the toolchain
#  - {libhdf5-dev} is the serial hdf5
#  - {libopenmpi-dev}, {libgsl-dev}, and {libpq-dev} bring in the optional packages pyre has
#    support for, so their libraries, bindings, and tests get built
#  - {postgresql} is the server the postgres tests talk to
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        curl git vim zip unzip \
        openssh-server \
        cmake \
        gcc g++ gfortran make \
        python3 python3-dev \
        python3-pybind11 python3-yaml python3-numpy \
        libopenmpi-dev libhdf5-dev libgsl-dev libpq-dev \
        postgresql


# the postgres server: the package creates a cluster; start it once to give {root}, the user the
# tests run as, a role that can create and drop the databases the tests use
RUN service postgresql start && \
        su postgres -c "createuser --superuser root" && \
        service postgresql stop

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

# let openmpi launch as root
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# stash the cmake settings so the {CMD} recipe stays legible
# the compilers, the install prefix, and the pybind11 cmake config location
ENV CC=${cc}
ENV CXX=${cxx}
ENV BUILDDIR=${builddir}
ENV INSTALLDIR=${installdir}
ENV PYBIND11_DIR=${pybind11_dir}

# go to the source directory; {pyre} is bind-mounted here at run time
WORKDIR ${srcdir}/pyre
# start the postgres server, configure with cmake, build and install, then run the test suite;
# make runs one job per core, since cmake's makefiles offer every object of every target at once,
# and an unbounded {-j} starts enough compilers to run out of memory
CMD service ssh start && service postgresql start && \
        mkdir -p ${BUILDDIR} && cd ${BUILDDIR} && \
        cmake \
            -DCMAKE_INSTALL_PREFIX=${INSTALLDIR} \
            -DCMAKE_BUILD_TYPE=Debug \
            -DCMAKE_C_COMPILER=${CC} \
            -DCMAKE_CXX_COMPILER=${CXX} \
            -Dpybind11_DIR=${PYBIND11_DIR} \
            -DPYRE_MPI_OVERSUBSCRIBE=ON \
            /usr/local/src/pyre && \
        make -j$(nproc) install && \
        ctest --output-on-failure


# end of file
