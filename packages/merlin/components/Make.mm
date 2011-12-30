# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = merlin
PACKAGE = components
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    ANSIRenderer.py \
    Curator.py \
    Host.py \
    Merlin.py \
    PackageManager.py \
    Spell.py \
    Spellbook.py \
    TextRenderer.py \
    User.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
