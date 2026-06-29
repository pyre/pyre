# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# catch2: a compiled C++ runner; mm compiles all of the suite's sources into a single binary that
# self-registers its TEST_CASEs, then runs it once; the suite supplies {extern := catch2} so the
# Catch2 headers and library land on the command lines, and the runner links {Catch2Main} to
# provide the entry point
runner.catch2.prepare := compiled
runner.catch2.language := c++
runner.catch2.libraries := Catch2Main
runner.catch2.doc := "compiled C++ runner; one binary from all sources; self-registers TEST_CASEs"
runner.catch2.suite := "extern := catch2; c++.flags for the language standard"


# end of file
