# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# the list of encountered packages
webpacks ?=

# package constructor
#   usage: webpack.init {project} {pack}
define webpack.init
    # add this to the pile
    ${eval webpacks += $(2)}
    # save the project
    ${eval $(2).project := $(1)}
    # and its home
    ${eval $(2).home ?= $($(1).home)/}
    # the stem for generating package specific names
    ${eval $(2).stem ?= $($(1).stem)}
    # form the name
    ${eval $(2).name ?= $($(2).stem)}

    # the root of the package relative to the project home
    ${eval $(2).root ?= ux/$($(2).name)/}
    # the absolute path to the pack
    ${eval $(2).prefix ?= $($(2).home)$($(2).root)}

    # the name of the configuration directory
    ${eval $(2).config ?= config/}
    # the names of directories with static assets
    ${eval $(2).static ?= styles graphics fonts}
    # the names of chunks from the external dependencies
    ${eval $(2).chunks ?=}
    # directories to bundle
    ${eval $(2).bundle ?= $($(2).name).html client schema react}

    # the list of available directories with static assets
    ${eval $(2).source.static.present := ${call webpack.source.static.present,$(2)}}
    ${eval $(2).source.static.dirs := ${call webpack.source.static.dirs,$(2)}}
    ${eval $(2).source.static.assets := ${call webpack.source.static.assets,$(2)}}

    # the configuration files
    ${eval $(2).source.page ?= $($(2).prefix)$($(2).name).html}
    ${eval $(2).source.npm_config ?= $($(2).prefix)$($(2).config)package.json}
    ${eval $(2).source.babel_config ?= $($(2).prefix)$($(2).config)babelrc}
    ${eval $(2).source.webpack_config ?= $($(2).prefix)$($(2).config)webpack.js}
    ${eval $(2).source.ts_config ?= $($(2).prefix)$($(2).config)tsconfig.json}
    # the list of sources
    ${eval $(2).source.app.dirs := ${call webpack.source.app.dirs,$(2)}}
    ${eval $(2).source.app.sources := ${call webpack.source.app.sources,$(2)}}

    # build locations
    ${eval $(2).staging.prefix ?= $($(1).tmpdir)$($(2).name).ux/}
    ${eval $(2).staging.prefix.generated ?= $($(2).staging.prefix)build/}
    ${eval $(2).staging.page ?= $($(2).staging.prefix)$($(2).name).html}
    ${eval $(2).staging.npm_config ?= $($(2).staging.prefix)package.json}
    ${eval $(2).staging.babel_config ?= $($(2).staging.prefix).babelrc}
    ${eval $(2).staging.webpack_config ?= $($(2).staging.prefix)webpack.config.js}
    ${eval $(2).staging.ts_config ?= $($(2).staging.prefix)tsconfig.json}
    # the list of sources
    ${eval $(2).staging.app.dirs := ${call webpack.staging.app.dirs,$(2)}}
    ${eval $(2).staging.app.sources := ${call webpack.staging.app.sources,$(2)}}
    # the bundle
    ${eval $(2).staging.generated.assets := ${call webpack.staging.generated.assets,$(2)}}

    # install locations
    ${eval $(2).install.prefix ?= $(builder.dest.etc)$($(2).name)/ux/}
    ${eval $(2).install.static.dirs ?= ${call webpack.install.static.dirs,$(2)}}
    ${eval $(2).install.static.assets ?= ${call webpack.install.static.assets,$(2)}}
    ${eval $(2).install.generated.assets ?= ${call webpack.install.generated.assets,$(2)}}

    # extern specifications seem to be required of all asset types, so here we go...
    ${eval $(2).extern ?=}
    ${eval $(2).extern.requested ?=}
    ${eval $(2).extern.supported ?=}
    ${eval $(2).extern.available ?=}

    # for the help system
    $(2).meta.categories := general layout source staging install
    # cetagory documentation
    $(2).metadoc.general := "general information about the pack"
    $(2).metadoc.layout := "information about the pack layout"
    $(2).metadoc.source := "information about the package sources"
    $(2).metadoc.staging := "information about the staging area"
    $(2).metadoc.install := "information about the installed assets"

    # build a list of all pack attributes by category

    # general: the list of attributes
    $(2).meta.general := project stem name
    # document each one
    $(2).metadoc.project := "the name of the project to which this pack belongs"
    $(2).metadoc.name := "the name of the pack"
    $(2).metadoc.stem := "the stem for generating product names"

    # layout: the list of attributes
    $(2).meta.layout := home root prefix config bundle source.static.present
    # document each one
    $(2).metadoc.home := "the project home directory"
    $(2).metadoc.root := "the root of the pack relative to the project home directory"
    $(2).metadoc.config := "the configuration directory"
    $(2).metadoc.bundle := "directories with code to be packed"
    $(2).metadoc.prefix := "the full path to the pack source code"
    $(2).metadoc.source.static.present := "directories with static assets"

    # sources: infromation about the sources
    $(2).meta.source := source.npm_config
    # document each one
    $(2).metadoc.source.npm_config := "the npm configuration file; typically called 'package.json'"

    # staging: the list of attributes
    $(2).meta.staging := staging.prefix staging.npm_config
    # document each one
    $(2).metadoc.staging.prefix := "the root of the staging directory"
    $(2).metadoc.staging.npm_config := "the npm configuration file"

    # install: the list of attributes
    $(2).meta.install := install.prefix
    # document each one
    $(2).metadoc.install.prefix := "the root of the asset installation directory"

