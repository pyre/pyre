# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


PROJECT = gauss
PACKAGE = integrators
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Integrator.py \
    MonteCarlo.py \
    __init__.py


export:: export-package-python-modules

# end of file
