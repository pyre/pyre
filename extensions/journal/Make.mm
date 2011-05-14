# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = journal
PACKAGE = 
MODULE = journal

PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)

include std-pythonmodule.def

EXTERNAL_LIBS += -ljournal

PROJ_SRCS = \
    DefaultDevice.cc \
    exceptions.cc \
    channels.cc \
    init.cc \
    metadata.cc

# end of file
