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

test: sanity evaluators faulty

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./node.py

evaluators:
	${PYTHON} ./literal.py
	${PYTHON} ./probe.py
	${PYTHON} ./reference.py
	${PYTHON} ./sum.py
	${PYTHON} ./aggregators.py
	${PYTHON} ./reductors.py
	${PYTHON} ./operations.py
	${PYTHON} ./expression.py
	${PYTHON} ./sample.py

faulty:
	${PYTHON} ./expression_resolution.py
	${PYTHON} ./expression_circular.py
	${PYTHON} ./expression_syntaxerror.py
	${PYTHON} ./expression_typeerror.py

# end of file 
