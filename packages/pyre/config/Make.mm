# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = config
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)

RECURSE_DIRS = \
    native \
    odb \
    pml \
    pcs \

#--------------------------------------------------------------------------
#

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Codec.py \
    CodecManager.py \
    CommandLine.py \
    Configuration.py \
    Configurator.py \
    Model.py \
    Slot.py \
    events.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


# end of file 
