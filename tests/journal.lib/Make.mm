# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

include journal.def
PACKAGE = journal

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS) $(SPECIAL_TESTS) *.log *.dSYM


TESTS = \
    alert_sanity \
    ansi_ansi \
    ansi_gray \
    ansi_misc \
    ansi_null \
    ansi_x11 \
    api_application \
    api_file \
    api_quiet \
    cerr_sanity \
    channel_default_device \
    channel_device \
    channel_flush \
    channel_index \
    channel_inject \
    channel_instance \
    channel_inventory \
    channel_iomanip \
    channel_manipulators \
    channel_sanity \
    channel_twice \
    channel_xtalk \
    chronicler_device \
    chronicler_globals \
    chronicler_nameset \
    chronicler_sanity \
    cout_sanity \
    csi_sanity \
    debug_cascade \
    debug_empty \
    debug_endl \
    debug_example \
    debug_example_fatal \
    debug_file \
    debug_flush \
    debug_inject \
    debug_loop \
    debug_manipulators \
    debug_nolocator \
    debug_null \
    debug_quiet \
    debug_sanity \
    debug_shared \
    device_sanity \
    error_cascade \
    error_empty \
    error_example \
    error_example_nonfatal \
    error_file \
    error_inventory \
    error_loop \
    error_nolocator \
    error_quiet \
    error_sanity \
    error_shared \
    file_example \
    file_sanity \
    firewall_cascade \
    firewall_empty \
    firewall_error \
    firewall_example \
    firewall_example_nonfatal \
    firewall_file \
    firewall_inventory \
    firewall_nolocator \
    firewall_quiet \
    firewall_sanity \
    firewall_shared \
    index_cascade \
    index_contains \
    index_iter \
    index_lookup \
    index_sanity \
    info_cascade \
    info_empty \
    info_example \
    info_example_fatal \
    info_file \
    info_loop \
    info_nolocator \
    info_quiet \
    info_shared \
    inventory_device \
    inventory_proxy \
    inventory_sanity \
    journal_sanity \
    memo_sanity \
    null_inject \
    null_manipulators \
    null_sanity \
    trash_sanity \
    warning_cascade \
    warning_empty \
    warning_example \
    warning_example_fatal \
    warning_file \
    warning_loop \
    warning_nolocator \
    warning_quiet \
    warning_shared \
    debuginfo \
    firewalls \


SPECIAL_TESTS = \
    ansi_emulates \
    chronicler_init \
    chronicler_detail \

PROJ_LCC_LIBPATH = $(PROJ_LIBDIR)
PROJ_LCXX_LIBPATH = $(PROJ_LIBDIR)
PROJ_LIBRARIES = -ljournal
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test clean

test: $(TESTS) $(SPECIAL_TESTS)
	@echo "testing:"
	@for testcase in $(TESTS); do { echo "    $${testcase}" ; ./$${testcase} ; } done
	@echo "    ansi_emulates foo"; TERM=foo ./ansi_emulates 0
	@echo "    ansi_emulates xterm"; TERM=xterm ./ansi_emulates 1
	@echo "    chronicler_init"; \
            JOURNAL_DETAIL=5 JOURNAL_DEBUG=test.init.one,test.init.two \
            ./chronicler_init \
            --journal.detail=5 --journal.debug=test.init.one,test.init.two
	@echo "    chronicler_detail 3"; JOURNAL_DETAIL=3 ./chronicler_detail 3
	@echo "    chronicler_detail 5"; JOURNAL_DETAIL=5 ./chronicler_detail 5

# build
%: %.c
	$(CC) $(CFLAGS) $^ -o $@ $(LCFLAGS) $(LIBRARIES)

%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)

# end of file
