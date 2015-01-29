# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = patterns
# headers that are scoped by the package name
EXPORT_PKG_HEADERS = \
    Registrar.h Registrar.icc

# the standard targets
all: export

export:: export-package-headers

live: live-package-headers

# end of file
