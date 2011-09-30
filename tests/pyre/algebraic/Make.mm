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

test: sanity algebra structural expressions

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

algebra:
	${PYTHON} ./number.py
	${PYTHON} ./ordering.py
	${PYTHON} ./boolean.py

structural:
	${PYTHON} ./dependencies.py
	${PYTHON} ./patch.py

expressions:
	${PYTHON} ./expression.py
	${PYTHON} ./expression_escaped.py
	${PYTHON} ./expression_circular.py
	${PYTHON} ./expression_syntaxerror.py
	${PYTHON} ./expression_typeerror.py

# end of file 
