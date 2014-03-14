# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = extensions
MODULE = cuda

include cuda/default.def
include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)/$(MODULE)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
PROJ_LIBRARIES = -ljournal

PROJ_SRCS = \
    discover.cc \
    exceptions.cc \
    metadata.cc

# end of file
