# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    Dispatcher.py \
    Marshaller.py \
    Node.py \
    Pickler.py \
    Pipe.py \
    Port.py \
    PortTCP.py \
    Scheduler.py \
    Selector.py \
    Server.py \
    Socket.py \
    SocketTCP.py \
    protocols.py \
    __init__.py


export:: export-package-python-modules

# end of file 
