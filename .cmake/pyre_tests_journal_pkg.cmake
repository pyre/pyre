# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# journal
#
pyre_test_python_testcase(journal.pkg/alert_sanity.py)
pyre_test_python_testcase(journal.pkg/ansi_ansi.py)
pyre_test_python_testcase_env(journal.pkg/ansi_emulates.py "TERM=foo" 0)
pyre_test_python_testcase_env(journal.pkg/ansi_emulates.py "TERM=xterm" 1)
pyre_test_python_testcase(journal.pkg/ansi_gray.py)
pyre_test_python_testcase(journal.pkg/ansi_misc.py)
pyre_test_python_testcase(journal.pkg/ansi_null.py)
pyre_test_python_testcase(journal.pkg/ansi_x11.py)
pyre_test_python_testcase(journal.pkg/api_application.py)
pyre_test_python_testcase(journal.pkg/api_file.py)
pyre_test_python_testcase(journal.pkg/api_file_mode.py)
pyre_test_python_testcase(journal.pkg/api_quiet.py)
pyre_test_python_testcase(journal.pkg/bland_sanity.py)
pyre_test_python_testcase(journal.pkg/cerr_sanity.py)
pyre_test_python_testcase(journal.pkg/channel_default_device.py)
pyre_test_python_testcase(journal.pkg/channel_device.py)
pyre_test_python_testcase(journal.pkg/channel_index.py)
pyre_test_python_testcase(journal.pkg/channel_inject.py)
pyre_test_python_testcase(journal.pkg/channel_inventory.py)
pyre_test_python_testcase(journal.pkg/channel_sanity.py)
pyre_test_python_testcase(journal.pkg/channel_state.py)
pyre_test_python_testcase(journal.pkg/channel_twice.py)
pyre_test_python_testcase(journal.pkg/channel_xtalk.py)
pyre_test_python_testcase(journal.pkg/chronicler_device.py)
pyre_test_python_testcase(journal.pkg/chronicler_sanity.py)
pyre_test_python_testcase(journal.pkg/cout_sanity.py)
pyre_test_python_testcase(journal.pkg/csi_sanity.py)
pyre_test_python_testcase(journal.pkg/debug_cascade.py)
pyre_test_python_testcase(journal.pkg/debug_empty.py)
pyre_test_python_testcase(journal.pkg/debug_example.py)
pyre_test_python_testcase(journal.pkg/debug_example_fatal.py)
pyre_test_python_testcase(journal.pkg/debug_file.py)
pyre_test_python_testcase(journal.pkg/debug_file_mode.py)
pyre_test_python_testcase(journal.pkg/debug_flush.py)
pyre_test_python_testcase(journal.pkg/debug_inject.py)
pyre_test_python_testcase(journal.pkg/debug_instance.py)
pyre_test_python_testcase(journal.pkg/debug_loop.py)
pyre_test_python_testcase(journal.pkg/debug_quiet.py)
pyre_test_python_testcase(journal.pkg/debug_report.py)
pyre_test_python_testcase(journal.pkg/debug_sanity.py)
pyre_test_python_testcase(journal.pkg/error_cascade.py)
pyre_test_python_testcase(journal.pkg/error_empty.py)
pyre_test_python_testcase(journal.pkg/error_example.py)
pyre_test_python_testcase(journal.pkg/error_example_nonfatal.py)
pyre_test_python_testcase(journal.pkg/error_file.py)
pyre_test_python_testcase(journal.pkg/error_file_mode.py)
pyre_test_python_testcase(journal.pkg/error_flush.py)
pyre_test_python_testcase(journal.pkg/error_inject.py)
pyre_test_python_testcase(journal.pkg/error_instance.py)
pyre_test_python_testcase(journal.pkg/error_loop.py)
pyre_test_python_testcase(journal.pkg/error_quiet.py)
pyre_test_python_testcase(journal.pkg/error_report.py)
pyre_test_python_testcase(journal.pkg/error_sanity.py)
pyre_test_python_testcase(journal.pkg/file_example.py)
pyre_test_python_testcase(journal.pkg/file_sanity.py)
pyre_test_python_testcase(journal.pkg/firewall_cascade.py)
pyre_test_python_testcase(journal.pkg/firewall_empty.py)
pyre_test_python_testcase(journal.pkg/firewall_example.py)
pyre_test_python_testcase(journal.pkg/firewall_example_nonfatal.py)
pyre_test_python_testcase(journal.pkg/firewall_file.py)
pyre_test_python_testcase(journal.pkg/firewall_file_mode.py)
pyre_test_python_testcase(journal.pkg/firewall_flush.py)
pyre_test_python_testcase(journal.pkg/firewall_inject.py)
pyre_test_python_testcase(journal.pkg/firewall_instance.py)
pyre_test_python_testcase(journal.pkg/firewall_loop.py)
pyre_test_python_testcase(journal.pkg/firewall_quiet.py)
pyre_test_python_testcase(journal.pkg/firewall_report.py)
pyre_test_python_testcase(journal.pkg/firewall_sanity.py)
pyre_test_python_testcase(journal.pkg/index_cascade.py)
pyre_test_python_testcase(journal.pkg/index_lookup.py)
pyre_test_python_testcase(journal.pkg/index_sanity.py)
pyre_test_python_testcase(journal.pkg/help_cascade.py)
pyre_test_python_testcase(journal.pkg/help_empty.py)
pyre_test_python_testcase(journal.pkg/help_example.py)
pyre_test_python_testcase(journal.pkg/help_example_fatal.py)
pyre_test_python_testcase(journal.pkg/help_file.py)
pyre_test_python_testcase(journal.pkg/help_file_mode.py)
pyre_test_python_testcase(journal.pkg/help_flush.py)
pyre_test_python_testcase(journal.pkg/help_inject.py)
pyre_test_python_testcase(journal.pkg/help_instance.py)
pyre_test_python_testcase(journal.pkg/help_loop.py)
pyre_test_python_testcase(journal.pkg/help_quiet.py)
pyre_test_python_testcase(journal.pkg/help_report.py)
pyre_test_python_testcase(journal.pkg/help_sanity.py)
pyre_test_python_testcase(journal.pkg/info_cascade.py)
pyre_test_python_testcase(journal.pkg/info_empty.py)
pyre_test_python_testcase(journal.pkg/info_example.py)
pyre_test_python_testcase(journal.pkg/info_example_fatal.py)
pyre_test_python_testcase(journal.pkg/info_file.py)
pyre_test_python_testcase(journal.pkg/info_file_mode.py)
pyre_test_python_testcase(journal.pkg/info_flush.py)
pyre_test_python_testcase(journal.pkg/info_inject.py)
pyre_test_python_testcase(journal.pkg/info_instance.py)
pyre_test_python_testcase(journal.pkg/info_loop.py)
pyre_test_python_testcase(journal.pkg/info_quiet.py)
pyre_test_python_testcase(journal.pkg/info_report.py)
pyre_test_python_testcase(journal.pkg/info_sanity.py)
pyre_test_python_testcase(journal.pkg/memo_long_filename.py)
pyre_test_python_testcase(journal.pkg/memo_sanity.py)
pyre_test_python_testcase(journal.pkg/null_inject.py)
pyre_test_python_testcase(journal.pkg/null_sanity.py)
pyre_test_python_testcase(journal.pkg/sanity.py)
pyre_test_python_testcase(journal.pkg/trash_sanity.py)
pyre_test_python_testcase(journal.pkg/warning_cascade.py)
pyre_test_python_testcase(journal.pkg/warning_empty.py)
pyre_test_python_testcase(journal.pkg/warning_example.py)
pyre_test_python_testcase(journal.pkg/warning_example_fatal.py)
pyre_test_python_testcase(journal.pkg/warning_file.py)
pyre_test_python_testcase(journal.pkg/warning_file_mode.py)
pyre_test_python_testcase(journal.pkg/warning_flush.py)
pyre_test_python_testcase(journal.pkg/warning_inject.py)
pyre_test_python_testcase(journal.pkg/warning_instance.py)
pyre_test_python_testcase(journal.pkg/warning_loop.py)
pyre_test_python_testcase(journal.pkg/warning_quiet.py)
pyre_test_python_testcase(journal.pkg/warning_report.py)
pyre_test_python_testcase(journal.pkg/warning_sanity.py)

