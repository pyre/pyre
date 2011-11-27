# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity types

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

types:
	${PYTHON} ./arry.py
	${PYTHON} ./boolean.py
	${PYTHON} ./date.py
	${PYTHON} ./dimensional.py
	${PYTHON} ./dtime.py
	${PYTHON} ./float.py
	${PYTHON} ./inet.py
	${PYTHON} ./int.py
	${PYTHON} ./numeric.py
	${PYTHON} ./str.py


# end of file 
