# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-data
targets.shared.description := building relocatable symbols suitable for a shared library

# initialize
${eval ${call target.init,shared}}

# adjust
${call target.adjust,shared,$(languages.compiled),flags ldflags}

# build my info target
${eval ${call target.info.flags,shared}}


# end of file