# all done
endef


# methods
# trim non-existent directories from the list of static source
define webpack.source.static.present =
    ${strip
        ${foreach dir,$($(1).static),
            ${if ${realpath $($(1).prefix)$(dir)},$(dir),}
        }
    }
# all done
endef


# make a pile with all the directories with static assets
define webpack.source.static.dirs =
    ${strip
        ${addsuffix /,
           ${shell find ${realpath ${addprefix $($(1).prefix),$($(1).static)}} -type d}
        }
    }
# all done
endef


# make a pile with all the static assets
define webpack.source.static.assets =
    ${strip
        ${shell find ${addprefix $($(1).prefix),$($(1).source.static.present)} -type f}
    }
# all done
endef


# make a pile with the source directory layout
define webpack.source.app.dirs =
    ${strip
        ${addsuffix /,
            ${shell find ${realpath ${addprefix $($(1).prefix),$($(1).bundle)}} -type d}
        }
    }
# all done
endef


# make a pile with all the javascript sources
define webpack.source.app.sources =
    ${strip
        ${shell find ${realpath ${addprefix $($(1).prefix),$($(1).bundle)}} -type f -name \*.js}
        ${shell find ${realpath ${addprefix $($(1).prefix),$($(1).bundle)}} -type f -name \*.gql}
    }
# all done
endef


# assemble the list of staging directories with source files
define webpack.staging.app.dirs =
    ${subst $($(1).prefix),$($(1).staging.prefix),$($(1).source.app.dirs)}
# all done
endef


define webpack.staging.app.sources =
    ${subst $($(1).prefix),$($(1).staging.prefix),$($(1).source.app.sources)}
# all done
endef


define webpack.staging.generated.assets =
    ${addprefix $($(1).staging.prefix.generated)$($(1).name),.html .js}
# all done
endef


# assemble the list of install directories with static assets
define webpack.install.static.dirs =
    ${subst $($(1).prefix),$($(1).install.prefix),$($(1).source.static.dirs)}
# all done
endef


define webpack.install.static.assets =
    ${subst $($(1).prefix),$($(1).install.prefix),$($(1).source.static.assets)}
# all done
endef


define webpack.install.generated.assets =
    ${addprefix $($(1).install.prefix)$($(1).name),.html .js}
# all done
endef


# end of file
