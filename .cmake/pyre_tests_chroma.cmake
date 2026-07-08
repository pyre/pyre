# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the chroma library test suite
pyre_test_driver(tests/chroma.lib/rgb/hsb.cc)
pyre_test_driver(tests/chroma.lib/rgb/hsl.cc)
pyre_test_driver(tests/chroma.lib/rgb/palette.cc)
pyre_test_driver(tests/chroma.lib/ansi/escapes.cc)

# the chroma python bindings test suite
pyre_test_python_testcase(tests/pyre.ext/chroma/sanity.py)
pyre_test_python_testcase(tests/pyre.ext/chroma/roundtrip.py)


# end of file
