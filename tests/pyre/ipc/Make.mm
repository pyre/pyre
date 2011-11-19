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

test: sanity scheduler selector

sanity:
	${PYTHON} ./sanity.py

scheduler:
	${PYTHON} ./scheduler.py
	${PYTHON} ./scheduler-instantiation.py
	${PYTHON} ./scheduler-alarms.py

selector:
	${PYTHON} ./selector.py
	${PYTHON} ./selector-instantiation.py
	${PYTHON} ./selector-alarms.py
	${PYTHON} ./selector-fds.py

# end of file 
