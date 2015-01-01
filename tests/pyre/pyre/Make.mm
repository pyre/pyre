# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre
PROJ_TIDY += __pycache__

#--------------------------------------------------------------------------
#

working:
	${PYTHON} ./defaults.py

all: test clean

test: sanity api regressions

sanity:
	${PYTHON} ./sanity.py

api:
	${PYTHON} ./loadConfiguration.py
	${PYTHON} ./resolve.py

regressions:
	${PYTHON} ./defaults.py
	${PYTHON} ./play.py

# end of file
