# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# get mpi
include MPI/default.def
# the project defaults
include pyre.def
# the package name
PACKAGE = mpi
# top level header
EXPORT_HEADERS = \
    mpi.h \
# headers scoped by the package name
EXPORT_PKG_HEADERS = \
    Communicator.h Communicator.icc \
    Error.h Error.icc \
    Group.h Group.icc \
    Handle.h Handle.icc \
    Shareable.h Shareable.icc \

# standard targets
all: export

export:: export-headers export-package-headers

live: live-headers live-package-headers

# end of file
