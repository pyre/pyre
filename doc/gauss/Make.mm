# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010  all rights reserved
#

PROJECT = pyre
PACKAGE = doc/gauss

RECURSE_DIRS = \
   figures \
   listings \

OTHERS = \

#--------------------------------------------------------------------------
#

DOCUMENT = gauss

INCLUDES = \
    config.tex \
    macros.tex \
    meta.tex \
    references.bib

SECTIONS = \
    $(DOCUMENT).tex \
    sec_introduction.tex \
    sec_montecarlo.tex \
    sec_simple.tex \
    sec_classes.tex \
    sec_components.tex \
    sec_pyreapp.tex \
    sec_epilogue.tex \

FIGURES = \
    figures/quadrant.pdf \

LISTINGS = \
    listings/simple/gauss.py \
    listings/simple/gauss.cc \
    listings/classes/Disk.py \
    listings/classes/PointCloud.py \
    listings/classes/Shape.py \
    listings/classes/MersenneTwister.py \
    listings/classes/gauss.py \
    listings/containers/Disk.py \
    listings/containers/PointCloud.py \
    listings/containers/Shape.py \
    listings/containers/MersenneTwister.py \
    listings/containers/gauss.py \
    listings/generators/Disk.py \
    listings/generators/PointCloud.py \
    listings/generators/Shape.py \
    listings/generators/MersenneTwister.py \
    listings/generators/gauss.py \

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
$(DOCUMENT).pdf: $(DOCUMENT).tex $(PACKAGES) $(INCLUDES) $(SECTIONS) $(FIGURES) $(LISTINGS)

# housekeeping
PROJ_CLEAN = $(CLEAN_LATEX) *.snm *.nav *.vrb 
PROJ_DISTCLEAN = *.ps *.pdf $(PROJ_CLEAN)

# end of file
