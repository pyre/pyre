# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# extension help
# make the recipe
extensions.info: mm.banner
	@$(log) "known extensions: "$(palette.targets)$(extensions)$(palette.normal)
	@$(log)
	@$(log) "to build one of them, use its name as a target"
	@$(log) "    mm ${firstword $(extensions)}"
	@$(log)
	@$(log) "to get more information about a specific extension, use"
	@$(log) "    mm ${firstword $(extensions)}.info"
	@$(log)


# bootstrap
# make the extension specific targets
define extensions.workflows =
    # the child library copied its extern list at construction time, before the global
    # resolve pass ran, so its dependency tiers miss anything induced, e.g. the mpi edge of
    # a parallel hdf5; resolve it here, where the package database is fully loaded
    ${call extern.resolve,$(1).lib}
    # build the recipes for the supporting library
    ${if $($(1).lib.sources),${call libraries.workflows,$(1).lib},}
    # build recipes
    ${call extension.workflows.build,$(1)}
    # info recipes: show values
    ${call extension.workflows.info,$(1)}
# all done
endef


# build targets
# target factory for building an extension
#   usage: extension.workflows.build {extension}
define extension.workflows.build =

# check whether we need to generate the module main initialization file, e.g. by running cython
${if ${filter-out $($(1).module.main),$($(1).module.init)},\
    ${call extension.workflows.makeinit,$(1)}, \
}

# if the module has capsules, make rules to export them
${if $($(1).capsule), ${call extension.workflows.capsule,$(1)},}

# the stubs can be made whenever their generator is installed; without it, asking for them gets
# an explanation
${if ${filter pybind11-stubgen,$($(1).extern)},${call extension.workflows.stubs,$(1)},${call extension.workflows.stubs.unavailable,$(1)}}

# the main recipe
$(1): $(1).prerequisites $(1).directories $(1).assets
	@${call log.asset,"ext",$(1)}

$(1).prerequisites: $($(1).prerequisites)

$(1).directories: $($(1).tmpdir)

$($(1).tmpdir):
	$(mkdirp) $$@
	@${call log.action,"mkdir",$$@}

$(1).assets: ${call extension.workflows.assets,$(1)}

$(1).extension: $($(1).module.so)

# the stubs of the module describe the one being replaced, so they go with it; a build that makes
# stubs writes new ones, any other build leaves none
$($(1).module.so): ${call extension.workflows.dependencies,$(1)}
	@${call log.action,"module",${subst $($(1).home),,$($(1).module.init)}}
	$(rm.force) $($(1).stubs.stamp)
	${call extension.stubs.remove,$(1)}
	${call languages.$($(1).module.language).ext,\
            $($(1).module.init), \
            $($(1).module.so), \
            $($(1).lib).$($(1).module.language) $($(1).lib) $($(1).wraps) $($(1).extern)}

# clean up, including any stubs an earlier build installed
$(1).clean:: $(1).lib.clean
	@${call log.action,"rm",$($(1).module.so)}
	$(rm.force) $($(1).module.so)
	$(rm.force-recurse) $($(1).stubs.tmpdir) $($(1).stubs.log) $($(1).stubs.stamp)
	${call extension.stubs.remove,$(1)}

# typically, extensions have no headers to export; this target is needed when an extension is
# used as a prerequisite
$(1).headers:

# typically, extensions have no archives to build; this target is needed when an extension is
# used as a prerequisite
$(1).archive:

# all done
endef


# build a list of the extension assets
#   usage: extension.workflows.assets {library}
define extension.workflows.assets =
${strip
    $($(1).pkg)
    ${if $($(1).lib.sources),$($(1).lib),}
    ${if $($(1).capsule),$(1).capsule}
    $(1).extension
    ${if $(project.stubs),${if ${filter pybind11-stubgen,$($(1).extern)},$(1).stubs}}
}
endef


# build a list of the dependencies of the extension module shared object
#   usage: extension.workflows.dependencies {extension}
define extension.workflows.dependencies =
${strip
    $($(1).module.init)
    ${if $($(1).lib.sources),$($($(1).lib).staging.archive)}
    ${foreach lib,$($(1).wraps),
        ${if $($(lib).sources),$($(lib).staging.archive) $($(lib).staging.dll)}
    }
}
endef


# build a rule to generate the extension {init} from its {main}, if necessary
#   usage: extension.workflows.makeinit {extension}
define extension.workflows.makeinit

    # alias the module
    ${eval module := $($(1).module.main)}
    # and the target
    ${eval module.target := $($(1).module.init)}
    # compute the path of the module relative to the project home
    ${eval module.relpath := ${subst $($(1).home),,$(module)}}
    # figure out the module language
    ${eval module.language := $(ext${suffix $($(1).module.main)})}

    # compute the directory structure of the module
    ${eval module.directories := ${addsuffix /,${shell find ${realpath ${dir $(module)}}}}}
    # compute the full set of sources of the module
    ${eval module.sources := \
        ${strip \
            ${foreach directory,$(module.directories), \
                ${wildcard \
                    ${addprefix \
                        $(directory)*,\
                        $(languages.$(module.language).sources) \
                            $(languages.$(module.language).headers) \
                    } \
                } \
            } \
        } \
    }

    # give the compiler access to the original location of the {main} module
    ${eval $(1).lib.incpath += ${dir $(module)}}

