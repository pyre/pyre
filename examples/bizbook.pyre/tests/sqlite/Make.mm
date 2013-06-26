# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = bizbook
PROJ_CLEAN += bizbook.sql

#--------------------------------------------------------------------------
#

all: test

test: sanity create queries drop clean

sanity:
	${PYTHON} ./sanity.py

create:
	${PYTHON} ./create_tables.py
	${PYTHON} ./populate.py

queries:
	${PYTHON} ./projections.py
	${PYTHON} ./restrictions.py
	${PYTHON} ./collations.py

drop:
	${PYTHON} ./drop_tables.py


# end of file 
