# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


PROJECT = pyre

# standard targets
all: test

test: sanity paths

sanity:
	${PYTHON} ./sanity.py

paths:
	${PYTHON} ./path.py
	${PYTHON} ./path_arithmetic.py
	${PYTHON} ./path_parts.py


# end of file
