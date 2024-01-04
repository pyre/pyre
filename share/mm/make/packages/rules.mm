# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# package help
# make the recipe
packages.info: mm.banner
	@$(log) "known packages: "$(palette.targets)$(packages)$(palette.normal)
	@$(log)
	@$(log) "to build one of them, use its name as a target"
	@$(log) "    mm ${firstword $(packages)}"
	@$(log)
	@$(log) "to get more information about a specific package, use"
	@$(log) "    mm ${firstword $(packages)}.info"
	@$(log)

# build the package targets
#   usage: packages.workflows {package}
define packages.workflows
    # build recipes
    ${call package.workflows.build,$(1)}
    # info recipes
    ${call package.workflows.info,$(1)}
    # help recipes
    ${call package.workflows.help,$(1)}
# all done
endef


# build targets
# make the package specific targets
#   usage: package.workflows {package}
define package.workflows.build

# top level target
$(1): $(1).directories $(1).assets $($(1).extras)
	@${call log.asset,"pkg",$(1)}

# clean up
$(1).clean::

# second level targets
# make all relevant directories
$(1).directories: $($(1).staging.pycdirs) $($(1).staging.config.dirs)
# make all assets
$(1).assets: $(1).pyc ${if $($(1).meta),$(1).meta,} $(1).drivers $(1).config
# byte compile all sources
$(1).pyc: $($(1).staging.pyc)
# export all driver scripts
$(1).drivers: $($(1).staging.drivers)
# export all configuration files
$(1).config: $($(1).staging.config.dirs) $($(1).staging.config)

# individual assets
# make the directories with the byte compiled files
$($(1).staging.pycdirs):
	$(mkdirp) $$@
	@${call log.action,"mkdir",$$@}

# make the directories where the configuration files go
$($(1).staging.config.dirs):
	$(mkdirp) $$@
	@${call log.action,"mkdir",$$@}

# build the package meta-data, if available
${if $($(1).meta),${call package.workflows.meta,$(1)}}

# make rules that byte compile the sources
${foreach source,$($(1).sources),
    ${eval ${call package.workflows.pyc,$(1),$(source)}}
}

# make rules that copy the drivers
${foreach driver,$($(1).drivers),
    ${eval ${call package.workflows.driver,$(1),$(driver)}}
}

# make rules that copy the configuration files
${foreach config,$($(1).config.sources),
    ${eval ${call package.workflows.config,$(1),$(config)}}
}

# all done
endef


define package.workflows.meta =
# build the package meta-data file
$(1).meta: $($(1).staging.meta.pyc)

$(1).meta.source: $($(1).staging.meta.py)

# make the rule that compiles the package meta-data file
$($(1).staging.meta.pyc): $($(1).staging.meta.py) | ${dir $($(1).staging.meta)}
	@${call log.action,python,$($(1).root)$($(1).meta)}
	$($(compiler.python).compile) $($(1).staging.meta.py)
	$(rm) $($(1).staging.meta.py)

# make the rule that generates the package meta-data file
$($(1).staging.meta.py): $($(1).staging.meta) | ${dir $($(1).staging.meta.py)}
	@${call log.action,sed,$($(1).root)$($(1).meta)}
	$(sed) \
          -e "s:@PROJECT@:$($(1).project):g" \
          -e "s:@TITLE@:$($(1).project):g" \
          -e "s:@MAJOR@:$($($(1).project).major):g" \
          -e "s:@MINOR@:$($($(1).project).minor):g" \
          -e "s:@MICRO@:$($($(1).project).micro):g" \
          -e "s:@REVISION@:$($($(1).project).revision):g" \
          -e "s|@YEAR@|$($($(1).project).now.year)|g" \
          -e "s|@TODAY@|$($($(1).project).now.date)|g" \
          $($(1).staging.meta) > $($(1).staging.meta.py)

# mark the package meta-data product as phony so it gets made unconditionally
.PHONY: $($(1).staging.meta.pyc)

endef


# helpers
# make a target for each byte compiled file
#   usage: package.workflows.pyc {package} {source}
define package.workflows.pyc =

    # local variables
    # the absolute path to the source
    ${eval path.py := $(2)}
    # the absolute path to the byte compiled file
    ${eval path.pyc := ${call package.staging.pyc,$(1),$(path.py)}}

$(path.pyc): $(path.py) | ${dir $(path.pyc)}
	@${call log.action,python,${subst $($(1).home),,$(path.py)}}
	$($(compiler.python).compile) $(path.py)
	$(mv) $$(<:$(languages.python.sources)=$(languages.python.pyc)) $(path.pyc)

