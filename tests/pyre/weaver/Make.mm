# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test clean

test: sanity weaver documents expressions

sanity:
	${PYTHON} ./sanity.py

weaver:
	${PYTHON} ./weaver.py

documents:
	${PYTHON} ./document_c.py
	${PYTHON} ./document_csh.py
	${PYTHON} ./document_cxx.py
	${PYTHON} ./document_f77.py
	${PYTHON} ./document_f90.py
	${PYTHON} ./document_html.py
	${PYTHON} ./document_latex.py
	${PYTHON} ./document_make.py
	${PYTHON} ./document_perl.py
	${PYTHON} ./document_python.py
	${PYTHON} ./document_sh.py
	${PYTHON} ./document_sql.py
	${PYTHON} ./document_tex.py
	${PYTHON} ./document_xml.py

expressions:
	${PYTHON} ./expressions_c.py
	${PYTHON} ./expressions_cxx.py
	${PYTHON} ./expressions_python.py
	${PYTHON} ./expressions_sql.py

# end of file 
