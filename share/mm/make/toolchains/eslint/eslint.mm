# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# eslint: a node-based linter and formatter for javascript, with the rules that lay out the code
# and the ones that reflow its comments; it is installed once per environment, so a project never
# installs it. its parts follow the releases of their major versions rather than pinned ones, so
# an update brings in fixes without anyone tending the pins; a new major version changes how the
# rules are configured, so moving to it is a deliberate edit of the manifest
toolchain.eslint.doc := "node linter and formatter, with stylistic and comment length rules"
toolchain.eslint.kind := node
toolchain.eslint.version := ^10

# the module that hands the plugins to the configurations of projects, which can't import them by
# name from the toolchain; it lives in the home of the toolchain, next to its modules
toolchain.eslint.plugins = $(toolchain.eslint.home)/plugins.mjs
# it is staged after the modules are in place, so its presence proves the installation is whole
toolchain.eslint.sentinel = $(toolchain.eslint.plugins)
# the consumer environment: a project's configuration finds the module through this variable
toolchain.eslint.env = \
    MM_ESLINT_PLUGINS=$(toolchain.eslint.plugins)


# install the toolchain: stage the manifest, fetch the newest releases it allows, and stage the
# module with the plugins
eslint.install:
	@${call log.sec,"eslint","installing the eslint toolchain $(toolchain.eslint.version)"}
	@${call log.action,"mkdir",$(toolchain.eslint.home)}
	$(mkdirp) $(toolchain.eslint.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/eslint/package.json $(toolchain.eslint.home)/package.json
	@${call log.action,"npm","install"}
	$(cd) $(toolchain.eslint.home) && npm install
	@${call log.action,"stage","plugins.mjs"}
	$(cp) $(toolchains.mm)/eslint/plugins.mjs $(toolchain.eslint.plugins)

# update the toolchain: re-stage the manifest, move to the newest releases it allows, past whatever
# the lock file of the last install recorded, and re-stage the module with the plugins
eslint.update:
	@${call log.sec,"eslint","updating the eslint toolchain $(toolchain.eslint.version)"}
	@${call log.action,"mkdir",$(toolchain.eslint.home)}
	$(mkdirp) $(toolchain.eslint.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/eslint/package.json $(toolchain.eslint.home)/package.json
	@${call log.action,"npm","update"}
	$(cd) $(toolchain.eslint.home) && npm update
	@${call log.action,"stage","plugins.mjs"}
	$(cp) $(toolchains.mm)/eslint/plugins.mjs $(toolchain.eslint.plugins)


# end of file
