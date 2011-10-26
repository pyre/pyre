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

test: sanity create destroy

sanity:
	${PYTHON} ./sanity.py

create:
	${PYTHON} ./create_database.py
	${PYTHON} ./create_tables.py
	${PYTHON} ./populate.py

destroy:
	${PYTHON} ./drop_tables.py
	${PYTHON} ./drop_database.py


# end of file 
