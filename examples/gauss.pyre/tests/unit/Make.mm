# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = gauss.pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity functors shapes meshes integrators

sanity:
	${PYTHON} ./sanity.py

functors:
	${PYTHON} ./one.py
	${PYTHON} ./constant.py
	${PYTHON} ./gaussian.py

meshes:
	${PYTHON} ./mersenne.py

shapes:
	${PYTHON} ./ball.py
	${PYTHON} ./box.py

integrators:
	${PYTHON} ./montecarlo.py


# end of file 
