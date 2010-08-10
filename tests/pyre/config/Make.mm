# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity configurator calculator commandline

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

configurator:
	${PYTHON} ./configurator.py
	${PYTHON} ./configurator_assignments.py

calculator:
	${PYTHON} ./calculator.py
	${PYTHON} ./calculator_assignments.py


commandline:
	${PYTHON} ./command.py
	${PYTHON} ./command_argv.py
	${PYTHON} ./command_config.py


# end of file 
