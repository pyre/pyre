# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# vitest: the vite-native unit and component runner; like playwright it needs node_modules and so
# runs from the staging area; {run} forces a single non-watch pass so the exit code is the verdict
runner.vitest.prepare := staged
# invoke the executable directly rather than through {npx}: with the toolchain's {node_modules/.bin}
# on {PATH}, {vitest} resolves to the installed binary, and a missing one fails loudly instead of
# {npx} silently fetching a copy from the network; the tests find {describe}, {test} and {expect}
# as globals, since an import of {vitest} from a staged test would look for it among the modules
# of the code under test rather than in the toolchain
runner.vitest.launch := vitest run --globals
runner.vitest.doc := "vite-native unit and component runner; jsdom for DOM tests"
runner.vitest.suite := "toolchain: declare {vitest}; stage.modules: the modules of the code under test"


# end of file
