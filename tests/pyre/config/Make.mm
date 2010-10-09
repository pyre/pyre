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

working:
	${PYTHON} ./configurator_locators.py

all: test

test: sanity configuration configurator commandline

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

configuration:
	${PYTHON} ./configuration.py
	${PYTHON} ./configuration_assignments.py

configurator:
	${PYTHON} ./configurator.py
	${PYTHON} ./configurator_assignments.py
	${PYTHON} ./configurator_load.py


commandline:
	${PYTHON} ./command.py
	${PYTHON} ./command_argv.py
	${PYTHON} ./command_config.py


# end of file 
