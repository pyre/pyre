# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    AttributeClassifier.py \
    ExtentAware.py \
    Named.py \
    Observable.py \
    PathHash.py \
    Singleton.py \
    __init__.py


export:: export-package-python-modules

# end of file 
