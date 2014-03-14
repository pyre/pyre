# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = tracking
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Chain.py \
    Command.py \
    File.py \
    FileRegion.py \
    NameLookup.py \
    Script.py \
    Simple.py \
    Tracker.py \
    __init__.py


export:: export-package-python-modules

# end of file 
