# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

PROJECT = pyre
PACKAGE = weaver
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


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
    CSh.py \
    Cfg.py \
    Cxx.py \
    Django.py \
    Expression.py \
    F77.py \
    F90.py \
    HTML.py \
    Indenter.py \
    Language.py \
    LineComments.py \
    LineMill.py \
    Make.py \
    Mill.py \
    MixedComments.py \
    Perl.py \
    Plexus.py \
    Project.py \
    Python.py \
    SQL.py \
    SVG.py \
    Smith.py \
    Sh.py \
    Stationery.py \
    TeX.py \
    Weaver.py \
    XML.py \
    __init__.py


export:: export-package-python-modules

# end of file
