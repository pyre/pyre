# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = components
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


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
    Executive.py \
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
