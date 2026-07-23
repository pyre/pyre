# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-data
targets.debug.description := compiling with support for debugging

# initialize
${eval ${call target.init,debug}}

# adjust
${call target.adjust,debug,$(languages.compiled),flags ldflags}

# build my info target
${eval ${call target.info.flags,debug}}


# end of file
