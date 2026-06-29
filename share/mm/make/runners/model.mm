# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the registry of known test runners
runners := playwright vitest pytest catch2 gtest

# load each runner's description
include $(runners:%=make/runners/%.mm)

# fill in defaults for anything a runner left unset, so the workflow can reference them safely
${foreach runner,$(runners), \
    ${eval runner.$(runner).prepare ?= plain} \
    ${eval runner.$(runner).launch ?=} \
    ${eval runner.$(runner).argv ?=} \
    ${eval runner.$(runner).env ?=} \
    ${eval runner.$(runner).language ?=} \
    ${eval runner.$(runner).libraries ?=} \
    ${eval runner.$(runner).doc ?=} \
    ${eval runner.$(runner).suite ?=} \
}

# build the per-runner info recipes
${foreach runner,$(runners),${eval ${call runner.recipes.info,$(runner)}}}


# end of file
