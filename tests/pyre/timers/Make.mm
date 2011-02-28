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

test: sanity python-timer pyre-timer

sanity:
	${PYTHON} ./sanity.py

python-timer:
	${PYTHON} ./python_timer.py
	${PYTHON} ./python_timer_errors.py

pyre-timer:
	${PYTHON} ./pyre_timer.py

# end of file 
