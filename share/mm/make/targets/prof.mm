# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# meta-data
targets.prof.description := compiling with profiling support

# initialize
${eval ${call target.init,prof}}

# adjust
${call target.adjust,prof,$(languages.compiled),flags ldflags}

# build my info target
${eval ${call target.info.flags,prof}}


# end of file
