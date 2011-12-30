# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

PROJ_CLEAN = shells.log

#--------------------------------------------------------------------------
#

all: test

test: sanity application script daemon clean

sanity:
	${PYTHON} ./sanity.py

application:
	${PYTHON} ./application-sanity.py
	${PYTHON} ./application-instantiation.py
	${PYTHON} ./application-namespace.py

script:
	${PYTHON} ./script-sanity.py
	${PYTHON} ./script-instantiation.py

daemon:
	${PYTHON} ./daemon-sanity.py
	${PYTHON} ./daemon-instantiation.py

# end of file 
