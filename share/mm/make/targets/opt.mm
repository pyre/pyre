# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# meta-data
targets.opt.description := optimized build

# initialize
${eval ${call target.init,opt}}

# adjust
${call target.adjust,opt,$(languages.compiled),flags}

# build my info target
${eval ${call target.info.flags,opt}}


# end of file
