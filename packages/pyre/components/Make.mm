# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = components
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Actor.py \
    CompatibilityReport.py \
    Component.py \
    Configurable.py \
    Inventory.py \
    PrivateInventory.py \
    Protocol.py \
    PublicInventory.py \
    Registrar.py \
    Requirement.py \
    Role.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
