## -*- docker-image-name: "pyre:conda-gcc" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# a plain ubuntu base; with a conda-forge toolchain the host distro is irrelevant, so the LTS is
# fine and the {ubuntu:24.04} tag is multi-arch, resolving to the host architecture with no emulation
FROM ubuntu:24.04

# set up some build variables
# the image instance; drives every {COPY} path below so a sibling image is a pure copy-and-edit
ARG instance=conda-gcc
# the conda environment name; must NOT collide with a {.mm} project name (e.g. {pyre}); kept in sync
# with the {name:} in {pyre-env.yaml} and the {micromamba activate} in the CMD below
ARG env=pyre-dev
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

# install just enough to fetch micromamba and support interactive use and the ssh-launched tests
RUN DEBIAN_FRONTEND=noninteractive \
        apt install -y \
        curl git vim zip unzip openssh-server

# install micromamba
WORKDIR /root/.local
# make the bin directory
RUN mkdir -p bin
# fetch the latest micromamba for the host architecture
RUN curl "https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-linux-$(uname -m)" -o bin/micromamba -fsSL --compressed
# make it executable
RUN chmod +x bin/micromamba
# copy the environment specification
COPY etc/docker/${instance}/pyre-env.yaml pyre-env.yaml
# create the pyre build environment from conda-forge
RUN /root/.local/bin/micromamba env create --quiet --yes --file pyre-env.yaml --prefix=/root/.local/envs/${env}


# setup the interactive environment
# go home
WORKDIR /root
# copy the readline configuration
COPY etc/docker/${instance}/inputrc .inputrc
# the shell startup file
COPY etc/docker/${instance}/bashrc bashrc.in
# expand the source location and the environment name
RUN sed -e "s:@SRCDIR@:${srcdir}:g" -e "s:@ENV@:${env}:g" bashrc.in > .bashrc
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

# go to the source directory; {mm} and {pyre} are bind-mounted here at run time
WORKDIR ${srcdir}/pyre
# activate the conda environment, discover the conda packages, build, and test the mounted working
# tree; {--jobs=2} caps the parallelism so the memory-heavy {pyre::grid} binding template expansions
# do not exhaust RAM, matching the CI containers
CMD service ssh start && \
    eval "$(/root/.local/bin/micromamba shell hook --shell bash /root/.local)" && \
    micromamba activate pyre-dev && \
    ${MM} --setup && ${MM} --jobs=2 && ${MM} --jobs=2 tests


# end of file
