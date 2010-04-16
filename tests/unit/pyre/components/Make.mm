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

test: sanity metaclasses interfaces components

sanity:
	${PYTHON} ./sanity.py

metaclasses:
	${PYTHON} ./requirement.py
	${PYTHON} ./role.py
	${PYTHON} ./actor.py

interfaces:

components:
	${PYTHON} ./component_sanity.py



# end of file 
