# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = parsing
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Descriptor.py \
    Lexer.py \
    Parser.py \
    Scanner.py \
    Token.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
