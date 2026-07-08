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

# N.B. the chroma bindings under tests/pyre.ext/chroma are registered in
# pyre_tests_chroma.cmake, alongside the rest of the chroma suite


# end of file
