# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

#
# h5 extension: these drivers import the {libh5} bindings directly, so a failure isolates the
# binding layer from the {pyre.h5} package shim above it
#
# sanity
pyre_test_python_testcase(tests/h5.ext/sanity.py)
# the property lists, each proving that what it was told is what it reports
pyre_test_python_testcase(tests/h5.ext/acpl.py)
pyre_test_python_testcase(tests/h5.ext/dcpl_fill.py)
pyre_test_python_testcase(tests/h5.ext/fapl.py)
pyre_test_python_testcase(tests/h5.ext/fcpl.py)
pyre_test_python_testcase(tests/h5.ext/gcpl.py)
pyre_test_python_testcase(tests/h5.ext/lcpl.py)
# the out-of-core mosaic
pyre_test_python_testcase(tests/h5.ext/mosaic.py)
# the raw data chunk cache: that it is consulted, and that an access list can size it
pyre_test_python_testcase(tests/h5.ext/read_chunk_cache.py)
pyre_test_python_testcase(tests/h5.ext/dapl_chunk_cache.py)
# the chunk table, and moving a chunk in the form it is stored in
pyre_test_python_testcase(tests/h5.ext/chunk_table.py)
pyre_test_python_testcase(tests/h5.ext/direct_chunk.py)
# a tile that skips cells, and one that is transformed on its way across
pyre_test_python_testcase(tests/h5.ext/strided_tile.py)
pyre_test_python_testcase(tests/h5.ext/transfer_list.py)

# the drivers leave their scratch products behind so they can be inspected; the harness
# sweeps them, each after the driver that makes it
pyre_test_python_cleanup(h5_ext_acpl.h5 tests/h5.ext/acpl.py)
pyre_test_python_cleanup(h5_ext_dcpl_fill.h5 tests/h5.ext/dcpl_fill.py)
pyre_test_python_cleanup(h5_ext_fapl.h5 tests/h5.ext/fapl.py)
pyre_test_python_cleanup(h5_ext_fcpl.h5 tests/h5.ext/fcpl.py)
pyre_test_python_cleanup(h5_ext_gcpl.h5 tests/h5.ext/gcpl.py)
pyre_test_python_cleanup(h5_ext_lcpl.h5 tests/h5.ext/lcpl.py)
pyre_test_python_cleanup(h5_ext_mosaic.h5 tests/h5.ext/mosaic.py)
pyre_test_python_cleanup(read_chunk_cache.h5 tests/h5.ext/read_chunk_cache.py)
pyre_test_python_cleanup(dapl_chunk_cache.h5 tests/h5.ext/dapl_chunk_cache.py)
pyre_test_python_cleanup(chunk_table.h5 tests/h5.ext/chunk_table.py)
pyre_test_python_cleanup(direct_chunk.h5 tests/h5.ext/direct_chunk.py)
pyre_test_python_cleanup(strided_tile.h5 tests/h5.ext/strided_tile.py)
pyre_test_python_cleanup(transfer_list.h5 tests/h5.ext/transfer_list.py)


# end of file
