# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2020 all rights reserved
#

include journal.def
PACKAGE = journal

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS) $(SPECIAL_TESTS)


TESTS = \
    sanity \
    chronicler-sanity \
    inventory \
    diagnostic-sanity \
    diagnostic-injection \
    channel-inventory \
    index-lookup \
    index-inventory \
    debug-inventory \
    debug-injection \
    debug-null \
    firewall-inventory \
    firewall-injection \
    firewall-null \
    info-inventory \
    info-injection \
    warning-inventory \
    warning-injection \
    error-inventory \
    error-injection \
    debuginfo \
    firewalls \

SPECIAL_TESTS = \
    debug-envvar \

PROJ_LCC_LIBPATH = $(PROJ_LIBDIR)
PROJ_LCXX_LIBPATH = $(PROJ_LIBDIR)
PROJ_LIBRARIES = -ljournal
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test clean

test: $(TESTS) $(SPECIAL_TESTS)
	@echo "testing:"
	@for testcase in $(TESTS); do { echo "    $${testcase}" ; ./$${testcase} ; } done
	@echo "    debug-envvar"; DEBUG_OPT=pyre.journal.test ./debug-envvar

# build
%: %.c
	$(CC) $(CFLAGS) $^ -o $@ $(LCFLAGS) $(LIBRARIES)

%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)

# end of file
