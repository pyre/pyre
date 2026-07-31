# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the pyre extension sanity check
pyre_test_python_testcase(tests/pyre.ext/sanity.py)

# the timer bindings test suite
pyre_test_python_testcase(tests/pyre.ext/timers/sanity.py)
pyre_test_python_testcase(tests/pyre.ext/timers/wall_timer_instance.py)
pyre_test_python_testcase(tests/pyre.ext/timers/wall_timer_example.py)
pyre_test_python_testcase(tests/pyre.ext/timers/process_timer_instance.py)
pyre_test_python_testcase(tests/pyre.ext/timers/process_timer_example.py)

# the grid bindings test suite
pyre_test_python_testcase(tests/pyre.ext/grid/sanity.py)
pyre_test_python_testcase(tests/pyre.ext/grid/heap.py)
pyre_test_python_testcase(tests/pyre.ext/grid/access.py)
pyre_test_python_testcase(tests/pyre.ext/grid/map.py)
pyre_test_python_testcase(tests/pyre.ext/grid/mosaic.py)
pyre_test_python_testcase(tests/pyre.ext/grid/readonly.py)
pyre_test_python_testcase(tests/pyre.ext/grid/view.py)
pyre_test_python_testcase(tests/pyre.ext/grid/lifetime.py)

# the drivers leave their scratch products behind so they can be inspected; sweep them
add_test(NAME tests.pyre.ext.grid.map.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm grid_map_test.dat"
  )
add_test(NAME tests.pyre.ext.grid.readonly.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm grid_readonly_test.dat"
  )
set_property(TEST tests.pyre.ext.grid.map.cleanup PROPERTY
  DEPENDS tests.pyre.ext.grid.map.py
  )
set_property(TEST tests.pyre.ext.grid.readonly.cleanup PROPERTY
  DEPENDS tests.pyre.ext.grid.readonly.py
  )

# N.B. the chroma bindings under tests/pyre.ext/chroma are registered in
# pyre_tests_chroma.cmake, alongside the rest of the chroma suite


# end of file