# clean up
add_test(NAME journal.pkg.api_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "echo $(pwd); rm api_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.api_file.cleanup PROPERTY
  DEPENDS journal.pkg.api_file.py
  )

add_test(NAME journal.pkg.debug_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm debug_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.debug_file.cleanup PROPERTY
  DEPENDS journal.pkg.debug_file.py
  )

add_test(NAME journal.pkg.error_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm error_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.error_file.cleanup PROPERTY
  DEPENDS journal.pkg.error_file.py
  )

add_test(NAME journal.pkg.firewall_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm firewall_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.firewall_file.cleanup PROPERTY
  DEPENDS journal.pkg.firewall_file.py
  )

add_test(NAME journal.pkg.help_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm help_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.help_file.cleanup PROPERTY
  DEPENDS journal.pkg.help_file.py
  )

add_test(NAME journal.pkg.info_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm info_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.info_file.cleanup PROPERTY
  DEPENDS journal.pkg.info_file.py
  )

add_test(NAME journal.pkg.warning_file.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm warning_file.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.warning_file.cleanup PROPERTY
  DEPENDS journal.pkg.warning_file.py
  )

add_test(NAME journal.pkg.file_sanity.cleanup
  COMMAND ${BASH_PROGRAM} -c "echo $(pwd); rm file_sanity.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.file_sanity.cleanup PROPERTY
  DEPENDS journal.pkg.file_sanity.py
  )

add_test(NAME journal.pkg.file_example.cleanup
  COMMAND ${BASH_PROGRAM} -c "echo $(pwd); rm file_example.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.file_example.cleanup PROPERTY
  DEPENDS journal.pkg.file_example.py
  )

# clean up
add_test(NAME journal.pkg.api_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "echo $(pwd); rm api_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.api_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.api_file_mode.py
  )

add_test(NAME journal.pkg.debug_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm debug_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.debug_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.debug_file_mode.py
  )

add_test(NAME journal.pkg.error_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm error_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.error_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.error_file_mode.py
  )

add_test(NAME journal.pkg.firewall_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm firewall_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.firewall_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.firewall_file_mode.py
  )

add_test(NAME journal.pkg.help_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm help_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.help_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.help_file_mode.py
  )

add_test(NAME journal.pkg.info_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm info_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.info_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.info_file_mode.py
  )

add_test(NAME journal.pkg.warning_file_mode.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm warning_file_mode.log"
  WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/journal.pkg
  )
set_property(TEST journal.pkg.warning_file_mode.cleanup PROPERTY
  DEPENDS journal.pkg.warning_file_mode.py
  )


# end of file
