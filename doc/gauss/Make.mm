# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011  all rights reserved
#

PROJECT = pyre
PACKAGE = doc/gauss

RECURSE_DIRS = \
   diagrams \
   figures \
   listings \

OTHERS = \

#--------------------------------------------------------------------------
#

DOCUMENT = gauss

INCLUDES = \
    titlepage.sty \
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
    figures/gaussian.pdf \
    figures/quadrant.pdf \

LISTINGS = \
    listings/simple/gauss.py \
    listings/simple/gauss.cc \
    listings/classes/Disk.py \
    listings/classes/PointCloud.py \
    listings/classes/Shape.py \
    listings/classes/Mersenne.py \
    listings/classes/gauss.py \
    listings/containers/Disk.py \
    listings/containers/PointCloud.py \
    listings/containers/Shape.py \
    listings/containers/Mersenne.py \
    listings/containers/gauss.py \
    listings/generators/Constant.py \
    listings/generators/Disk.py \
    listings/generators/Functor.py \
    listings/generators/Gaussian.py \
    listings/generators/Mersenne.py \
    listings/generators/PointCloud.py \
    listings/generators/Shape.py \
    listings/generators/gauss.py \
    listings/generators/gauss-mc.py \
    listings/components/Ball.py \
    listings/components/Box.py \
    listings/components/Constant.py \
    listings/components/Functor.py \
    listings/components/Gaussian.py \
    listings/components/Integrator.py \
    listings/components/Mersenne.py \
    listings/components/MonteCarlo.py \
    listings/components/PointCloud.py \
    listings/components/Shape.py \

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
$(DOCUMENT).pdf: $(DOCUMENT).tex $(INCLUDES) $(SECTIONS) $(FIGURES) $(LISTINGS)

# housekeeping
PROJ_CLEAN = $(CLEAN_LATEX) *.snm *.nav *.vrb 
PROJ_DISTCLEAN = *.ps *.pdf $(PROJ_CLEAN)

# end of file
