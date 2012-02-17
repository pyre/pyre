# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = bizbook
PROJ_CLEAN += bizbook.sql

#--------------------------------------------------------------------------
#

all: test

test: sanity create queries destroy clean

sanity:
	${PYTHON} ./sanity.py

create:
	${PYTHON} ./create_tables.py
	${PYTHON} ./populate.py

queries:
	${PYTHON} ./projections.py
	${PYTHON} ./restrictions.py
	${PYTHON} ./collations.py

destroy:
	${PYTHON} ./drop_tables.py


# end of file 
