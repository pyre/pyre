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
	${PYTHON} ./interface_sanity.py
	${PYTHON} ./interface_declaration.py
	${PYTHON} ./interface_inheritance.py
	${PYTHON} ./interface_shadow.py
	${PYTHON} ./interface_inheritance_multi.py
	${PYTHON} ./interface_compatibility.py
	${PYTHON} ./interface_compatibility_report.py

components:
	${PYTHON} ./component_sanity.py



# end of file 
