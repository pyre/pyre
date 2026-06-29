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
    # the bootstrap bundle, for projects that opt in
    ${if $($(1).boot.packages),${call project.workflows.boot,$(1)}}
# all done
endef


# bootstrap bundle
# target factory that assembles a project's pure-python sources into a zip archive, suitable
# for bootstrapping {mm} on a machine without {pyre}; only invoked for projects that declare a
# non-empty {boot.packages}
#
# the staging targets are independent and accumulative: each one refreshes only its own package
# subdirectory, so you can stage packages one at a time and bundle when ready
#   - {project}.boot.stage.{stem} : (re)stage a single package
#   - {project}.boot.stage        : stage every package
#   - {project}.boot.bundle       : zip whatever is currently staged
#   - {project}.boot              : wipe, stage every package, then bundle (a clean release)
#   - {project}.boot.clean        : discard the whole release directory
#   usage: project.workflows.boot {project}
define project.workflows.boot =

# the full release: wipe the staging area, stage every package, then bundle; the {.WAIT} keeps
# the wipe from racing the stagers under a parallel build (needs GNU make >= 4.4)
$(1).boot: $(1).boot.clean .WAIT $(1).boot.stage
	${call project.boot.zip,$(1)}

# bundle whatever is currently staged, without restaging anything
$(1).boot.bundle:
	${call project.boot.zip,$(1)}

# stage every package, leaving the bundling to the caller
$(1).boot.stage: ${foreach package,$($(1).boot.packages),$(1).boot.stage.$($(package).stem)}

# discard the entire release directory, for a clean slate
$(1).boot.clean:
	$(rm.force-recurse) $($(1).boot.root)

# one staging target per package
${foreach package,$($(1).boot.packages),${call project.boot.stage,$(1),$(package)}}

# none of these correspond to a file of the same name, so they always run
.PHONY: $(1).boot $(1).boot.bundle $(1).boot.stage $(1).boot.clean

endef


# zip the currently-staged contents into the archive, replacing any previous one
#   usage: project.boot.zip {project}
define project.boot.zip =
	$(rm.force) $($(1).boot.archive)
	cd $($(1).boot.contents) && $(zip) $(zip.flags.bundle) $($(1).boot.archive) .
	@${call log.asset,"boot",$($(1).boot.archive)}
endef


# stage a single package into its own subdirectory of the bundle contents
#   usage: project.boot.stage {project} {package}
# the wipe is scoped to this package's subdirectory, so staging one package never disturbs the
# others already sitting in the contents area
define project.boot.stage =

$(1).boot.stage.$($(2).stem):
	@${call log.action,"boot",$($(2).stem)}
	$(rm.force-recurse) $($(1).boot.contents)$($(2).stem)/
	$(mkdirp) $($(1).boot.contents)$($(2).stem)/
	$(rsync) --recursive --prune-empty-dirs \
            --include "*/" --include "*.py" --exclude "*" \
            $($(2).prefix) $($(1).boot.contents)$($(2).stem)/
	${call package.meta.expand,$(2),$($(2).prefix)$($(2).meta),$($(1).boot.contents)$($(2).stem)/meta.py}

.PHONY: $(1).boot.stage.$($(2).stem)

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
