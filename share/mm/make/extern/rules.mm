# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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


# the body of a per-package verification report, rendered as recipe lines; it is expanded
# only for packages whose {init.mm} has been loaded, so the marker variables it reads are
# guaranteed to be defined
define extern.verify.report =
	@${call log.var,"incpath","$($(1).incpath)"}
	@${call log.var,"header markers","$($(1).markers.headers)"}
	@${if ${call extern.markers.headers.missing,$(1)},${call log.error,"unresolved headers: ${call extern.markers.headers.missing,$(1)}"},${call log.info,"headers ok"}}
	@${call log.var,"libpath","$($(1).libpath)"}
	@${call log.var,"libraries","$($(1).libraries)"}
	@${if ${call extern.markers.libraries.missing,$(1)},${call log.error,"unresolved libraries: ${call extern.markers.libraries.missing,$(1)}"},${call log.info,"libraries ok"}}
	@${if ${call extern.markers.required.missing,$(1)},${call log.error,"unset required values: ${call extern.markers.required.missing,$(1)}"},:}
	@${if $($(1).dependencies),${call log.var,"dependencies","$($(1).dependencies)"},:}
	@${if ${call extern.deps.missing,$(1)},${call log.error,"unavailable dependencies: ${call extern.deps.missing,$(1)}"},${if $($(1).dependencies),${call log.info,"dependencies ok"},:}}
endef


# verify that a package's declared markers resolve against its fully-resolved include and
# library paths; this reads the effective make variables, so it honors anything the user
# overrode in their adhoc config, which a package-database-time check cannot see. only the
# project's loaded externs carry their marker declarations, so anything else gets a hint
extern.%.verify:
	@${call log.sec,"$*","marker verification"}
	${if ${filter $*,$(projects.extern.loaded)}, \
	    ${call extern.verify.report,$*}, \
	    @${call log.warning,"$* is not an active external here; add it to the .extern of an asset to verify it"}}


# verify every external the project actually loads, reported as a verified set and a broken set
extern.verify:
	@${call log.sec,"extern","marker verification"}
	@${call log.var,"verified","$(extern.markers.ok)"}
	@${call log.var,"broken","$(extern.markers.broken)"}


# package database management
define extern.workflows.pkgdb

	${eval _db := $(builder.staging)pkg-$(mm.pkgdb).db}

# attempt to load the package database
include $(_db)

# for conda, warn if the active environment differs from the one used to build the database;
# guard on {conda.environment} being set: if it's empty the db is being rebuilt and there
# is nothing to compare against yet
${if ${filter conda,$(mm.pkgdb)}, \
    ${if $(conda.environment), \
        ${if ${filter-out $(conda.environment),$(user.environment)}, \
            ${warning conda environment mismatch: database was built for '$(conda.environment)', current is '$(user.environment)'} \
        } \
    } \
}

extern.db.info:
	@${call log.sec,"extern.db","the active package database"}
	@${call log.var,"manager",$(mm.pkgdb)}
	@${call log.var,"location",$(_db)}
	@${if $(conda.prefix),${call log.sec,"  conda",},:}
	@${if $(conda.prefix),${call log.var,"prefix",$(conda.prefix)},:}
	@${if $(conda.environment),${call log.var,"environment",$(conda.environment)},:}

extern.db.clean:
	@${call log.action,"rm",$(_db)}
	$(rm.force) $(_db)

# the rule that regenerates the package database
$(builder.staging)pkg-%.db: | $(builder.staging)
	@${call log.action,"pkgdb",$$@}
	@$(mm) --pkgdb=$$* --setup


endef

# end of file
