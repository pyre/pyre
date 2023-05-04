# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#

PROJECT = pyre
PACKAGE = doc/overview/config

# punt upstairs
all:
	(cd ..; $(MM))

osx:
	(cd ..; $(MM) osx)

xpdf:
	(cd ..; $(MM) xpdf)

# end of file
