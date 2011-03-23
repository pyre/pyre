# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

working:
	${PYTHON} ./merlin-shell.py

all: test

test: sanity merlin

sanity:
	${PYTHON} ./sanity.py

merlin:
	${PYTHON} ./merlin-shell.py


# end of file 
