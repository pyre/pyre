# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

PROJECT = journal
PACKAGE = journal
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    ANSIRenderer.py \
    Channel.py \
    Console.py \
    Debug.py \
    Device.py \
    Diagnostic.py \
    Error.py \
    File.py \
    Firewall.py \
    Info.py \
    Journal.py \
    Renderer.py \
    TextRenderer.py \
    Warning.py \
    exceptions.py \
    protocols.py \
    proxies.py \
    schemes.py \
    __init__.py


export:: export-python-modules

# end of file 
