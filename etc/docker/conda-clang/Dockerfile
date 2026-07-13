## -*- docker-image-name: "pyre:conda-clang" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# a plain ubuntu base; the conda-forge toolchain is distro-independent
FROM ubuntu:24.04

# set up some build variables
# the image instance; drives every {COPY} path below so a sibling image is a pure copy-and-edit
ARG instance=conda-clang
# the conda environment name; must not be a {.mm} project name like {pyre}
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

# where mm's conda pkgdb finds the conda agent
ENV MAMBA_EXE=/root/.local/bin/micromamba
ENV MAMBA_ROOT_PREFIX=/root/.local

# run the CMD under bash for the micromamba shell hook
SHELL ["/bin/bash", "-c"]

# activate the environment, discover packages, build, and test the mounted working tree
CMD service ssh start && \
    eval "$(/root/.local/bin/micromamba shell hook --shell bash /root/.local)" && \
    micromamba activate pyre-dev && \
    ${MM} --setup && ${MM} --jobs=2 && ${MM} --jobs=2 tests


# end of file
