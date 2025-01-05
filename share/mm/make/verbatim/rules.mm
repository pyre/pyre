# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# bootstrap
define verbatim.workflows =
    # build recipes
    ${call verbatim.workflows.build,$(1)}
    # info recipes: show values
    ${call verbatim.workflows.info,$(1)}
    # help recipes: show documentation
    ${call verbatim.workflows.help,$(1)}
# all done
endef


# copy file verbatim
define verbatim.workflows.build =

# the top level target
$(1): $($(1).staging.assets)
	@${call log.asset,"vrb",$(1)}

# the destination folder
$($(1).staging):
	$(mkdirp) $$@
	@${call log.action,"mkdir",$$@}

# make targets for the staging directories
$($(1).staging.directories):
	$(mkdirp) $$@
	@${call log.action,"mkdir",$$@}

# make targets for individual files
${foreach asset,$($(1).assets),${call verbatim.workflows.asset,$(1),$(asset)}}

$(1).clean::

# all done
endef


# function that builds the rule that connects installed verbatim assets to their sources
#  usage: verbatim.workflows.asset {verbatim} {asset}
define verbatim.workflows.asset =

    # local variables
	${eval _src := $(2)}
	${eval _dst := ${subst $($(1).prefix),$($(1).staging),$(_src)}}
	${eval _dstdir := ${dir $(_dst)}}

$(_dst): $(_src) | $(_dstdir)
	$(cp) $$< $$@
	@${call log.action,"cp",${subst $($(1).home),,$(_src)}}

# all done
endef

#
define verbatim.workflows.info =
# make the recipe with the overall info
$(1).info:
	@${call log.sec,$(1),"verbatim content in project '$($(1).project)'"}
	@$(log)
	${call log.var,"home",$($(1).home)}
	${call log.var,"root",$($(1).root)}
	${call log.var,"prefix",$($(1).prefix)}
	${call log.var,"destination",$($(1).staging)}

# show the complete list of source files
$(1).info.files:
	@${call log.sec,$(1),"source files"}
	@${foreach asset,$($(1).assets),$(log) $(log.indent)$(asset);}

# show the complete list of staged files
$(1).info.staged.files:
	@${call log.sec,$(1),"staged files"}
	@${foreach asset,$($(1).staging.assets),$(log) $(log.indent)$(asset);}

# show the complete list of source files
$(1).info.directories:
	@${call log.sec,$(1),"source directories"}
	@${foreach asset,$($(1).directories),$(log) $(log.indent)$(asset);}

# show the complete list of staged files
$(1).info.staged.directories:
	@${call log.sec,$(1),"staged directories"}
	@${foreach asset,$($(1).staging.directories),$(log) $(log.indent)$(asset);}

# all done
endef


#
define verbatim.workflows.help =
# make the recipe
$(1).help:
	@$(log)
	@${call log.sec,$(1),verbatim}
	@$(log)

# all done
endef


# end of file
