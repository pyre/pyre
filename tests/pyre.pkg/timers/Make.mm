# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


PROJECT = pyre

all: test

test:
	${PYTHON} ./sanity.py
	${PYTHON} ./process_timer_instance.py
	${PYTHON} ./process_timer_example.py
	${PYTHON} ./wall_timer_instance.py
	${PYTHON} ./wall_timer_example.py

# end of file
