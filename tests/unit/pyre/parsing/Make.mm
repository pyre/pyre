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

test: sanity lexing

sanity:
	${PYTHON} ./sanity.py

lexing:
	${PYTHON} ./scanner.py
	${PYTHON} ./lexing.py
	${PYTHON} ./lexing-tokenizationError.py

# end of file 
