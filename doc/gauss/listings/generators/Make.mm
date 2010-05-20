# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

PROJECT = pyre
PACKAGE = doc/gauss/generators

#--------------------------------------------------------------------------
#

all: tidy

test:
	${PYTHON} ./gauss.py

# end of file
