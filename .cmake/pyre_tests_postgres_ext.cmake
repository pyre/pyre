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

# components
pyre_test_python_testcase(tests/postgres.ext/postgres_database.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_attach.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_database_create.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_table.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_reserved.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_references.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_database_drop.py)

# pyre.db against the default database, each in a transaction it rolls back
pyre_test_python_testcase(tests/postgres.ext/postgres_null_insert.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_null_text.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_time.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_timestamp.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_bytes.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_uuid.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_array.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_update_null.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_update_all.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_group_by.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_where_null.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_where_date.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_where_like.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_where_like_escape.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_defaults.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_values.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_nonfinite.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_cast.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_select_arrays.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_with_aborted.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_json.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_bigint.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_table_exist_ok.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_table_missing_ok.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_database_exist_ok.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_database_missing_ok.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_index.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_identity.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_constraint_named.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_projection_derived.py)

# the component tests pound on a database they create and drop; the create is a setup fixture,
# the drop a cleanup one, and everything in between requires it
set_property(TEST tests.postgres.ext.postgres_database_create.py PROPERTY
  FIXTURES_SETUP POSTGRES)
set_property(TEST tests.postgres.ext.postgres_database_drop.py PROPERTY
  FIXTURES_CLEANUP POSTGRES)

# set up the dependencies
set_property(TEST tests.postgres.ext.postgres_table.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)

set_property(TEST tests.postgres.ext.postgres_reserved.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)

set_property(TEST tests.postgres.ext.postgres_references.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)


# end of file
