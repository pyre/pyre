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

test: sanity pyrepg connections components

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./sanity-pyrepg.py

pyrepg:
	${PYTHON} ./pyrepg_exceptions.py
	${PYTHON} ./pyrepg_connect.py
	${PYTHON} ./pyrepg_execute.py
	${PYTHON} ./pyrepg_execute_badCommand.py

connections:
	${PYTHON} ./connect.py
	${PYTHON} ./disconnect.py
	${PYTHON} ./execute.py

components:
	${PYTHON} ./postgres_database.py
	${PYTHON} ./postgres_attach.py


# end of file 
