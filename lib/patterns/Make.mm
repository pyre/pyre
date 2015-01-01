# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

PROJECT = pyre
PACKAGE = patterns

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)

#
all: export

export:: export-package-headers

release:: release-package-headers

EXPORT_PKG_HEADERS = \
    Registrar.h Registrar.icc

# end of file
