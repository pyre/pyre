# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# pytest: the python test runner; it runs in place and discovers test_*.py itself, against the
# package the suite depends on (already importable in the active environment), so it needs no
# staging
runner.pytest.prepare := plain
runner.pytest.launch := pytest
runner.pytest.doc := "the python test runner; discovers test_*.py and runs in place"
runner.pytest.suite := "prerequisites: the package under test"


# end of file
