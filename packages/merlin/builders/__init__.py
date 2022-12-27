# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# N.B.: function foundries don't work here, unless they are named something other the names
#   of the local subdirectories: they get overwritten by their embedded import statement that makes
#   global assignment


# builder foundries
# the native flow builder
from .flow.Builder import Builder as flow
# the makefile generator
from .make.Builder import Builder as make


# end of file
