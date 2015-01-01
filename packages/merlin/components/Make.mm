# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = merlin
PACKAGE = components
PROJ_CLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Component.py \
    Curator.py \
    Dashboard.py \
    Merlin.py \
    PythonClassifier.py \
    Spell.py \
    Spellbook.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file
