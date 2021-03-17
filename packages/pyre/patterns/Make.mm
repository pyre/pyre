# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = patterns
# the python modules
EXPORT_PYTHON_MODULES = \
    Accumulator.py \
    AttributeClassifier.py \
    AttributeFilter.py \
    CoFunctor.py \
    Extent.py \
    Named.py \
    Observable.py \
    Printer.py \
    Singleton.py \
    Tee.py \
    Type.py \
    Unique.py \
    __init__.py

# standard targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
