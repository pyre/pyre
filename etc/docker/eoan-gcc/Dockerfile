## -*- docker-image-name: "pyre:eoan-gcc" -*-

# based on ubuntu
FROM ubuntu:eoan

# set up some build variables
# python version
ARG python_version=3.7
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
# export the python choide
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
        git vim \
        g++ gfortran make \
        ${python} ${python}-dev \
        python3-pybind11 \
        libopenmpi-dev \
        libgsl-dev


# setup the interactive environment
# go home
WORKDIR /root
# copy the file
COPY etc/docker/eoan-gcc/bashrc bashrc.in
# expand
RUN sed -e "s:@SRCDIR@:${srcdir}:g" bashrc.in > .bashrc

# place the {mm} configuration file
# make the pyre configuration directory
WORKDIR /root/.pyre
# copy the {mm} coniguration file here
COPY etc/docker/eoan-gcc/mm.pfg mm.pfg.in
# expand; the '/' after ${prefix} is necessary for complying with the mm convention of
# terminating slashes on all directories
RUN sed \
        -e "s:@PREFIX@:${prefix}:g" \
        mm.pfg.in > mm.pfg

# place the {mm} control file
WORKDIR /root/.mm
# copy the relevant configuration file
COPY etc/docker/eoan-gcc/config.mm config.mm.in
# expand
RUN sed \
        -e "s:@PYTHON_VERSION@:${python_version}:g" \
        -e "s:@PYTHON_MODEL@:m:g" \
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

# install the python packages
RUN \
        ln -s ${prefix}/packages/pyre ${prefix}/lib/${python}/dist-packages; \
        ln -s ${prefix}/packages/journal ${prefix}/lib/${python}/dist-packages; \
        ln -s ${prefix}/packages/mpi ${prefix}/lib/${python}/dist-packages; \
        ln -s ${prefix}/packages/gsl ${prefix}/lib/${python}/dist-packages

# and test
# RUN ${mm} tests


# end of file
