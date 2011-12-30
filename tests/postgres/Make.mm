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

test: sanity pyrepg connections components

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./sanity_pyrepg.py

pyrepg:
	${PYTHON} ./pyrepg_exceptions.py
	${PYTHON} ./pyrepg_connect.py
	${PYTHON} ./pyrepg_execute.py
	${PYTHON} ./pyrepg_execute_badCommand.py
	${PYTHON} ./pyrepg_submit.py

connections:
	${PYTHON} ./connect.py
	${PYTHON} ./disconnect.py
	${PYTHON} ./execute.py

components:
	${PYTHON} ./postgres_database.py
	${PYTHON} ./postgres_attach.py
	${PYTHON} ./postgres_database_create.py
	${PYTHON} ./postgres_table.py
	${PYTHON} ./postgres_reserved.py
	${PYTHON} ./postgres_references.py
	${PYTHON} ./postgres_database_drop.py


# end of file 
