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

test: sanity nodes

sanity:
	${PYTHON} ./sanity.py

nodes:
	${PYTHON} ./node.py
	${PYTHON} ./folder.py
	${PYTHON} ./folder_insert.py
	${PYTHON} ./folder_insert_badNode.py
	${PYTHON} ./folder_find.py


# end of file 
