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

test: sanity formats

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./manager.py

formats: pml

pml:
	${PYTHON} ./pml.py
	${PYTHON} ./pml_empty.py
	${PYTHON} ./pml_sample.py

# end of file 
