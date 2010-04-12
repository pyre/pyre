# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

PROJECT = pyre
PACKAGE = tracking
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


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
    Script.py \
    Simple.py \
    Tracker.py \
    __init__.py


export:: export-package-python-modules

# end of file 
