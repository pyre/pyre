# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
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
    Component.py \
    Curator.py \
    Host.py \
    Merlin.py \
    PackageManager.py \
    PythonClassifier.py \
    Spell.py \
    Spellbook.py \
    User.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
