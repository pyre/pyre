# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre
PACKAGE = config
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Assignment.py \
    Calculator.py \
    CommandLine.py \
    Configurator.py \
    Event.py \
    Variable.py \
    __init__.py


export:: export-package-python-modules

# end of file 
