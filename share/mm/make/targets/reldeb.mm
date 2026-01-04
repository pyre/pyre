# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-data
targets.reldeb.description := compiling with support for debugging

# initialize
${eval ${call target.init,reldeb}}

# adjust
${call target.adjust,reldeb,$(languages.compiled),flags ldflags}
# define the DEBUG macro
${foreach language,c c++ cuda cython fortran, \
    ${eval targets.reldeb.$(language).defines += DEBUG} \
}

# build my info target
${eval ${call target.info.flags,reldeb}}


# end of file
