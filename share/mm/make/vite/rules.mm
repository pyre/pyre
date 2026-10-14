# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# bundle info
vite.info: mm.banner
	@$(log) "known ux bundles: "$(palette.targets)$(vite.bundles)$(palette.normal)
	@$(log)
	@$(log) "to build one of them, use its name as a target"
	@$(log) "    mm ${firstword $(vite.bundles)}"
	@$(log)
	@$(log) "to get more information about a specific package, use"
	@$(log) "    mm ${firstword $(vite.bundles)}.info"
	@$(log)


# build the vite targets
#   usage: vite.workflows {bundle}
define vite.workflows
    # alias
    ${eval _bundle := $(1)}
    # build recipes
    ${call vite.workflows.build,$(_bundle)}
    # info recipes
    ${call vite.workflows.info,$(_bundle)}
    # help recipes
    ${call vite.workflows.help,$(_bundle)}
# all done
endef


# build targets
#  usage: vite.workflows.build {bundle}
define vite.workflows.build

    # alias
    ${eval _bundle := $(1)}

# the default target builds the production bundle and installs it
$(_bundle): $(_bundle).install
	@${call log.asset,"vite",$(_bundle)}

# stage the sources, configuration files, and node modules, after removing the staged files whose
# sources are gone
$(_bundle).stage: $(_bundle).prune $(_bundle).stage.config $(_bundle).stage.files $(_bundle).stage.modules

# the staged files that were moved, renamed, or deleted since the last build, by the record it left;
# relay and vite run on every build, so removing them is enough; files that the build itself writes,
# e.g. the relay artifacts, the node modules, and the bundle, are not on the record
${eval _stale := ${filter-out $($(_bundle).staged),${if ${wildcard $($(_bundle).staged.manifest)},${file <$($(_bundle).staged.manifest)},}}}

# remove them, along with the directories they leave empty in the staging area, and record what
# the bundle stages now
$(_bundle).prune: | $($(_bundle).staging.prefix)
	@${foreach file,$(_stale),${call log.action,"prune",${subst $($(_bundle).staging.prefix),,$(file)}};}
	${if $(_stale),$(rm.force) $(_stale)}
	${if $(_stale),${call rmdir.empty,${filter $($(_bundle).staging.prefix)%,${sort ${dir $(_stale)}}}}}
	$${file >$($(_bundle).staged.manifest),$($(_bundle).staged)}

# the graphql codegen pass that needs a separate step; relay does, houdini folds it into vite
$(_bundle).codegen: $(_bundle).stage
	${if ${filter relay,$($(_bundle).graphql)},@${call log.action,relay,$(_bundle)}; $(cd) $($(_bundle).staging.prefix) && npm run relay,@true}

# produce the production bundle inside the staging area
$(_bundle).bundle: $(_bundle).codegen
	@${call log.action,vite,$(_bundle)}
	$(cd) $($(_bundle).staging.prefix) && npm run build

# install the built assets to their destination, replacing what is there: vite names its chunks
# after a hash of their contents, so merging into the installed tree would keep every chunk of every
# earlier build; the new tree is copied next to the old one and then swapped in, so the installed
# tree is never half copied
$(_bundle).install: $(_bundle).bundle
	@${call log.action,install,$($(_bundle).install.prefix)}
	$(mkdirp) ${dir ${patsubst %/,%,$($(_bundle).install.prefix)}}
	$(rm.force-recurse) ${patsubst %/,%.new,$($(_bundle).install.prefix)}
	$(cp.r) $($(_bundle).staging.dist) ${patsubst %/,%.new,$($(_bundle).install.prefix)}
	$(rm.force-recurse) $($(_bundle).install.prefix)
	$(mv) ${patsubst %/,%.new,$($(_bundle).install.prefix)} ${patsubst %/,%,$($(_bundle).install.prefix)}

# run the vite dev server with HMR, serving from the staging area
$(_bundle).dev: $(_bundle).codegen
	@${call log.action,dev,$(_bundle)}
	$(cd) $($(_bundle).staging.prefix) && npm run dev

# clean up the staging and install areas, and the record of what was staged
$(_bundle).clean:
	@${call log.action,rm,$(_bundle)}
	$(rm.force-recurse) $($(_bundle).staging.prefix) $($(_bundle).install.prefix) $($(_bundle).staged.manifest)

# prime the configuration pile, just in case it's empty
$(_bundle).config::

# prime the pile of stage directories
$(_bundle).stage.dirs::
# prime the pile of staged sources
$(_bundle).stage.files::

