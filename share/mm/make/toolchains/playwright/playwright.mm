# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# playwright: a node-based end-to-end browser-automation toolchain; it is installed once per
# environment and owns its own browser binaries, so a project's test suite never reinstalls it
toolchain.playwright.doc := "node end-to-end browser automation; owns its browsers"
toolchain.playwright.kind := node
toolchain.playwright.version := 1.60.0

# the location of the browser binaries; keeping them inside the toolchain makes the install
# self-contained, so {playwright.clean} removes everything and environments cannot drift
toolchain.playwright.browsers = $(toolchain.playwright.home)/browsers

# the consumer environment: a project using playwright must point it at these browsers, since they
# live inside the toolchain rather than the default per-user cache. {modules} is supplied generically
# by {toolchain.init} for {node} tools, so it is not repeated here. the {DEP0205} suppression is a
# stopgap: playwright 1.60 installs its TS loader through node's now-deprecated {module.register()},
# which recent node flags loudly on every worker; it is harmless and silenced narrowly (only this one
# code) until a playwright release that adopts {module.registerHooks()} lets us drop it
toolchain.playwright.env = \
    PLAYWRIGHT_BROWSERS_PATH=$(toolchain.playwright.browsers) \
    NODE_OPTIONS=--disable-warning=DEP0205


# install the toolchain: stage the pinned manifest, fetch the framework, then the browsers
playwright.install:
	@${call log.sec,"playwright","installing the playwright toolchain $(toolchain.playwright.version)"}
	@${call log.action,"mkdir",$(toolchain.playwright.home)}
	$(mkdirp) $(toolchain.playwright.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/playwright/package.json $(toolchain.playwright.home)/package.json
	@${call log.action,"npm","install"}
	$(cd) $(toolchain.playwright.home) && npm install
	@${call log.action,"playwright","browsers"}
	$(cd) $(toolchain.playwright.home) && PLAYWRIGHT_BROWSERS_PATH=$(toolchain.playwright.browsers) npx playwright install chromium

# update the toolchain: re-stage the pinned manifest and refresh the framework and browsers
playwright.update: playwright.install


# end of file
