# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = ipc
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Channel.py \
    Marshaller.py \
    Pickler.py \
    Pipe.py \
    Scheduler.py \
    Selector.py \
    Socket.py \
    sockaddr.py \
    __init__.py


export:: export-package-python-modules

# end of file 
