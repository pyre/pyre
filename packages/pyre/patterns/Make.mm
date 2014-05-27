# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = patterns
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    AbstractMetaclass.py \
    Accumulator.py \
    AttributeClassifier.py \
    CoFunctor.py \
    ExtentAware.py \
    Named.py \
    Observable.py \
    PathHash.py \
    Printer.py \
    Singleton.py \
    Tee.py \
    __init__.py


export:: export-package-python-modules

# end of file 
