# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# vitest: the vite-native unit and component runner; like playwright it needs node_modules and so
# runs from the staging area; {run} forces a single non-watch pass so the exit code is the verdict
runner.vitest.prepare := staged
runner.vitest.launch := npx vitest run
runner.vitest.doc := "vite-native unit and component runner; jsdom for DOM tests"
runner.vitest.suite := "stage.modules: the ux bundle's node_modules"


# end of file
