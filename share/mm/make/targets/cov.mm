# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-data
targets.cov.description := compiling with coverage information

# initialize
${eval ${call target.init,cov}}

# adjust
${call target.adjust,cov,$(languages.compiled),flags ldflags}

# build my info target
${eval ${call target.info.flags,cov}}


# end of file
