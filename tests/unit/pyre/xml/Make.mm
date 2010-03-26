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

test: sanity documents

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./reader.py
	${PYTHON} ./document.py

documents:
	${PYTHON} ./blank.py
	${PYTHON} ./empty.py
	${PYTHON} ./namespaces.py
	${PYTHON} ./schema.py
	${PYTHON} ./fs.py
	${PYTHON} ./fs_namespaces.py
	${PYTHON} ./fs_schema.py


# end of file 
