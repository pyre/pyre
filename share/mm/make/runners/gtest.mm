# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# gtest: a compiled C++ runner, like catch2; mm compiles the suite's sources into one binary
# that self-registers its TEST()s and runs them; the suite supplies {extern := gtest}, and the
# runner links {gtest_main} to provide the entry point that discovers and runs the cases
runner.gtest.prepare := compiled
runner.gtest.language := c++
runner.gtest.libraries := gtest_main
runner.gtest.doc := "compiled C++ runner (GoogleTest); one binary from all sources; self-registers TEST()s"
runner.gtest.suite := "extern := gtest; c++.flags for the language standard"


# end of file
