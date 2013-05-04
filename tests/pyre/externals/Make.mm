# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity manager applications

sanity:
	${PYTHON} ./sanity.py

manager:
	${PYTHON} ./locate.py

applications:
	${PYTHON} ./simple.py


# end of file 
