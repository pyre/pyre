# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# register {python2} as the python compiler
compiler.python := python2

# the name of the executable
python2.driver ?= python

# hardwire the module suffix; {python2-config} doesn't cover this
python2.suffix.module ?= .module.so
# byte compile
python2.compile.base ?= -m compileall -b -q

# compile
python2.compile := $(python2.driver) $(python2.compile.base)


# end of file
