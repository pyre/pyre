# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = gauss.pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity config

sanity:
	${PYTHON} ./sanity.py

config:
	${PYTHON} ./pi.py
	${PYTHON} ./gaussian.py


# end of file 
