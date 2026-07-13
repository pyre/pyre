# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the docker images; each one is configured in its own {.mm/pyre.<instance>} file
pyre.docker-images := \
    pyre.lts-clang \
    pyre.lts-gcc \
    pyre.rolling-clang \
    pyre.rolling-gcc


# pull in the per-instance configuration
include $(pyre.docker-images)


# end of file
