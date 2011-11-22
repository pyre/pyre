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

test: sanity channels scheduler selector

sanity:
	${PYTHON} ./sanity.py

channels:
	${PYTHON} ./pipe.py
	${PYTHON} ./pickler.py
	${PYTHON} ./pickler_over_pipe.py

scheduler:
	${PYTHON} ./scheduler.py
	${PYTHON} ./scheduler_instantiation.py
	${PYTHON} ./scheduler_alarms.py

selector:
	${PYTHON} ./selector.py
	${PYTHON} ./selector_instantiation.py
	${PYTHON} ./selector_alarms.py
	${PYTHON} ./selector_fds.py
	${PYTHON} ./selector_pickler_over_pipe.py


# end of file 
