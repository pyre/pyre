# -*- cmake -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the drivers that start threads need the thread library, which older linux systems keep apart
find_package(Threads REQUIRED)


# register a postgres library test driver
#
# the plain {pyre_test_driver} links against {pyre} and {journal} only; these drivers also need
# the header-only {pyre::postgres} library, which drags in libpq, and the thread library
function(pyre_test_driver_postgres testfile)
  # generate the name of the testcase
  pyre_test_testcase(testname ${testfile})
  # generate the name of the target
  pyre_target(target ${testfile})

  # schedule it to be compiled
  add_executable(${target} ${testfile})
  # with some macros
  target_compile_definitions(${target} PRIVATE PYRE_CORE)
  # that keep their checks in every configuration
  pyre_test_checks(${target})
  # link against the postgres layer, which brings pyre, journal and libpq along, and the threads
  target_link_libraries(${target} PUBLIC pyre::postgres Threads::Threads)

  # make it a test case
  add_test(NAME ${testname} COMMAND ${target})
  # specify the directory for the target compilation products
  pyre_target_directory(${target} tests)

  # all done
endfunction()


# the postgres library tests; each stands on its own over libpq, and none of them loads python
pyre_test_driver_postgres(tests/postgres.lib/sanity.cc)
pyre_test_driver_postgres(tests/postgres.lib/connect.cc)
pyre_test_driver_postgres(tests/postgres.lib/exec.cc)
pyre_test_driver_postgres(tests/postgres.lib/codecs.cc)
pyre_test_driver_postgres(tests/postgres.lib/codecs_locale.cc)
pyre_test_driver_postgres(tests/postgres.lib/errors.cc)
pyre_test_driver_postgres(tests/postgres.lib/transaction.cc)
pyre_test_driver_postgres(tests/postgres.lib/transaction_aborted.cc)
pyre_test_driver_postgres(tests/postgres.lib/transaction_nested_rollback.cc)
pyre_test_driver_postgres(tests/postgres.lib/transaction_nested_release.cc)
pyre_test_driver_postgres(tests/postgres.lib/threads.cc)
pyre_test_driver_postgres(tests/postgres.lib/cancel.cc)
pyre_test_driver_postgres(tests/postgres.lib/async.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in_escape.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in_abort.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in_abandoned.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in_statement.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_out.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_out_abandoned.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_out_abandoned_transaction.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_exec.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_exec_out.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_result.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_threads.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_in_exec_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/copy_out_exec_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/send_exec_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_exec.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_duplicate.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_unknown.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_describe.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_describe_unknown.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_release.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_release_aborted.cc)
pyre_test_driver_postgres(tests/postgres.lib/prepare_release_unknown.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_arguments.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_empty.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_abandoned.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_abandoned_transaction.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_exec_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_failed.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_copy.cc)
pyre_test_driver_postgres(tests/postgres.lib/stream_batch_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/send_prepared.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_prepared.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_failed.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_skipped_raise.cc)
pyre_test_driver_postgres(tests/postgres.lib/result_raise_ran.cc)
pyre_test_driver_postgres(tests/postgres.lib/handle_box_failed.cc)
pyre_test_driver_postgres(tests/postgres.lib/handle_count_failed.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_flush.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_exec_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_abandoned.cc)
pyre_test_driver_postgres(tests/postgres.lib/pipeline_large.cc)
pyre_test_driver_postgres(tests/postgres.lib/hold.cc)
pyre_test_driver_postgres(tests/postgres.lib/hold_refused.cc)
pyre_test_driver_postgres(tests/postgres.lib/hold_threads.cc)
pyre_test_driver_postgres(tests/postgres.lib/hold_closed.cc)


# end of file
