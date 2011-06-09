# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

PROJ_CLEAN += \
    .merlin/project.pickle

#--------------------------------------------------------------------------
#

all: test

test: sanity merlin clean

sanity:
	${PYTHON} ./sanity.py

merlin:
	${PYTHON} ./merlin-shell.py
	${PYTHON} ./merlin-spell.py
	${PYTHON} ./merlin-curator.py
	${PYTHON} ./merlin-packages.py

# end of file 
