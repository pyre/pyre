# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity algebra structural expressions hierarchical

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

algebra:
	${PYTHON} ./number.py
	${PYTHON} ./ordering.py
	${PYTHON} ./boolean.py

structural:
	${PYTHON} ./reference.py
	${PYTHON} ./dependencies.py
	${PYTHON} ./patch.py

expressions:
	${PYTHON} ./expression.py
	${PYTHON} ./expression_escaped.py
	${PYTHON} ./expression_circular.py
	${PYTHON} ./expression_syntaxerror.py
	${PYTHON} ./expression_typeerror.py

hierarchical:
	${PYTHON} ./hierarchical.py
	${PYTHON} ./hierarchical_patch.py
	${PYTHON} ./hierarchical_alias.py
	${PYTHON} ./hierarchical_group.py

# end of file 
