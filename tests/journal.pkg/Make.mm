# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


PROJECT = pyre

PROJ_CLEAN += *.log

#--------------------------------------------------------------------------
#

all: test clean

test: sanity channels devices

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./csi_sanity.py
	${PYTHON} ./chronicler_sanity.py
	${PYTHON} ./alert_sanity.py
	${PYTHON} ./memo_sanity.py
	${PYTHON} ./null_sanity.py
	${PYTHON} ./cout_sanity.py
	${PYTHON} ./cerr_sanity.py
	${PYTHON} ./trash_sanity.py
	${PYTHON} ./file_sanity.py
	${PYTHON} ./index_sanity.py
	${PYTHON} ./channel_sanity.py
	${PYTHON} ./debug_sanity.py
	${PYTHON} ./error_sanity.py
	${PYTHON} ./firewall_sanity.py
	${PYTHON} ./info_sanity.py
	${PYTHON} ./warning_sanity.py

colors:
	${PYTHON} ./ansi_ansi.py
	${PYTHON} ./ansi_emulates.py
	${PYTHON} ./ansi_gray.py
	${PYTHON} ./ansi_misc.py
	${PYTHON} ./ansi_null.py
	${PYTHON} ./ansi_x11.py

api:
	${PYTHON} ./api_quiet.py
	${PYTHON} ./api_file.py
	${PYTHON} ./api_application.py
	${PYTHON} ./chronicler_device.py

channels:
	${PYTHON} ./index_lookup.py
	${PYTHON} ./channel_default_device.py
	${PYTHON} ./channel_device.py
	${PYTHON} ./channel_index.py
	${PYTHON} ./channel_inject.py
	${PYTHON} ./channel_inventory.py
	${PYTHON} ./channel_state.py
	${PYTHON} ./channel_twice.py
	${PYTHON} ./channel_xtalk.py
	${PYTHON} ./debug_cascade.py
	${PYTHON} ./debug_empty.py
	${PYTHON} ./debug_example.py
	${PYTHON} ./debug_example_fatal.py
	${PYTHON} ./debug_file.py
	${PYTHON} ./debug_flush.py
	${PYTHON} ./debug_inject.py
	${PYTHON} ./debug_instance.py
	${PYTHON} ./debug_loop.py
	${PYTHON} ./debug_quiet.py
	${PYTHON} ./error_cascade.py
	${PYTHON} ./error_empty.py
	${PYTHON} ./error_example.py
	${PYTHON} ./error_example_nonfatal.py
	${PYTHON} ./error_file.py
	${PYTHON} ./error_flush.py
	${PYTHON} ./error_inject.py
	${PYTHON} ./error_instance.py
	${PYTHON} ./error_loop.py
	${PYTHON} ./error_quiet.py
	${PYTHON} ./firewall_cascade.py
	${PYTHON} ./firewall_empty.py
	${PYTHON} ./firewall_example.py
	${PYTHON} ./firewall_example_nonfatal.py
	${PYTHON} ./firewall_file.py
	${PYTHON} ./firewall_flush.py
	${PYTHON} ./firewall_inject.py
	${PYTHON} ./firewall_instance.py
	${PYTHON} ./firewall_loop.py
	${PYTHON} ./firewall_quiet.py
	${PYTHON} ./index_cascade.py
	${PYTHON} ./info_cascade.py
	${PYTHON} ./info_empty.py
	${PYTHON} ./info_example.py
	${PYTHON} ./info_example_fatal.py
	${PYTHON} ./info_file.py
	${PYTHON} ./info_flush.py
	${PYTHON} ./info_inject.py
	${PYTHON} ./info_instance.py
	${PYTHON} ./info_loop.py
	${PYTHON} ./info_quiet.py
	${PYTHON} ./warning_cascade.py
	${PYTHON} ./warning_empty.py
	${PYTHON} ./warning_example.py
	${PYTHON} ./warning_example_fatal.py
	${PYTHON} ./warning_file.py
	${PYTHON} ./warning_flush.py
	${PYTHON} ./warning_inject.py
	${PYTHON} ./warning_instance.py
	${PYTHON} ./warning_loop.py
	${PYTHON} ./warning_quiet.py

renderers:
	${PYTHON} ./memo_long_filename.py

devices:
	${PYTHON} ./null_inject.py
	${PYTHON} ./file_example.py

# end of file
