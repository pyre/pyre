# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = merlin
PACKAGE = spells
PROJ_CLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    About.py \
    AssetManager.py \
    Initializer.py \
    __init__.py


export:: export-package-python-modules

# end of file
