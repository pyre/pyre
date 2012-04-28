# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

include MPI/default.def

PROJECT = pyre
PACKAGE = mpi

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)

#--------------------------------------------------------------------------
#

all: export

export:: export-headers export-package-headers


EXPORT_HEADERS = \
    mpi.h \

EXPORT_PKG_HEADERS = \
    Communicator.h Communicator.icc \
    Error.h Error.icc \
    Group.h Group.icc \
    Handle.h Handle.icc \
    Shareable.h Shareable.icc \


# end of file 
