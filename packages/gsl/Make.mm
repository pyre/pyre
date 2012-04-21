# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = gsl
PACKAGE = gsl
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Histogram.py \
    Matrix.py \
    Permutation.py \
    RNG.py \
    Vector.py \
    blas.py \
    linalg.py \
    pdf.py \
    exceptions.py \
    __init__.py


export:: export-python-modules

# end of file 
