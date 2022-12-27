# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# journal
#
pyre_test_driver(journal.lib/alert_sanity.cc)
pyre_test_driver(journal.lib/ansi_ansi.cc)
pyre_test_driver_env(journal.lib/ansi_emulates.cc TERM=foo 0)
pyre_test_driver_env_case(journal.lib/ansi_emulates.cc TERM=xterm 1)
pyre_test_driver(journal.lib/ansi_gray.cc)
pyre_test_driver(journal.lib/ansi_misc.cc)
pyre_test_driver(journal.lib/ansi_null.cc)
pyre_test_driver(journal.lib/ansi_x11.cc)
pyre_test_driver(journal.lib/api_application.cc)
pyre_test_driver(journal.lib/api_file.cc)
pyre_test_driver(journal.lib/api_file_mode.cc)
pyre_test_driver(journal.lib/api_quiet.cc)
pyre_test_driver(journal.lib/bland_sanity.cc)
pyre_test_driver(journal.lib/cerr_sanity.cc)
pyre_test_driver(journal.lib/channel_default_device.cc)
pyre_test_driver(journal.lib/channel_device.cc)
pyre_test_driver(journal.lib/channel_flush.cc)
pyre_test_driver(journal.lib/channel_index.cc)
pyre_test_driver(journal.lib/channel_inject.cc)
pyre_test_driver(journal.lib/channel_instance.cc)
pyre_test_driver(journal.lib/channel_inventory.cc)
pyre_test_driver(journal.lib/channel_iomanip.cc)
pyre_test_driver(journal.lib/channel_manipulators.cc)
pyre_test_driver(journal.lib/channel_sanity.cc)
pyre_test_driver(journal.lib/channel_twice.cc)
pyre_test_driver(journal.lib/channel_xtalk.cc)
pyre_test_driver(journal.lib/chronicler_device.cc)
pyre_test_driver(journal.lib/chronicler_globals.cc)
pyre_test_driver(journal.lib/chronicler_init.cc
  --journal.detail=5 --journal.debug=test.init.one,test.init.two)
pyre_test_driver_env_case(journal.lib/chronicler_init.cc
  "JOURNAL_DETAIL=5;JOURNAL_DEBUG=test.init.one,test.init.two")
