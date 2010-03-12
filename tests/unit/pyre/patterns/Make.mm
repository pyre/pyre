# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity utils patterns

sanity:
	${PYTHON} ./sanity.py

utils:
	${PYTHON} ./powerset.py

patterns:
	${PYTHON} ./extent.py
	${PYTHON} ./named.py
	${PYTHON} ./observable.py


# end of file 
