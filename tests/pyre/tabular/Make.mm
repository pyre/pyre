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

test: sanity sheets

sanity:
	${PYTHON} ./sanity.py

sheets:
	${PYTHON} ./sheet.py

# end of file 
