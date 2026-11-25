# -*- cmake -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


#
# postgres capability tests
#
# sanity
pyre_test_python_testcase(tests/postgres.ext/sanity.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_sanity.py)
# the low level interface, over the pybind11 bindings
pyre_test_python_testcase(tests/postgres.ext/libpq_connect.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_execute.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_exceptions.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_async.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_bool.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_numbers.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_bytea.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_times.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_json.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_arrays.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_datestyle.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_uuid.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_text.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_timezones.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_arrays_nested.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_arrays_bounds.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_arrays_quoted.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_infinity.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_era.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_values_midnight.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_session_settings.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_arguments_nul.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_arguments_types.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_transaction_failed_commit.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_threads.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_copy_in.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_copy_in_raised.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_copy_out.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_copy_exec.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_prepare.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_describe.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_release.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_stream.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_stream_arguments.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_stream_refused.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_stream_abandoned.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_stream_failed.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_send_prepared.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_pipeline.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_pipeline_failed.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_pipeline_skipped_check.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_connect_boolean.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_row_column_range.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_transaction_exit_waits.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_transaction_collected_waits.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_stream_collected_waits.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_copy_in_collected_waits.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_copy_out_collected_waits.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_pipeline_collected_waits.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_error_context.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_error_internal_query.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_diagnostic_internal_query.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_send_params.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_field_bytes.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_row_negative.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_cancel.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_reset.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_flush.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_notify_other.py)


# end of file
