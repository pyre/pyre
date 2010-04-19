# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    Behavior.py \
    CompatibilityReport.py \
    Component.py \
    Configurable.py \
    Inventory.py \
    Interface.py \
    Property.py \
    Registrar.py \
    Requirement.py \
    Role.py \
    Trait.py \
    __init__.py


export:: export-package-python-modules

# end of file 
