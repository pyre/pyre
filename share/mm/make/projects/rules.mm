# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# bootstrap
# make all project workflows
#   usage: project.workflows ${project}
define project.workflows =
    # the main project target
    ${call project.main,$(1)}
    # info workflows: show values
    ${call project.workflows.info,$(1)}
    # help workflows: show documentation
    ${call project.workflows.help,$(1)}
# all done
endef


# build targets
# target factory for building a project
#   usage: project.main {project}
define project.main =
# the main recipe
$(1): projects.boot $(1).directories $(1).assets

# the required directories
$(1).directories: $($(1).prefix) $($(1).tmpdir)

# the asset category target
$(1).assets: ${foreach type,$($(1).assetTypes),$(1).$(type)}

# asset targets by category
${foreach type,$($(1).contentTypes), \
    ${eval $(1).$(type): $($(1).$(type))} \
}

$($(1).tmpdir):
	$(mkdirp) $($(1).tmpdir)
	@${call log.action,"mkdir",$($(1).tmpdir)}

$(1).clean: ${addsuffix .clean,$($(1).contents)}
	$(rm.force-recurse) $($(1).tmpdir) $($(1).clean)
	@${call log.action,"rm",$($(1).tmpdir)}

# all done
endef


# targets common to all projects
$(project.prefix) :
	$(mkdirp) $@
	@${call log.action,"mkdir",$@}


# informational targets
# project help banner: list the known projects and tell the user what the next steps are
projects.info: mm.banner
	@$(log) "known projects: "$(palette.targets)$(projects)$(palette.normal)
	@$(log)
	@$(log) "to build one of them, use its name as a target"
	@$(log) "    mm ${firstword $(projects)}"
	@$(log)
	@$(log) "to get more information about a specific project, use"
	@$(log) "    mm ${firstword $(projects)}.info"
	@$(log)


# make a recipe to log the metadata of a specific project
# usage: project.workflows.info {project}
define project.workflows.info =
# make the recipe
$(1).info:
	@$(log)
	@${call log.sec,$(1),project attributes}
	@$(log)
	@${foreach category,$($(1).meta.categories),\
            ${call log.sec,"  "$(category),$($(1).metadoc.$(category))}; \
            ${foreach var,$($(1).meta.$(category)), \
                ${call log.var,$(1).$(var),$$($(1).$(var))}; \
             } \
        }
	@$(log)
	@$(log) "for an explanation of their purpose, try"
	@$(log)
	@$(log) "    mm $(1).help"
	@$(log)

# make a recipe that displays the project assets
$(1).info.contents:
	@${call log.sec,$(1),}
	@${call log.var,"contents",$$($(1).contents)}

# all done
endef


# make a recipe to show the metadata documentation of a specific project
# usage: project.workflows.info {project}
define project.workflows.help =
# make the recipe
$(1).help:
	@$(log)
	@${call log.sec,$(1),project attributes}
	@$(log)
	@${foreach category,$($(1).meta.categories),\
            ${call log.sec,"  "$(category),$($(1).metadoc.$(category))}; \
            ${foreach var,$($(1).meta.$(category)), \
                ${call log.help,$(1).$(var),$($(1).metadoc.$(var))}; \
             } \
        }
	@$(log)
	@$(log) "for a listing of their values, try"
	@$(log)
	@$(log) "    mm $(1).info"
	@$(log)
# all done
endef


# end of file
