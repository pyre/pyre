# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = merlin
PACKAGE = spells
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    AssetManager.py \
    Copyright.py \
    Info.py \
    Initializer.py \
    License.py \
    Spell.py \
    Version.py \
    __init__.py


export:: export-package-python-modules

# end of file 
