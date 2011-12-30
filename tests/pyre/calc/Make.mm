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

test: sanity evaluators structural model

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py
	${PYTHON} ./node.py

evaluators:
	${PYTHON} ./explicit.py
	${PYTHON} ./probe.py
	${PYTHON} ./reference.py
	${PYTHON} ./sum.py
	${PYTHON} ./aggregators.py
	${PYTHON} ./reductors.py
	${PYTHON} ./operations.py
	${PYTHON} ./algebra.py
	${PYTHON} ./expression.py

structural:
	${PYTHON} ./substitute.py
	${PYTHON} ./subsume.py
	${PYTHON} ./patch.py

model:
	${PYTHON} ./model.py

# end of file 