# the rule that installs/updates the node modules
$(_bundle).stage.modules: $($(_bundle).stage.modules)
# and its implementation, selected by the build mode
${eval ${call $(vite.npm.install),$(_bundle)}}

# seed a clean install from the committed lock; recovers from npm instability in {dev}
$(_bundle).lock.seed: $(_bundle).stage.config | $($(_bundle).staging.prefix)
	@test -f $($(_bundle).source.npm_lock) || { ${call log.error,no committed lock to install from}; false; }
	@${call log.action,"cp",$($(_bundle).config.npm_lock)}
	$(cp) $($(_bundle).source.npm_lock) $($(_bundle).staging.npm_lock)
	@${call log.action,"npm ci",$(_bundle)}
	$(cd) $($(_bundle).staging.prefix); npm ci

# harvest the freshly-resolved lock back to the source tree for committing
$(_bundle).lock.harvest:
	@${call log.action,"cp",$($(_bundle).config.npm_lock)}
	$(cp) $($(_bundle).staging.npm_lock) $($(_bundle).source.npm_lock)

# make the rules that copy the configuration files to the staging area
${foreach file,
    $($(_bundle).config.all),
	${if ${realpath $($(_bundle).config.prefix)$(file)},
        ${eval ${call vite.workflows.config.stage,$(_bundle),$(file)}}
    }
}

# make the rules that create the source directories in the staging area
${foreach dir,
    $($(_bundle).sources.dirs),
    ${eval ${call vite.workflows.sources.stage.dir,$(_bundle),$(dir)}}
}
# make the rules that copy the source files to the staging area
${foreach file,
    $($(_bundle).sources.files),
    ${eval ${call vite.workflows.sources.stage.file,$(_bundle),$(file)}}
}

# make the rules that create the static asset directories in the staging area
${foreach dir,
    $($(_bundle).static.dirs),
    ${eval ${call vite.workflows.static.stage.dir,$(_bundle),$(dir)}}
}
# make the rules that copy the static asset files to the staging area
${foreach file,
    $($(_bundle).static.files),
    ${eval ${call vite.workflows.static.stage.file,$(_bundle),$(file)}}
}


# directories
# entry point, for interactive use
$(_bundle).directories: $(_bundle).staging.prefix

# the staging area entry point
$(_bundle).staging.prefix: | $($(_bundle).staging.prefix)
# and its implementation
$($(_bundle).staging.prefix): | $($($(_bundle).project).tmpdir)
	@${call log.action,"mkdir",$$@}
	$(mkdirp) $$@

# all done
endef


# stage the npm config (via the config rules), then resolve dependencies fresh
define vite.npm.install.fresh =
$($(1).stage.modules): $($(1).source.npm_config) | $($(1).staging.prefix)
	@${call log.action,"npm i",$(1)}
	$(cd) $($(1).staging.prefix); npm install
# all done
endef


# stage the committed lock, then install exactly from it
define vite.npm.install.locked =
$($(1).staging.npm_lock): $($(1).source.npm_lock) | $($(1).staging.prefix)
	@${call log.action,"cp",$($(1).config.npm_lock)}
	$(cp) $($(1).source.npm_lock) $($(1).staging.npm_lock)
$($(1).stage.modules): $($(1).source.npm_config) $($(1).staging.npm_lock) | $($(1).staging.prefix)
	@${call log.action,"npm ci",$(1)}
	$(cd) $($(1).staging.prefix); npm ci
# all done
endef


# the install strategy selected by the build mode
vite.npm.install := vite.npm.install.${if $(mode.npm.locked),locked,fresh}


# rule factory for creating individual staging source directories
#   usage: vite.workflows.sources.stage.dir {bundle} {dir}
define vite.workflows.sources.stage.dir =

    # local variables
    # aliases
    ${eval _bundle := $(1)}
    ${eval _dir := $(2)}
	# form the path relative to home of the sources
	${eval _naked := $(_dir:$($(_bundle).root.sources)%=%)}
	# the absolute path of the destination
	${eval _dst := $($(_bundle).staging.src)$(_naked)}

# add the directory to the pile
$(_bundle).stage.dirs:: $(_dst)

# make it
$(_dst):
	@${call log.action,"mkdir",$$@}
	$(mkdirp) $$@

# all done
endef


# rule factory for staging individual source files
#   usage: vite.workflows.sources.stage.file {bundle} {file}
define vite.workflows.sources.stage.file =

    # local variables
    # aliases
    ${eval _bundle := $(1)}
    ${eval _file := $(2)}
	# form the path relative to home of the sources
	${eval _naked := $(_file:$($(_bundle).root.sources)%=%)}
	# the absolute path of the source file
	${eval _src := $($(_bundle).prefix.sources)$(_naked)}
	# the absolute path of the destination
	${eval _dst := $($(_bundle).staging.src)$(_naked)}