pyre_test_driver(journal.lib/chronicler_nameset.cc)
pyre_test_driver(journal.lib/chronicler_sanity.cc)
pyre_test_driver_env(journal.lib/chronicler_detail.cc JOURNAL_DETAIL=3 3)
pyre_test_driver_env_case(journal.lib/chronicler_detail.cc JOURNAL_DETAIL=5 5)
pyre_test_driver(journal.lib/cout_sanity.cc)
pyre_test_driver(journal.lib/csi_sanity.cc)
pyre_test_driver(journal.lib/debug_cascade.cc)
pyre_test_driver(journal.lib/debug_code.cc)
pyre_test_driver(journal.lib/debug_color.cc)
pyre_test_driver(journal.lib/debug_empty.cc)
pyre_test_driver(journal.lib/debug_endl.cc)
pyre_test_driver(journal.lib/debug_example.cc)
pyre_test_driver(journal.lib/debug_example_fatal.cc)
pyre_test_driver(journal.lib/debug_file.cc)
pyre_test_driver(journal.lib/debug_file_mode.cc)
pyre_test_driver(journal.lib/debug_flush.cc)
pyre_test_driver(journal.lib/debug_indent.cc)
pyre_test_driver(journal.lib/debug_indent_multi.cc)
pyre_test_driver(journal.lib/debug_inject.cc)
pyre_test_driver(journal.lib/debug_loop.cc)
pyre_test_driver(journal.lib/debug_manipulators.cc)
pyre_test_driver(journal.lib/debug_nolocator.cc)
pyre_test_driver(journal.lib/debug_null.cc)
pyre_test_driver(journal.lib/debug_quiet.cc)
pyre_test_driver(journal.lib/debug_sanity.cc)
pyre_test_driver(journal.lib/debug_shared.cc)
pyre_test_driver(journal.lib/debuginfo.c)
pyre_test_driver(journal.lib/device_sanity.cc)
pyre_test_driver(journal.lib/error_cascade.cc)
pyre_test_driver(journal.lib/error_code.cc)
pyre_test_driver(journal.lib/error_empty.cc)
pyre_test_driver(journal.lib/error_example.cc)
pyre_test_driver(journal.lib/error_example_nonfatal.cc)
pyre_test_driver(journal.lib/error_file.cc)
pyre_test_driver(journal.lib/error_file_mode.cc)
pyre_test_driver(journal.lib/error_indent.cc)
pyre_test_driver(journal.lib/error_indent_multi.cc)
pyre_test_driver(journal.lib/error_inventory.cc)
pyre_test_driver(journal.lib/error_loop.cc)
pyre_test_driver(journal.lib/error_nolocator.cc)
pyre_test_driver(journal.lib/error_quiet.cc)
pyre_test_driver(journal.lib/error_sanity.cc)
pyre_test_driver(journal.lib/error_shared.cc)
pyre_test_driver(journal.lib/file_example.cc)
pyre_test_driver(journal.lib/file_sanity.cc)
pyre_test_driver(journal.lib/firewall_cascade.cc)
pyre_test_driver(journal.lib/firewall_code.cc)
pyre_test_driver(journal.lib/firewall_empty.cc)
pyre_test_driver(journal.lib/firewall_error.cc)
pyre_test_driver(journal.lib/firewall_example.cc)
pyre_test_driver(journal.lib/firewall_example_nonfatal.cc)
pyre_test_driver(journal.lib/firewall_file.cc)
pyre_test_driver(journal.lib/firewall_file_mode.cc)
pyre_test_driver(journal.lib/firewall_indent.cc)
pyre_test_driver(journal.lib/firewall_indent_multi.cc)
pyre_test_driver(journal.lib/firewall_inventory.cc)
pyre_test_driver(journal.lib/firewall_nolocator.cc)
pyre_test_driver(journal.lib/firewall_quiet.cc)
pyre_test_driver(journal.lib/firewall_sanity.cc)
pyre_test_driver(journal.lib/firewall_shared.cc)
pyre_test_driver(journal.lib/firewalls.c)
pyre_test_driver(journal.lib/index_cascade.cc)
pyre_test_driver(journal.lib/index_contains.cc)
pyre_test_driver(journal.lib/index_iter.cc)
pyre_test_driver(journal.lib/index_lookup.cc)
pyre_test_driver(journal.lib/index_sanity.cc)
pyre_test_driver(journal.lib/help_cascade.cc)
pyre_test_driver(journal.lib/help_code.cc)
pyre_test_driver(journal.lib/help_empty.cc)
pyre_test_driver(journal.lib/help_example.cc)
pyre_test_driver(journal.lib/help_example_fatal.cc)
pyre_test_driver(journal.lib/help_file.cc)
pyre_test_driver(journal.lib/help_file_mode.cc)
pyre_test_driver(journal.lib/help_indent.cc)
pyre_test_driver(journal.lib/help_indent_multi.cc)
pyre_test_driver(journal.lib/help_loop.cc)
pyre_test_driver(journal.lib/help_nolocator.cc)
pyre_test_driver(journal.lib/help_quiet.cc)
pyre_test_driver(journal.lib/help_shared.cc)
pyre_test_driver(journal.lib/info_cascade.cc)
pyre_test_driver(journal.lib/info_code.cc)
pyre_test_driver(journal.lib/info_empty.cc)
pyre_test_driver(journal.lib/info_example.cc)
pyre_test_driver(journal.lib/info_example_fatal.cc)
pyre_test_driver(journal.lib/info_file.cc)
pyre_test_driver(journal.lib/info_file_mode.cc)
pyre_test_driver(journal.lib/info_indent.cc)
pyre_test_driver(journal.lib/info_indent_multi.cc)
pyre_test_driver(journal.lib/info_loop.cc)
pyre_test_driver(journal.lib/info_nolocator.cc)
pyre_test_driver(journal.lib/info_quiet.cc)
pyre_test_driver(journal.lib/info_shared.cc)
pyre_test_driver(journal.lib/inventory_device.cc)
pyre_test_driver(journal.lib/inventory_proxy.cc)
pyre_test_driver(journal.lib/inventory_sanity.cc)
pyre_test_driver(journal.lib/journal_sanity.cc)
pyre_test_driver(journal.lib/memo_sanity.cc)
pyre_test_driver(journal.lib/null_inject.cc)
pyre_test_driver(journal.lib/null_manipulators.cc)
pyre_test_driver(journal.lib/null_sanity.cc)
pyre_test_driver(journal.lib/trash_sanity.cc)
pyre_test_driver(journal.lib/warning_cascade.cc)
pyre_test_driver(journal.lib/warning_code.cc)
pyre_test_driver(journal.lib/warning_empty.cc)
pyre_test_driver(journal.lib/warning_example.cc)
pyre_test_driver(journal.lib/warning_example_fatal.cc)
pyre_test_driver(journal.lib/warning_file.cc)
pyre_test_driver(journal.lib/warning_file_mode.cc)
pyre_test_driver(journal.lib/warning_indent.cc)
pyre_test_driver(journal.lib/warning_indent_multi.cc)
pyre_test_driver(journal.lib/warning_loop.cc)
pyre_test_driver(journal.lib/warning_nolocator.cc)
pyre_test_driver(journal.lib/warning_quiet.cc)
pyre_test_driver(journal.lib/warning_shared.cc)

