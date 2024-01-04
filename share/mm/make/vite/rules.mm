# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


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

$(_bundle): $(_bundle).stage.config $(_bundle).stage.files $(_bundle).stage.modules
	@${call log.asset,"vite",$(_bundle)}

# prime the configuration pile, just in case it's empty
$(_bundle).config::

# prime the pile of stage directories
$(_bundle).stage.dirs::
# prime the pile of staged sources
$(_bundle).stage.files::

# the rule that installs/updates the node modules
$(_bundle).stage.modules: $($(_bundle).stage.modules)
# and its implementation
$($(_bundle).stage.modules): $($(_bundle).config.prefix)$($(_bundle).config.npm) | $($(_bundle).staging.prefix)
	@${call log.action,"npm",$($(_bundle).config.npm)}
	$(cd) $($(_bundle).staging.prefix); npm install

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
	${eval _dst := $($(_bundle).staging.prefix)src/$(_naked)}

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
	${eval _dst := $($(_bundle).staging.prefix)src/$(_naked)}

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
