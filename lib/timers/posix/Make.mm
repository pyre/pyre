# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = timers/posix

all: export

export:: export-package-headers

release:: release-package-headers


EXPORT_PKG_HEADERS = \
    Clock.h Clock.icc

# end of file 
