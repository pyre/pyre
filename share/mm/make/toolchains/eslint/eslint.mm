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


# install the toolchain: stage the manifest and fetch the newest releases it allows
eslint.install:
	@${call log.sec,"eslint","installing the eslint toolchain $(toolchain.eslint.version)"}
	@${call log.action,"mkdir",$(toolchain.eslint.home)}
	$(mkdirp) $(toolchain.eslint.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/eslint/package.json $(toolchain.eslint.home)/package.json
	@${call log.action,"npm","install"}
	$(cd) $(toolchain.eslint.home) && npm install

# update the toolchain: re-stage the manifest, and move to the newest releases it allows, past
# whatever the lock file of the last install recorded
eslint.update:
	@${call log.sec,"eslint","updating the eslint toolchain $(toolchain.eslint.version)"}
	@${call log.action,"mkdir",$(toolchain.eslint.home)}
	$(mkdirp) $(toolchain.eslint.home)
	@${call log.action,"stage","package.json"}
	$(cp) $(toolchains.mm)/eslint/package.json $(toolchain.eslint.home)/package.json
	@${call log.action,"npm","update"}
	$(cd) $(toolchain.eslint.home) && npm update


# end of file
