# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-data
targets.openmp.description := compiling and linking with OpenMP enabled

# initialize
${eval ${call target.init,openmp}}

# adjust: the OpenMP switch belongs on both the compile and the link command lines, so that
# the compiler enables the {_OPENMP} guard and the driver pulls in the OpenMP runtime
${call target.adjust,openmp,$(languages.compiled),flags ldflags}

# build my info target
${eval ${call target.info.flags,openmp}}


# end of file
