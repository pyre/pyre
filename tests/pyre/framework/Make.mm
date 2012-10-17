# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test clean

test: sanity slots nameserver fileserver registrar linker executive

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

slots:
	${PYTHON} ./slot.py
	${PYTHON} ./slot_instance.py
	${PYTHON} ./slot_algebra.py
	${PYTHON} ./slot_update.py

nameserver:
	${PYTHON} ./nameserver.py
	${PYTHON} ./nameserver_access.py

fileserver:
	${PYTHON} ./fileserver.py
	${PYTHON} ./fileserver_uri.py
	${PYTHON} ./fileserver_mount.py

registrar:
	${PYTHON} ./registrar.py

linker:
	${PYTHON} ./linker.py
	${PYTHON} ./linker_codecs.py
	${PYTHON} ./linker_shelves.py

executive:
	${PYTHON} ./executive.py
	${PYTHON} ./executive_configuration.py
	${PYTHON} ./executive_retrieveComponentDescriptor.py
	${PYTHON} ./executive_retrieveComponentDescriptor_duplicate.py
	${PYTHON} ./executive_retrieveComponentDescriptor_badImport.py
	${PYTHON} ./executive_retrieveComponentDescriptor_syntaxError.py


# end of file 
