# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = journal
PACKAGE = 
MODULE = journal

include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
PROJ_LIBRARIES = -ljournal

PROJ_SRCS = \
    DeviceProxy.cc \
    exceptions.cc \
    channels.cc \
    init.cc \
    metadata.cc \
    tests.cc \

# end of file
