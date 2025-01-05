# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# meta-data
targets.debug.description := compiling with support for debugging

# initialize
${eval ${call target.init,debug}}

# adjust
${call target.adjust,debug,$(languages.compiled),flags ldflags}
# define the DEBUG macro
${foreach language,c c++ cuda cython fortran, \
    ${eval targets.debug.$(language).defines += DEBUG} \
}

# build my info target
${eval ${call target.info.flags,debug}}


# end of file
