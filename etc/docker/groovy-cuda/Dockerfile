## -*- docker-image-name: "pyre:groovy-cuda" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# based on ubuntu
FROM ubuntu:groovy

# set up some build variables
ARG instance=groovy-cuda
# python version
ARG python_version=3.8
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
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        git vim unzip zip \
        g++ gfortran make \
        npm \
        fftw3-dev \
        libgsl-dev \
        libpq-dev \
        libopenmpi-dev \
        nvidia-cuda-toolkit \
        ${python} ${python}-dev \
        python3-pybind11 python3-yaml python3-numpy


# setup the interactive environment
# go home
WORKDIR /root
# copy the files with support for interactive use
COPY etc/docker/${instance}/inputrc .inputrc
# the startup file
COPY etc/docker/${instance}/bashrc bashrc.in
# expand
RUN sed \
        -e "s:@SRCDIR@:${srcdir}:g" \
        bashrc.in > .bashrc
# copy the prompt
COPY etc/docker/${instance}/prompt.py prompt.py.in
# expand
RUN sed \
        -e "s:@INSTANCE@:${instance}:g" \
        prompt.py.in > prompt.py


# make the pyre configuration directory
WORKDIR /root/.pyre
# the mpi configuration
COPY etc/docker/${instance}/mpi.pfg mpi.pfg
# the {mm} coniguration file
COPY etc/docker/${instance}/mm.pfg mm.pfg.in
# expand
RUN sed \
        -e "s:@PREFIX@:${prefix}:g" \
        mm.pfg.in > mm.pfg

# place the {mm} control file
WORKDIR /root/.mm
# copy the relevant configuration file
COPY etc/docker/${instance}/config.mm config.mm.in
# expand
RUN sed \
        -e "s:@PYTHON_VERSION@:${python_version}:g" \
        config.mm.in > config.mm

# go to the source directory
WORKDIR /usr/local/src


# end of file