# clean up
add_test(NAME journal.lib.api_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm api_file.log"
  )
set_property(TEST journal.lib.api_file.cleanup PROPERTY
  DEPENDS journal.lib.api_file.cc
  )

add_test(NAME journal.lib.debug_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm debug_file.log"
  )
set_property(TEST journal.lib.debug_file.cleanup PROPERTY
  DEPENDS journal.lib.debug_file.cc
  )

add_test(NAME journal.lib.error_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm error_file.log"
  )
set_property(TEST journal.lib.error_file.cleanup PROPERTY
  DEPENDS journal.lib.error_file.cc
  )

add_test(NAME journal.lib.firewall_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm firewall_file.log"
  )
set_property(TEST journal.lib.firewall_file.cleanup PROPERTY
  DEPENDS journal.lib.firewall_file.cc
  )

add_test(NAME journal.lib.help_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm help_file.log"
  )
set_property(TEST journal.lib.help_file.cleanup PROPERTY
  DEPENDS journal.lib.help_file.cc
  )

add_test(NAME journal.lib.info_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm info_file.log"
  )
set_property(TEST journal.lib.info_file.cleanup PROPERTY
  DEPENDS journal.lib.info_file.cc
  )

add_test(NAME journal.lib.warning_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm warning_file.log"
  )
set_property(TEST journal.lib.warning_file.cleanup PROPERTY
  DEPENDS journal.lib.warning_file.cc
  )

add_test(NAME journal.lib.api_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm api_file_mode.log"
  )
set_property(TEST journal.lib.api_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.api_file_mode.cc
  )

add_test(NAME journal.lib.debug_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm debug_file_mode.log"
  )
set_property(TEST journal.lib.debug_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.debug_file_mode.cc
  )

add_test(NAME journal.lib.error_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm error_file_mode.log"
  )
set_property(TEST journal.lib.error_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.error_file_mode.cc
  )

add_test(NAME journal.lib.firewall_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm firewall_file_mode.log"
  )
set_property(TEST journal.lib.firewall_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.firewall_file_mode.cc
  )

add_test(NAME journal.lib.help_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm help_file_mode.log"
  )
set_property(TEST journal.lib.help_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.help_file_mode.cc
  )

add_test(NAME journal.lib.info_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm info_file_mode.log"
  )
set_property(TEST journal.lib.info_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.info_file_mode.cc
  )

add_test(NAME journal.lib.warning_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm warning_file_mode.log"
  )
set_property(TEST journal.lib.warning_file_mode.cleanup PROPERTY
  DEPENDS journal.lib.warning_file_mode.cc
  )

# end of file
