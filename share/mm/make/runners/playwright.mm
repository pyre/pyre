# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# playwright: a node-based end-to-end runner; it needs the client's node_modules, so it runs from
# a staging area; it discovers its own specs and starts servers through playwright.config.ts, so
# serial vs parallel routing and server fixtures are its concern, not ours
runner.playwright.prepare := staged
# invoke the executable directly rather than through {npx}: with the toolchain's {node_modules/.bin}
# on {PATH}, {playwright} resolves to the installed binary, and a missing one fails loudly instead
# of {npx} silently fetching a copy from the network
runner.playwright.launch := playwright test
runner.playwright.doc := "node end-to-end runner; owns the browsers and the servers under test"
runner.playwright.suite := "toolchain: declare {playwright} so mm wires NODE_PATH, PATH, and browsers"


# end of file
