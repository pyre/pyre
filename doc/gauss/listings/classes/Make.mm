# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = pyre
PACKAGE = doc/gauss/classes

#--------------------------------------------------------------------------
#

all: tidy

test:
	${PYTHON} ./gauss.py

# end of file
