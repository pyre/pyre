## -*- docker-image-name: "pyre:hirsute-gcc-cmake" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# based on ubuntu
FROM ubuntu:hirsute

# set up some build variables
# locations
ARG prefix=/usr/local
ARG srcdir=${prefix}/src

# environment
# colorize (for fun)
ENV TERM=xterm-256color
# set up the dynamic linker path
ENV LD_LIBRARY_PATH=${prefix}/lib


# update the package repository
RUN apt update -y
# get the latest
RUN apt dist-upgrade -y

# install the base software stack
#  - {vim} is for interactive use
#  - {openssh}, {zip}, {unzip} are needed for some of the tests
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        git vim unzip zip \
        openssh-server \
        g++ gfortran make cmake \
        python3 python3-dev \
        python3-distutils python3-numpy python3-pybind11 python3-yaml \
        libopenmpi-dev \
        libgsl-dev


# setup the interactive environment
# go home
WORKDIR /root
# copy the files with support for interactive use
COPY etc/docker/hirsute-gcc-cmake/inputrc .inputrc
# the startup file
COPY etc/docker/hirsute-gcc-cmake/bashrc bashrc.in
# expand
RUN sed \
        -e "s:@SRCDIR@:${srcdir}:g" \
        bashrc.in > .bashrc

# make the pyre configuration directory
WORKDIR /root/.pyre
# the mpi configuration
COPY etc/docker/hirsute-gcc-cmake/mpi.pfg mpi.pfg


# make the development area
WORKDIR ${srcdir}
# pull pyre
COPY . pyre

# go to the {pyre} top level directory
WORKDIR /tmp/builds/pyre
# configure
RUN cmake \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DMPIEXEC_PREFLAGS=--allow-run-as-root \
        /usr/local/src/pyre
# build
RUN make -j 16 install

# and test
CMD service ssh start && ctest --verbose


# end of file
