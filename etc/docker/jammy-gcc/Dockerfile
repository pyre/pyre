## -*- docker-image-name: "pyre:jammy-gcc" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# based on ubuntu
FROM ubuntu:jammy

# set up some build variables
# python version
ARG python_version=3.10
ARG python=python${python_version}
# locations
ARG prefix=/usr/local
ARG srcdir=${prefix}/src
# the build system
ARG mm="${python} ${srcdir}/mm/mm.py"

# environment
# colorize (for fun)
ENV TERM=xterm-256color
# set up the dynamic linker path
ENV LD_LIBRARY_PATH=${prefix}/lib
# export the python choice
ENV PYTHON=${python}
# and the path to {mm}
ENV MM=${mm}


# update the package repository
RUN apt update -y
# get the latest
RUN apt dist-upgrade -y

# install the base software stack
#  - {vim} is for interactive use
#  - {openssh}, {zip}, {unzip} are needed for some of the tests
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        git vim zip unzip \
        openssh-server \
        g++ gfortran make \
        ${python} ${python}-dev \
        python3-pybind11 python3-yaml python3-numpy \
        libopenmpi-dev libhdf5-openmpi-dev libgsl-dev


# setup the interactive environment
# go home
WORKDIR /root
# copy the files with support for interactive use
COPY etc/docker/jammy-gcc/inputrc .inputrc
# the startup file
COPY etc/docker/jammy-gcc/bashrc bashrc.in
# expand
RUN sed \
        -e "s:@SRCDIR@:${srcdir}:g" \
        bashrc.in > .bashrc

# make the pyre configuration directory
WORKDIR /root/.pyre
# the mpi configuration
COPY etc/docker/jammy-gcc/mpi.pfg mpi.pfg
# the {mm} configuration file
COPY etc/docker/jammy-gcc/mm.pfg mm.pfg.in
# expand
RUN sed \
        -e "s:@PREFIX@:${prefix}:g" \
        mm.pfg.in > mm.pfg

# place the {mm} control file
WORKDIR /root/.mm
# copy the relevant configuration file
COPY etc/docker/jammy-gcc/config.mm config.mm.in
# expand
RUN sed \
        -e "s:@PYTHON_VERSION@:${python_version}:g" \
        config.mm.in > config.mm


# make the development area
WORKDIR ${srcdir}
# pull mm
RUN git clone https://github.com/aivazis/mm.git
# pull pyre
COPY . pyre

# go to the {pyre} top level directory
WORKDIR ${srcdir}/pyre
# build
RUN ${mm}
# show me the build context
RUN ${mm} --serial host.info builder.info compilers.info

# and test
CMD service ssh start && ${MM} tests


# end of file
