# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = weaver
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Banner.py \
    BlockComments.py \
    BlockMill.py \
    C.py \
    Cxx.py \
    Indenter.py \
    Language.py \
    LineComments.py \
    LineMill.py \
    Mill.py \
    Stationery.py \
    Weaver.py \
    __init__.py


export:: export-package-python-modules

# end of file 
