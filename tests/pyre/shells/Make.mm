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

test: sanity launching clean

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./application-sanity.py
	${PYTHON} ./application-instantiation.py
	${PYTHON} ./application-namespace.py
	${PYTHON} ./script-sanity.py
	${PYTHON} ./script-instantiation.py
	${PYTHON} ./fork-sanity.py
	${PYTHON} ./fork-instantiation.py
	${PYTHON} ./daemon-sanity.py
	${PYTHON} ./daemon-instantiation.py

launching:
	${PYTHON} ./script-launching.py
	${PYTHON} ./fork-launching.py
	${PYTHON} ./daemon-launching.py


# end of file 