# all done
endef

# make a target for each driver
#   usage: package.workflows.driver {package} {source}
define package.workflows.driver =
    # local variables
    # the absolute path to the source
    ${eval path.source := $($(1).home)/$($(1).bin)$(2)}
    # the absolute path to the byte compiled file
    ${eval path.destination := ${call package.staging.driver,$(1),$(2)}}

$(path.destination): $(path.source) | ${dir $(path.destination)}
	@${call log.action,"cp",${subst $($(1).home),,$(path.source)}}
	$(cp) $(path.source) $(path.destination)

# all done
endef


# make a target for each configuration file
define package.workflows.config =
    # local variables
    # the absolute path to the source
    ${eval config.source := $(2)}
    # the absolute path to the destination
    ${eval config.destination := ${call package.staging.config.file,$(1),$(config.source)}}

$(config.destination): $(config.source) | ${dir $(config.destination)}
	@${call log.action,"cp",${subst $($(1).home),,$(config.source)}}
	$(cp) $(config.source) $(config.destination)

# all done
endef

# make a recipe to log the metadata of a specific package
# usage: package.workflows.info {package}
define package.workflows.info =
# make the recipe
$(1).info:
	@${call log.sec,$(1),"a package in project '$($(1).project)'"}
	@$(log)
	@$(log) "   ## MGA: FIXME ##"
	@$(log)
	@$(log) "for an explanation of their purpose, try"
	@$(log)
	@$(log) "    mm $(1).help"
	@$(log)
	@$(log) "related targets:"
	@$(log)
	@${call log.help,$(1).info.directories,"the layout of the source directories"}
	@${call log.help,$(1).info.sources,"the source files"}
	@${call log.help,$(1).info.pyc,"the byte compiled files"}
	@${call log.help,$(1).info.pycdirs,"the locations of the byte compiled files"}


# make a recipe that prints the directory layout of the sources of a package
$(1).info.directories:
	@${call log.sec,$(1),"a package in project '$($(1).project)'"}
	@${call log.sec,"  source directories",}
	@${foreach directory,$($(1).directories),$(log) $(log.indent)$(directory);}


# make a recipe that prints the set of sources that comprise a package
$(1).info.sources:
	@${call log.sec,$(1),"a package in project '$($(1).project)'"}
	@${call log.sec,"  sources",}
	@${foreach source,$($(1).sources),$(log) $(log.indent)$(source);}


# make a recipe that prints the set of byte compiled files that comprise a package
$(1).info.pyc:
	@${call log.sec,$(1),"a package in project '$($(1).project)'"}
	@${call log.sec,"  byte compiled files",}
	@${foreach pyc,$($(1).staging.pyc),$(log) $(log.indent)$(pyc);}


# make a recipe that prints the directories that house the package byte compiled files
$(1).info.pycdirs:
	@${call log.sec,$(1),"a package in project '$($(1).project)'"}
	@${call log.sec,"  directories with byte compiled files",}
	@${foreach dir,$($(1).staging.pycdirs),$(log) $(log.indent)$(dir);}

# make a recipe that shows how the package configuration files get built
$(1).info.config:
	@${call log.sec, $(1),"configuration files"}
	@${call log.var,"dir",$($(1).defaults)}
	@${call log.var,"root",$($(1).config.root)}
	@${call log.var,"destination",$($(1).staging.defaults)}
	@${call log.var,"stems",$($(1).config)}
	@${call log.var,"sources",$($(1).config.sources)}
	@${call log.var,"destinations",$($(1).staging.config)}
	@${call log.var,"directories",$($(1).staging.config.dirs)}


# make a recipe that prints the directory layout of the sources of a package
$(1).info.general:
	@${call log.sec,$(1),"a package in project '$($(1).project)'"}
	@${foreach var,$($(1).meta.general), \
            ${call log.var,$(var),$$($(1).$(var))}; \
         }

$(1).info.package:
	@echo $(builder.dest.pyc)$($(1).name)

$(1).info.meta:
	@${call log.sec, $(1),"package metadata"}
	@${call log.var,$(1).meta,$($(1).meta)}
	@${call log.var,$(1).staging.meta,$($(1).staging.meta)}
	@${call log.var,$(1).staging.meta.py,$($(1).staging.meta.py)}
	@${call log.var,$(1).staging.meta.pyc,$($(1).staging.meta.pyc)}

# all done
endef


# make a recipe to show the metadata documentation of a specific package
# usage: package.workflows.help {package}
define package.workflows.help =
# make the recipe
$(1).help:
	@$(log)
	@${call log.sec,$(1),package attributes}
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
