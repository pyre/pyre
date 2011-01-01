# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = parsing
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Lexer.py \
    Parser.py \
    Scanner.py \
    Token.py \
    TokenDescriptor.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
