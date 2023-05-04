# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

PROJECT = pyre
PACKAGE = doc/overview/sections

# punt upstairs
all:
	(cd ..; $(MM))

osx:
	(cd ..; $(MM) osx)

xpdf:
	(cd ..; $(MM) xpdf)

# end of file