# add the file to the bundle
$(_bundle).stage.files:: $(_dst)

# copy it
$(_dst): $(_src) | ${dir $(_dst)}
	@${call log.action,cp,$(_file)}
	$(cp) $(_src) $(_dst)

# all done
endef


# rule factory for individual configuration files
#   usage: vite.workflows.config.stage {bundle} {file}
define vite.workflows.config.stage =

    # local variables
    # aliases
    ${eval _bundle := $(1)}
    ${eval _file := $(2)}
    # the absolute path to this configuration file
    ${eval _src := $($(_bundle).config.prefix)$(file)}
    # the absolute path to the destination of this configuration file
    ${eval _dst := $($(_bundle).staging.prefix)$(_file)}
    # the label to use for the action log
    ${eval _nickname := ${subst $($(_bundle).prefix),,${_file}}}

# add the configuration file to the pile
$(_bundle).stage.config:: $(_dst)

# copy it
$(_dst): $(_src) | ${dir $(_dst)}
	@${call log.action,cp,$(_nickname)}
	$(sed) \
          -e "s:@PROJECT@:$($(1).project):g" \
          -e "s:@TITLE@:$($(1).project):g" \
          -e "s:@MAJOR@:$($($(1).project).major):g" \
          -e "s:@MINOR@:$($($(1).project).minor):g" \
          -e "s:@MICRO@:$($($(1).project).micro):g" \
          -e "s:@REVISION@:$($($(1).project).revision):g" \
          -e "s|@YEAR@|$($($(1).project).now.year)|g" \
          -e "s|@TODAY@|$($($(1).project).now.date)|g" \
          $(_src) > $(_dst)

# all done
endef


# rule factory for creating individual static asset directories
#   usage: vite.workflows.static.stage.dir {bundle} {dir}
define vite.workflows.static.stage.dir =

    # local variables
    # aliases
    ${eval _bundle := $(1)}
    ${eval _dir := $(2)}
	# form the path relative to home of the sources
	${eval _naked := $(_dir:$($(_bundle).root.static)%=%)}
	# the absolute path of the destination
	${eval _dst := $($(_bundle).staging.prefix)public/$(_naked)}

# add the directory to the pile
$(_bundle).stage.dirs:: $(_dst)

# make it
$(_dst):
	@${call log.action,"mkdir",$$@}
	$(mkdirp) $$@

# all done
endef


# rule factory for staging individual static assets
#   usage: vite.workflows.static.stage.file {bundle} {file}
define vite.workflows.static.stage.file =

    # local variables
    # aliases
    ${eval _bundle := $(1)}
    ${eval _file := $(2)}
	# form the path relative to home of the sources
	${eval _naked := $(_file:$($(_bundle).root.static)%=%)}
	# the absolute path of the source file
	${eval _src := $($(_bundle).prefix.static)$(_naked)}
	# the absolute path of the destination
	${eval _dst := $($(_bundle).staging.prefix)public/$(_naked)}

# add the file to the bundle
$(_bundle).stage.files:: $(_dst)

# copy it
$(_dst): $(_src) | ${dir $(_dst)}
	@${call log.action,cp,$(_file)}
	$(cp) $(_src) $(_dst)

# all done
endef


# info target
define vite.workflows.info =

    # alias
    ${eval _bundle := $(1)}

# the layout
$(_bundle).info:
	@${call log.sec,$(_bundle),"a bundle in project '$($(_bundle).project)'"}
	@$(log)
	@${call log.var,"name",$($(_bundle).name)}
	@${call log.var,"stem",$($(_bundle).stem)}
	@$(log)
	@${call log.var,"home",$($(_bundle).home)}
	@${call log.var,"root",$($(_bundle).root)}
	@${call log.var,$(log.indent)"prefix",$($(_bundle).prefix)}
	@${call log.var,"sources",$($(_bundle).root.sources)}
	@${call log.var,$(log.indent)"prefix",$($(_bundle).prefix.sources)}

# the configuration files
$(_bundle).info.config:
	@${call log.sec,$(_bundle),"a bundle in project '$($(_bundle).project)'"}
	@$(log)
	@${foreach var,$($(_bundle).config),$(log) $(log.indent)$(var);}

# all done
endef


# help targets
# usage: vite.workflows.help {bundle}
define vite.workflows.help
# make the recipe
$(1).help:
	@$(log)
	@${call log.sec,$(1),vite attributes}
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
