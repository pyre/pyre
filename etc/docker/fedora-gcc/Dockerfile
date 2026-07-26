## -*- docker-image-name: "pyre:fedora-gcc" -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# the current fedora release: a modern rpm/dnf instance; the official tag is multi-arch, so
# it resolves to the host architecture with no emulation
FROM fedora:latest

# set up some build variables
# the image instance; drives every {COPY} path below so a sibling image is a pure copy-and-edit
ARG instance=fedora-gcc
# locations
ARG prefix=/usr/local
ARG srcdir=${prefix}/src
# the build system; {mm} and {pyre} are bind-mounted under {srcdir} at run time, not baked in
ARG mm="python3 ${srcdir}/mm/mm"

# environment
# colorize (for fun)
ENV TERM=xterm-256color
# fedora activates mpi through environment modules; bake the openmpi layout in instead
ENV PATH=/usr/lib64/openmpi/bin:${PATH}
# set up the dynamic linker path, including the openmpi home
ENV LD_LIBRARY_PATH=${prefix}/lib:/usr/lib64/openmpi/lib
# and the path to {mm}
ENV MM=${mm}


# get the latest
RUN dnf -y upgrade

# install the base software stack
#  - {vim} is for interactive use
#  - {openssh}, {zip}, {unzip} are needed for some of the tests
#  - {gcc}/{gcc-c++}/{gcc-gfortran} are the toolchain
#  - the {-devel} packages are the externals the rpm engine will be asked to discover
RUN dnf -y install \
        git vim zip unzip \
        openssh-server passwd \
        gcc gcc-c++ gcc-gfortran make \
        python3 python3-devel \
        pybind11-devel python3-pyyaml python3-numpy \
        openmpi-devel hdf5-devel gsl-devel


# allow passwordless {ssh localhost} as root
RUN ssh-keygen -A && \
        mkdir -p -m 700 /root/.ssh && \
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
# the package location overrides
COPY etc/docker/${instance}/config.mm config.mm

# let openmpi launch as root
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# go to the source directory; {mm} and {pyre} are bind-mounted here at run time
WORKDIR ${srcdir}/pyre
# discover packages, build, and test the mounted working tree
CMD /usr/sbin/sshd && ${MM} --setup && ${MM} --jobs=2 && ${MM} --jobs=2 tests


# end of file
