# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

PROJECT = pyre
PACKAGE = overview

RECURSE_DIRS = \
   figures \
   listings \

OTHERS = \

#--------------------------------------------------------------------------
#

DOCUMENT = overview

PACKAGES =

INCLUDES = \
    pyre.sty \
    setup.tex \
    references.bib

SECTIONS = \
    sec-*.tex \

LISTINGS = \
    listings/*.py \
    ../../examples/gauss.pyre/gauss/*.py \
    ../../examples/gauss.pyre/gauss/functors/*.py \
    ../../examples/gauss.pyre/gauss/integrators/*.py \
    ../../examples/gauss.pyre/gauss/meshes/*.py \
    ../../examples/gauss.pyre/gauss/shapes/*.py \

FIGURES = \
    figures/*.pdf \

#--------------------------------------------------------------------------
#

all: $(DOCUMENT).pdf
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#

# preview types
osx: $(DOCUMENT).pdf
	open $(DOCUMENT).pdf

xpdf: $(DOCUMENT).pdf
	xpdf -remote $(DOCUMENT) $(DOCUMENT).pdf

# make the document using the default document class
$(DOCUMENT).pdf: $(DOCUMENT).tex $(PACKAGES) $(INCLUDES) $(SECTIONS) $(LISTINGS) $(FIGURES)

# housekeeping
PROJ_CLEAN += $(CLEAN_LATEX) *.snm *.nav *.vrb 
PROJ_DISTCLEAN = *.ps *.pdf $(PROJ_CLEAN)

# end of file
