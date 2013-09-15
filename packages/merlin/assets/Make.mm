# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

PROJECT = merlin
PACKAGE = assets
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Asset.py \
    AssetContainer.py \
    PythonModule.py \
    PythonPackage.py \
    __init__.py


export:: export-package-python-modules

# end of file 
