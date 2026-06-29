# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the registry of known toolchains
toolchains := playwright docker

# load each tool's definition
include ${foreach tool,$(toolchains),$(toolchains.mm)/$(tool)/$(tool).mm}

# fill in defaults and resolve installation locations
${foreach tool,$(toolchains),${eval ${call toolchain.init,$(tool)}}}

# build the universal recipes for each tool
${foreach tool,$(toolchains),${eval ${call toolchain.workflows,$(tool)}}}


# end of file
