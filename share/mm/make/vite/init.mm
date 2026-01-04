# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the list of encountered bundles
vite.bundles ?=

# the constructor
#  usage: vite.init {project} {bundle}
define vite.init
    # alias the parameters
    ${eval _project := $(1)}
    ${eval _bundle := $(2)}

    # add the bundle to the pile
    ${eval vite.bundles += $(_bundle)}
    # remeber the project
    ${eval $(_bundle).project := $(_project)}
    # and its home
    ${eval $(_bundle).home ?= $($(_project).home)/}
    # the name of the bundle
    ${eval $(_bundle).name ?= $($(_project).name)}
    # the stem for generating project specific names
    ${eval $(_bundle).stem ?= $($(_project).stem)}
    # the pile of file suffixes that are recognized as sources
    ${eval $(_bundle).suffixes ?= *.ts *.tsx *.js *.jsx *.css *.gql *.svg}

    # the root of the bundle relative to the project home
    ${eval $(_bundle).root ?= ux/}
    # the absolute path to the bundle
    ${eval $(_bundle).prefix ?= $($(_bundle).home)$($(_bundle).root)}
    # the root of the sources relative to the project home
    ${eval $(_bundle).root.sources ?= $($(_bundle).root)$($(_bundle).name)/}
    # the absolute path to the sources
    ${eval $(_bundle).prefix.sources ?= $($(_bundle).home)$($(_bundle).root.sources)}
    # the root of the static assets relative to the project home
    ${eval $(_bundle).root.static ?= $($(_bundle).root)public/}
    # the absolute path to the sources
    ${eval $(_bundle).prefix.static ?= $($(_bundle).home)$($(_bundle).root.static)}


    # discover the source directories
    ${eval $(_bundle).sources.dirs ?= ${call vite.sources.dirs,$(_bundle)}}
    # and the source files they contain
    ${eval $(_bundle).sources.files ?= ${call vite.sources.files,$(_bundle)}}

    # discover the static asset directories
    ${eval $(_bundle).static.dirs ?= ${call vite.static.dirs,$(_bundle)}}
    # and the assets they contain
    ${eval $(_bundle).static.files ?= ${call vite.static.files,$(_bundle)}}

    # extern specifications seem to be required of all asset types, so here we go...
    ${eval $(_bundle).extern ?=}
    ${eval $(_bundle).extern.requested ?=}
    ${eval $(_bundle).extern.supported ?=}
    ${eval $(_bundle).extern.available ?=}

    # configuration files
    # the directory with the configuration files
    ${eval $(_bundle).config.root ?= config/}
    # the absolute path to the configuration directory
    ${eval $(_bundle).config.prefix ?= $($(_bundle).prefix)$($(_bundle).config.root)}
    # the various files by category
    ${eval $(_bundle).config.index ?= index.html}
    ${eval $(_bundle).config.npm ?= package.json}
    ${eval $(_bundle).config.ts ?= tsconfig.node.json tsconfig.json}
    ${eval $(_bundle).config.vite ?= vite.config.ts .eslintrc.cjs}
    ${eval $(_bundle).config.extra ?=}
    # put them all in one pile
    ${eval $(_bundle).config.all ?= \
        ${strip \
            $($(_bundle).config.index) \
            $($(_bundle).config.npm) \
            $($(_bundle).config.ts)  \
            $($(_bundle).config.vite) \
            $($(_bundle).config.extra) \
        } \
    }
    # and form absolute paths
    ${eval $(_bundle).config = ${call vite.config.source.files,$(_bundle)}}

    # the staging area
    ${eval $(_bundle).staging.prefix ?= $($(_project).tmpdir)$($(_bundle).stem).ux/}
    # the folder with the app source
    ${eval $(_bundle).staging.src ?= $($(_project).tmpdir)$($(_bundle).stem).ux/$($(_bundle).stem)/}
    # the folder with the node modules
    ${eval $(_bundle).stage.modules ?= $($(_bundle).staging.prefix)node_modules/}


    # for the help system
    $(2).meta.categories := general layout source staging install
    # cetagory documentation
    $(2).metadoc.general := "general information about the bundle"
    $(2).metadoc.layout := "information about the bundle layout"
    $(2).metadoc.source := "information about the package sources"
    $(2).metadoc.staging := "information about the staging area"
    $(2).metadoc.install := "information about the installed assets"

    # build a list of all bundle attributes by category
    # general: the list of attributes
    $(_bundle).meta.general := project stem name
    # document each one
    $(_bundle).metadoc.project := "the name of the project to which this bundle belongs"
    $(_bundle).metadoc.name := "the name of the bundle"
    $(_bundle).metadoc.stem := "the stem for generating product names"

    # layout: the list of attributes
    $(_bundle).meta.layout := home root prefix config bundle source.static.present
    # document each one
    $(_bundle).metadoc.home := "the project home directory"
    $(_bundle).metadoc.root := "the root of the bundle relative to the project home directory"
    $(_bundle).metadoc.config := "the configuration directory"
    $(_bundle).metadoc.bundle := "directories with code to be bundled"
    $(_bundle).metadoc.prefix := "the full path to the bundle source code"
    $(_bundle).metadoc.source.static.present := "directories with static assets"

    # sources: infromation about the sources
    $(_bundle).meta.source := source.npm_config
    # document each one
    $(_bundle).metadoc.source.npm_config := "the npm configuration file; typically called 'package.json'"

    # staging: the list of attributes
    $(_bundle).meta.staging := staging.prefix staging.npm_config
    # document each one
    $(_bundle).metadoc.staging.prefix := "the root of the staging directory"
    $(_bundle).metadoc.staging.npm_config := "the npm configuration file"

    # install: the list of attributes
    $(_bundle).meta.install := install.prefix
    # document each one
    $(_bundle).metadoc.install.prefix := "the root of the asset installation directory"

# all done
endef


# methods
# scan the source directory for its structure
#  usage: vite.sources.dir {bundle}
define vite.sources.dirs =
    ${strip
        ${if ${realpath $($(1).root.sources)},
            ${addsuffix /,
                ${shell find $($(1).root.sources:%/=%) -type d}
            }
        }
    }
# all done
endef


# scan the source directory for files
#  usage: vite.sources.files {bundle}
define vite.sources.files =
    ${strip
        ${if ${realpath $($(1).root.sources)},
            ${foreach
                suffix,
                $($(1).suffixes),
                ${shell find $($(1).root.sources:%/=%) -type f -name $(suffix)}
            }
        }
    }
# all done
endef


# form the absolute paths to the configuration files
#  usage: vite.config.source.files {bundle}
define vite.config.source.files =
    ${strip
        ${realpath
            ${addprefix $($(1).config.prefix), $($(1).config.all)}
        }
    }
# all done
endef


# form the absolute paths to the staged configuration files
#  usage: vite.config.stage.files {bundle}
define vite.config.stage.files =
    ${strip
        ${realpath
            ${addprefix $($(1).staging.prefix), $($(1).config.all)}
        }
    }
# all done
endef


# scan the static asset directory for its structure
#  usage: vite.static.dir {bundle}
define vite.static.dirs =
    ${strip
        ${if ${realpath $($(1).root.static)},
            ${addsuffix /,
                ${shell find $($(1).root.static:%/=%) -type d}
            }
        }
    }
# all done
endef


# scan the static asset directory for files
#  usage: vite.static.files {bundle}
define vite.static.files =
    ${strip
        ${if ${realpath $($(1).root.static)},
            ${shell find $($(1).root.static:%/=%) -type f}
        }
    }
# all done
endef


# end of file
