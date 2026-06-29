# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the baseline shared by every mode
include make/modes/default.mm
# the selected mode's overrides; a mode with no file here is a fatal error
include make/modes/$(project.mode).mm

# the implemented modes, discovered from the files present here, minus the framework files
modes.available := ${filter-out init default rules model,${basename ${notdir ${wildcard $(mm.home)/make/modes/*.mm}}}}


# end of file
