# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test clean

test: sanity weaver documents

sanity:
	${PYTHON} ./sanity.py

weaver:
	${PYTHON} ./weaver.py

documents:
	${PYTHON} ./document_c.py
	${PYTHON} ./document_cpp.py

# end of file 
