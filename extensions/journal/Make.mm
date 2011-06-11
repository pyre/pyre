# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = journal
PACKAGE = 
MODULE = journal

include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
EXTERNAL_LIBS += -ljournal

PROJ_SRCS = \
    DeviceProxy.cc \
    exceptions.cc \
    channels.cc \
    init.cc \
    metadata.cc \
    tests.cc \

# end of file
