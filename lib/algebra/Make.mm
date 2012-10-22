# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = pyre
PACKAGE = algebra

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)

#
all: export

export:: export-package-headers

release:: release-package-headers

EXPORT_PKG_HEADERS = \
    operators.h operators.icc \
    BCD.h BCD.icc

# end of file 
