# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

include clock/default.def

PROJECT = pyre
PACKAGE = timers
MODULE = timers

include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)module
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
PROJ_CXX_SRCLIB += -lpyre-timers

PROJ_SRCS = \
    display.cc \
    metadata.cc

# end of file
