# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PROJ_TIDY += __pycache__

#--------------------------------------------------------------------------
#

all: test clean

test: sanity api

sanity:
	${PYTHON} ./sanity.py

api:
	${PYTHON} ./loadConfiguration.py
	${PYTHON} ./resolve.py

# end of file 
