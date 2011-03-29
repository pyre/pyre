# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity application

sanity:
	${PYTHON} ./sanity.py

application:
	${PYTHON} ./application-sanity.py

# end of file 
