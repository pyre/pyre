# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

working:
	${PYTHON} ./configurator_load_cfg.py

all: test

test: sanity slots configuration configurator commandline

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

slots:
	${PYTHON} ./slot.py
	${PYTHON} ./slot_instance.py
	${PYTHON} ./slot_algebra.py
	${PYTHON} ./slot_update.py

configuration:
	${PYTHON} ./configuration.py
	${PYTHON} ./configuration_assignments.py

configurator:
	${PYTHON} ./configurator.py
	${PYTHON} ./configurator_access.py
	${PYTHON} ./configurator_assignments.py
	${PYTHON} ./configurator_load_pml.py

commandline:
	${PYTHON} ./command.py
	${PYTHON} ./command_argv.py
	${PYTHON} ./command_config.py

# end of file 
