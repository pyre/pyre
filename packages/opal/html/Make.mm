# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = opal
PACKAGE = html
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


all: export


EXPORT_PYTHON_MODULES = \
    __init__.py

export:: export-package-python-modules


# end of file
