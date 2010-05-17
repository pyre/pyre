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
    listings/classes-simple/Disk.py \
    listings/classes-simple/PointCloud.py \
    listings/classes-simple/Shape.py \
    listings/classes-simple/WichmannHill.py \
    listings/classes-simple/gauss.py \
    listings/classes-containers/Disk.py \
    listings/classes-containers/PointCloud.py \
    listings/classes-containers/Shape.py \
    listings/classes-containers/WichmannHill.py \
    listings/classes-containers/gauss.py \
    listings/classes-containers/Disk.py \
    listings/classes-containers/PointCloud.py \
    listings/classes-containers/Shape.py \
    listings/classes-containers/WichmannHill.py \
    listings/classes-containers/gauss.py \

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
