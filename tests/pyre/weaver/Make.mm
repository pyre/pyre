# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

working: weaver

all: test

test: sanity weaver

sanity:
	${PYTHON} ./sanity.py

weaver:
	${PYTHON} ./weaver.py

# end of file 
