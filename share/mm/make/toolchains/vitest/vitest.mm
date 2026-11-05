# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# vitest: a node-based unit test runner; it is installed once per environment, so a project's
# test suite never installs it. it follows the releases of its major version rather than a pinned
# one, so an update brings in fixes without anyone tending the pin; a new major version changes
# how suites are written, so moving to it is a deliberate edit of the manifest
toolchain.vitest.doc := "node unit test runner; runs modules without a browser"
toolchain.vitest.kind := node
toolchain.vitest.version := ^5


# install the toolchain: stage the manifest and fetch the newest release it allows
vitest.install:
	@${call log.sec,"vitest","installing the vitest toolchain $(toolchain.vitest.version)"}
	@${call log.action,"mkdir",$(toolchain.vitest.home)}
	$(mkdirp) $(toolchain.vitest.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/vitest/package.json $(toolchain.vitest.home)/package.json
	@${call log.action,"npm","install"}
	$(cd) $(toolchain.vitest.home) && npm install

# update the toolchain: re-stage the manifest, and move to the newest release it allows, past
# whatever the lock file of the last install recorded
vitest.update:
	@${call log.sec,"vitest","updating the vitest toolchain $(toolchain.vitest.version)"}
	@${call log.action,"mkdir",$(toolchain.vitest.home)}
	$(mkdirp) $(toolchain.vitest.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/vitest/package.json $(toolchain.vitest.home)/package.json
	@${call log.action,"npm","update"}
	$(cd) $(toolchain.vitest.home) && npm update


# end of file
