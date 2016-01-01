# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
include pyre.def
# the package name
PACKAGE = algebra
# the package headers
EXPORT_PKG_HEADERS = \
    operators.h operators.icc \
    BCD.h BCD.icc

# standard targets
all: export

export:: export-package-headers

live: live-package-headers

# end of file
