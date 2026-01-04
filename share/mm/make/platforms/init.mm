# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# platform id; by default, these match what is known about the host
platform.os := $(host.os)
platform.arch := $(host.arch)
# assemble the platform id
platform := $(platform.os)-$(platform.arch)

# default compilers
platform.compilers ?=

# pull the plaform/architecture specific settings
include make/platforms/$(host.os)/$(host.arch).mm


# end of file
