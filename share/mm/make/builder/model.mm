# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# instantiate the builder
# we need project.bldroot and target.variants to have their final value by now....
${eval ${call builder.init,$(project.prefix),$(project.bldroot)}}

# make the builder targets
${eval ${call builder.workflows}}


# end of file
