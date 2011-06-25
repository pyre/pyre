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

test: sanity tables

sanity:
	${PYTHON} ./sanity.py

tables:
	${PYTHON} ./table_declaration.py
	${PYTHON} ./table_inheritance.py
	${PYTHON} ./table_instantiation.py
	${PYTHON} ./table_create.py
	${PYTHON} ./table_references.py

# end of file 
