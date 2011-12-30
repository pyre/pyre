# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = pyre
PACKAGE = mpi

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS)


TESTS = \
    sanity \
    chronicler \
    inventory \
    diagnostic \
    diagnostic-injection \
    channel \
    index \
    index-inventory \
    debug \
    debug-envvar \
    debug-injection \
    debug-null \
    firewall \
    firewall-injection \
    firewall-null \
    info \
    info-injection \
    warning \
    warning-injection \
    error \
    error-injection \
    debuginfo \
    firewalls \

PROJ_LCC_LIBPATH = $(PROJ_LIBDIR)
PROJ_LCXX_LIBPATH = $(PROJ_LIBDIR)
LIBRARIES = -ljournal $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test clean

test: $(TESTS)
	./sanity
	./inventory
	./diagnostic
	./diagnostic-injection
	./channel
	./index
	./index-inventory
	./chronicler
	./debug
	DEBUG_OPT=pyre.journal.test ./debug-envvar
	./debug-injection
	./debug-null
	./firewall
	./firewall-injection
	./firewall-null
	./info
	./info-injection
	./warning
	./warning-injection
	./error
	./error-injection
	./debuginfo
	./firewalls


sanity: sanity.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

inventory: inventory.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

diagnostic: diagnostic.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

diagnostic-injection: diagnostic-injection.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

channel: channel.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index: index.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index-inventory: index-inventory.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

chronicler: chronicler.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug: debug.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug-envvar: debug-envvar.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug-injection: debug-injection.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug-null: debug-null.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

firewall: firewall.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

firewall-injection: firewall-injection.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

firewall-null: firewall-null.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

info: info.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

info-injection: info-injection.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

warning: warning.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

warning-injection: warning-injection.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

error: error.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

error-injection: error-injection.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debuginfo: debuginfo.c
	$(CC) $(CFLAGS) $< -o $@ $(LCFLAGS) $(LIBRARIES)

firewalls: firewalls.c
	$(CC) $(CFLAGS) $< -o $@ $(LCFLAGS) $(LIBRARIES)


# end of file 
