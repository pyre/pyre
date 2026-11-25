# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# swift-testing: apple's test library for swift. swift compiles a whole module at once, so mm
# compiles the suite's tests, the sources they test and an entry point into one program, which
# finds the tests marked {@Test} by itself, runs them, and exits with the verdict. the suite names
# the sources it tests in {<suite>.sources} and opts into the {xcode} toolchain, through which the
# compiler is reached
runner.swift-testing.prepare := module
runner.swift-testing.suffixes := .swift
runner.swift-testing.doc := "swift tests; one program from the tests and the sources they test"
runner.swift-testing.suite := "toolchain := xcode; sources := the files under test"

# the entry point of the program: the one the library provides for package managers, which runs
# every test it finds and turns the outcome into the exit code
runner.swift-testing.main := import Testing\nawait Testing.__swiftPMEntryPoint() as Never

# compile {sources} into the program {binary}, as the module {module}; the library and its
# macros live in the developer directory, which the {xcode} toolchain locates
#   usage: runner.swift-testing.compile {sources} {binary} {module}
runner.swift-testing.compile = \
    $(toolchain.xcode.env) $(toolchain.xcode.cli) --sdk macosx swiftc \
        -swift-version 6 $(toolchain.xcode.testing) -module-name $(3) -o $(2) $(1)


# end of file
