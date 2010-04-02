# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity configurator evaluator

sanity:
	${PYTHON} ./sanity.py

configurator:
	${PYTHON} ./configurator.py
	${PYTHON} ./configurator_assignments.py

evaluator:
	${PYTHON} ./evaluator.py


# end of file 