# build {init} from {main}
$($(1).module.init) : $(module.sources)
	@${call log.action,"$(module.language)",$(module.relpath)}
	${call languages.compile,$(module.language),$(module),$(module.target),}

# convenience target to build {init} from {main}
$(1).module.init : $(1).directories $($(1).module.init)

# remove {init}
$(1).module.init.clean :
	${rm.force} $($(1).module.init)

endef


# build rules that publish the extension capsules
#   usage: extension.workflows.capsule {extension}
define extension.workflows.capsule =
    # alias the source
    ${eval capsule.source := $($(1).prefix)$($(1).capsule)}
    # compute the destination directory
    ${eval capsule.incdir := ${strip \
        ${if $($(1).capsule.destination), \
            $(builder.dest.inc)$($(1).capsule.destination), \
            $($($(1).wraps).incdir) \
        } \
    }}
    # alias the destination
    ${eval capsule.destination := $(capsule.incdir)$($(1).capsule)}

$(1).capsule : $(capsule.destination)

$(capsule.destination) : $(capsule.incdir) $(capsule.source)
	$(cp) $(capsule.source) $(capsule.destination)
	@${call log.action,"cp",${subst $($(1).home),,$(capsule.source)}}

${if $($(1).wraps),,\
    ${eval $(capsule.incdir) : ; \
	$(mkdirp) $(capsule.incdir) ; ${call log.action,"mkdir",$(capsule.incdir)} \
    } \
}

endef


# build the rules that make the type stubs of an extension module
#   usage: extension.workflows.stubs {extension}
define extension.workflows.stubs =

# convenience target
$(1).stubs: $($(1).stubs.stamp)

# the generator imports the module from the prefix, so it waits for the module and its package,
# and it runs in the scratch area of the extension, where no source tree can answer the import.
# the stubs installed earlier go first, and the ones it writes take their place; names it cannot
# resolve leave holes in them, so their count is reported along with the log that lists them. a
# generator that fails leaves no stubs and no stamp, so the next build tries again
$($(1).stubs.stamp): $($(1).module.so) | $($(1).pkg) $($(1).tmpdir)
	$(rm.force-recurse) $($(1).stubs.tmpdir) $$@
	${call extension.stubs.remove,$(1)}
	if cd $($(1).tmpdir) && PYTHONPATH=$(builder.dest.pyc)${if ${value PYTHONPATH},:${value PYTHONPATH},} \
            $(pybind11-stubgen.driver) -o $($(1).stubs.tmpdir) $($(1).stubs.module) \
                > $($(1).stubs.log) 2>&1; then \
        $(cp.fr) $($(1).stubs.source). $($(1).stubs.destination); \
        touch $$@; \
        errors=`grep -c "\[  ERROR\]" $($(1).stubs.log)`; \
        if [ $$$$errors -eq 0 ]; then \
            ${call log.action,"pyi",$($(1).stubs.module)}; \
        else \
            ${call log.action.attn,"pyi","$($(1).stubs.module): $$$$errors unresolved; see $($(1).stubs.log)"}; \
        fi; \
    else \
        ${call log.action.attn,"pyi","$($(1).stubs.module): the generator failed; see $($(1).stubs.log)"}; \
    fi

endef


# build the rule that explains why the stubs of an extension module cannot be made
#   usage: extension.workflows.stubs.unavailable {extension}
define extension.workflows.stubs.unavailable =

# the generator is not installed
$(1).stubs:
	@${call log.warning,"$(1): no stubs; the generator pybind11-stubgen is not installed"}

endef


# remove the installed stubs of an extension module, in either of the forms the generator writes;
# the {stem} directory is the extension's own, since a package by that name would hide the module
#   usage: extension.stubs.remove {extension}
define extension.stubs.remove =
$(rm.force) $($(1).stubs.installed).pyi; if [ -d $($(1).stubs.installed) ]; then find $($(1).stubs.installed) -name "*.pyi" -delete; find $($(1).stubs.installed) -depth -type d -empty -delete; fi
endef


# make a recipe to log the metadata of a specific extension
# usage: extension.workflows.info {extension}
define extension.workflows.info =
# make the recipe
$(1).info:
	@${call log.sec,$(1),"an extension in project '$($(1).project)'"}
	@$(log)
	@${call log.var,home,$($(1).home)}
	@${call log.var,root,$($(1).root)}
	@${call log.var,prefix,$($(1).prefix)}
	@${call log.var,stem,$($(1).stem)}
	@${call log.var,name,$($(1).name)}
	@${call log.var,module,$($(1).module)}
	@${call log.var,shared object,$($(1).module.so)}
	@${call log.var,main,$($(1).module.main)}
	@${call log.var,init,$($(1).module.init)}
	@${call log.var,support archive,$($(1).lib.archive)}
	@${call log.var,stubs,${if ${filter pybind11-stubgen,$($(1).extern)},$($(1).stubs.installed),}}
# all done
endef


# end of file
