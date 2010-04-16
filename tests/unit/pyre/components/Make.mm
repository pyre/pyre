# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity metaclasses

sanity:
	${PYTHON} ./sanity.py

metaclasses:
	${PYTHON} ./requirement.py


# end of file 
