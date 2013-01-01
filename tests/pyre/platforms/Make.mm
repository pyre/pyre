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

test: sanity host

sanity:
	${PYTHON} ./sanity.py

host:
	${PYTHON} ./host.py


# end of file 
