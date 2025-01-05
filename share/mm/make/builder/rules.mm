# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


builder.info: mm.banner
	@${call log.sec,"builder directory layout",}
	@${call log.sec,"  staging layout",}
	@${call log.var,"       tmp",$(builder.staging)}
	@${call log.sec,"  install layout",}
	@${call log.var,"    prefix",$(builder.dest.prefix)}
	@${call log.var,"       bin",$(builder.dest.bin)}
	@${call log.var,"       doc",$(builder.dest.doc)}
	@${call log.var,"       inc",$(builder.dest.inc)}
	@${call log.var,"       lib",$(builder.dest.lib)}
	@${call log.var,"     share",$(builder.dest.share)}
	@${call log.var,"       pyc",$(builder.dest.pyc)}

# targets that just print the value of the corresponding configuration setting
# useful at shell level
builder.info.tmp:
	@echo $(builder.staging)

builder.info.prefix:
	@echo $(builder.dest.prefix)

builder.info.bin:
	@echo $(builder.dest.bin)

builder.info.doc:
	@echo $(builder.dest.doc)

builder.info.inc:
	@echo $(builder.dest.inc)

builder.info.lib:
	@echo $(builder.dest.lib)

builder.info.share:
	@echo $(builder.dest.share)

builder.info.pyc:
	@echo $(builder.dest.pyc)

builder.info.staging:
	@echo $(builder.staging)


# create the builder targets
#   usage: builder.workflows
define builder.workflows

# rule to create the builder directories
$(builder.directories):
	$(mkdirp) $$@
	@${call log.action,"mkdir",$$@}

# all done
endef


# end of file
