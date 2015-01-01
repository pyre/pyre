# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre
PACKAGE = framework
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Dashboard.py \
    Environ.py \
    Executive.py \
    Externals.py \
    FileServer.py \
    Linker.py \
    NameServer.py \
    Package.py \
    Priority.py \
    Pyre.py \
    Schema.py \
    Slot.py \
    SlotInfo.py \
    exceptions.py \
    __init__.py

export:: export-package-python-modules

# end of file
