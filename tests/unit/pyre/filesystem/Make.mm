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

test: sanity nodes filesystem

sanity:
	${PYTHON} ./sanity.py

nodes:
	${PYTHON} ./node.py
	${PYTHON} ./folder.py
	${PYTHON} ./folder_insert.py
	${PYTHON} ./folder_insert_multiple.py
	${PYTHON} ./folder_insert_badNode.py
	${PYTHON} ./folder_find.py
	${PYTHON} ./folder_subscripts.py

filesystem:
	${PYTHON} ./filesystem.py
	${PYTHON} ./filesystem_access.py



# end of file 
