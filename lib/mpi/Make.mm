# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = mpi

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_SAR = $(BLD_LIBDIR)/lib$(PROJECT)-$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PROJECT)-$(PACKAGE).$(EXT_SO)

PROJ_SRCS = \
    Error.cc \
    Communicator.cc \
    Group.cc \


#--------------------------------------------------------------------------
#

all: $(PROJ_DLL) export

export:: export-headers export-package-headers


EXPORT_HEADERS = \
    mpi.h \

EXPORT_PKG_HEADERS = \
    Communicator.h Communicator.icc \
    Error.h Error.icc \
    Group.h Group.icc \


# end of file 
