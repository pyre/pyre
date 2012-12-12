# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = pyre
PACKAGE = extensions
MODULE = host

include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PACKAGE)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)

PROJ_SRCS = \
    cpu.cc \
    metadata.cc

# end of file
