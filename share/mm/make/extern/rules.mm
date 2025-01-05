# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


extern.info:
	@${call log.sec,"extern","support for external packages"}
	@${call log.sec,"  locations",}
	@${call log.var,"built in",$(extern.mm)}
	@${call log.var,"user",$(extern.user)}
	@${call log.var,"project",$(extern.project)}
	@${call log.sec,"  packages",}
	@${call log.var,"supported",$(extern.supported)}
	@${call log.var,"available",$(extern.available)}
	@${call log.var,"requested",$(projects.extern.requested)}
	@${call log.var,"provided",$(projects.extern.loaded)}
	@${call log.sec,"  db",}
	@${call log.var,$(mm.pkgdb),$(builder.staging)pkg-$(mm.pkgdb).db}


# package database amanagement
define extern.workflows.pkgdb

	${eval _db := $(builder.staging)pkg-$(mm.pkgdb).db}

# attempt to load the package database
include $(_db)

extern.db.clean:
	@${call log.action,"rm",$(_db)}
	$(rm.force) $(_db)

# the rule that regenerates the package database
$(builder.staging)pkg-%.db: | $(builder.staging)
	@${call log.action,"pkgdb",$$@}
	@$(mm) --pkgdb=$$* --setup


endef

# end of file
