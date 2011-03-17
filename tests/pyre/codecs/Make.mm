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

working:
	${PYTHON} ./pml_componentName.py

all: test

test: sanity formats

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py
	${PYTHON} ./manager.py

formats: pml

pml:
	${PYTHON} ./pml.py
	${PYTHON} ./pml_empty.py
	${PYTHON} ./pml_badRoot.py
	${PYTHON} ./pml_unknownNode.py
	${PYTHON} ./pml_badNode.py
	${PYTHON} ./pml_badAttribute.py
	${PYTHON} ./pml_inventory.py
	${PYTHON} ./pml_componentFamily.py
	${PYTHON} ./pml_componentName.py

# end of file 
