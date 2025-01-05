# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the list of encountered packages
packages ?=

# package constructor
#   usage: packages.init {project} {package}
define packages.init
    # add this to the pile
    ${eval packages += $(2)}
    # save the project
    ${eval $(2).project := $(1)}
    # and its home
    ${eval $(2).home ?= $($(1).home)/}
    # the stem for generating package specific names
    ${eval $(2).stem ?= $($(1).stem)}
    # form the name
    ${eval $(2).name ?= $($(2).stem)}
    # the configuration file stem
    ${eval $(2).config ?= $($(2).stem)}

    # hook for user supplied targets that must be built along with the main package target
    ${eval $(2).extras ?=}

    # external dependencies: packages do not typically list these explicitly, for now; their
    # meanings are defined in {make/projects/init.mm}
    ${eval $(2).extern ?=}
    ${eval $(2).extern.requested ?=}
    ${eval $(2).extern.supported ?=}
    ${eval $(2).extern.available ?=}

    # build locations
    # the package destination
    ${eval $(2).pycdir ?= $(builder.dest.pyc)$($(2).name)/}
    # the destination for drivers
    ${eval $(2).bindir ?= $(builder.dest.bin)}

    # artifacts
    # the root of the package relative to the project home
    ${eval $(2).root ?= pkg/$($(2).name)/}
    # the file with the package metadata, relative to the package root
    ${eval $(2).meta ?= meta.py.in}
    # the directory with the driver script sources relative to the project home
    ${eval $(2).bin ?= bin/}
    # the directory where extensions get parked, relative to the package root
    ${eval $(2).ext ?= ext/}
    # the directory with the configuration files, relative to the package root
    ${eval $(2).defaults ?= defaults/}

    # the absolute path to the package source tree
    ${eval $(2).prefix ?= $($(2).home)$($(2).root)}

    # directory exclusions
    ${eval $(2).directories.exclude ?=}
    # source exclusions
    ${eval $(2).sources.exclude ?=}

    # the directory structure
    ${eval $(2).directories ?= ${call package.directories,$(2)}}
    # the list of sources
    ${eval $(2).sources ?= ${call package.sources,$(2)}}
    # the list of scripts
    ${eval $(2).drivers ?=}

    # the home of the configuration files
    ${eval $(2).config.root ?= $($(1).home)/$($(2).defaults)$($(2).config)/}
    # the actual list of files derivable from the stems
    ${eval $(2).config.sources := ${call package.config,$(2)}}

    # derived artifacts
    # the compiled products
    ${eval $(2).staging.pyc ?= ${call package.pyc,$(2)}}
    # the set of directories that house the compiled products
    ${eval $(2).staging.pycdirs ?= ${call package.pycdirs,$(2)}}
    # the directory where extensions are delivered
    ${eval $(2).staging.ext ?= $($(2).pycdir)$($(2).ext)}

    # the directory where configuration files are delivevered
    ${eval $(2).staging.defaults ?= $(builder.dest.share)$($(2).config)/}
    # the list of files to deliver there
    ${eval $(2).staging.config ?= ${call package.staging.config,$(2),$($(2).config.sources)}}
    # and the list of directories that must exist
    ${eval $(2).staging.config.dirs ?= ${call package.staging.config.dirs,$(2)}}

    # the raw meta-data file
    ${eval $(2).staging.meta ?= $($(2).prefix)$($(2).meta)}
    # the generated meta-data file
    ${eval $(2).staging.meta.py ?= \
        ${if $($(2).staging.meta),$($(2).pycdir)${basename $($(2).meta)},}}
    # the byte-compiled meta-data file
    ${eval $(2).staging.meta.pyc ?= \
        ${if $($(2).staging.meta),${basename $($(2).staging.meta.py)}$(languages.python.pyc),}}

    # the drivers
    ${eval $(2).staging.drivers ?= ${addprefix $($(2).bindir),$($(2).drivers)}}

    # documentation
    $(2).meta.categories := general
    # category documentation
    $(2).metadoc.general := "general information"

    # build a list of all project attributes by category
    $(2).meta.general := project name stem

    # document each one
    # general
    $(2).metadoc.project := "the name of the project to which this package belongs"
    $(2).metadoc.name := "the name of the package"
    $(2).metadoc.stem := "the stem for generating product names"

# all done
endef


# methods

# build the set of source directories
#   usage: package.directories {package}
define package.directories =
    ${strip
        ${addsuffix /,
            ${filter-out
                ${foreach dir,$($(1).directories.exclude),
                    ${shell find ${realpath $($(1).prefix)$(dir)} -type d}
                },
                ${shell find ${realpath $($(1).prefix)} -type d}
            }
        }
    }
# all done
endef

# build the set of source files
#   usage: package.sources {package}
define package.sources =
    ${strip
        ${filter-out $($(1).sources.exclude),
            ${foreach directory, $($(1).directories),
                ${wildcard ${addprefix $(directory)*,$(languages.python.sources)}}
            }
        }
    }
# all done
endef


# build the set of byte compiled sources
#   usage: package.pyc {package}
define package.pyc =
    ${addprefix $($(1).pycdir),
        ${addsuffix $(languages.python.pyc),
            ${subst $($(1).prefix),,${basename $($(1).sources)}}
        }
    }
# all done
endef


# compute the absolute path to the byte compiled file given its source
#   usage: package.staging.pyc {package} {source}
define package.staging.pyc =
    $($(1).pycdir)${subst $($(1).prefix),,${basename $(2)}}$(languages.python.pyc)
# all done
endef


# compute the absolute path to the installed copy of a driver script
#   usage: package.staging.driver {package} {driver}
define package.staging.driver =
    $($(1).bindir)$(2)
# all done
endef


# build the set of directories with the byte compiled files
#   usage: package.staging.pycdirs {package}
define package.pycdirs =
    ${subst $($(1).prefix),$($(1).pycdir),$($(1).directories)}
# all done
endef


# build the set of configuration files
#   usage: package.config {package}
define package.config =
    ${strip
        ${eval root := ${realpath $($(1).config.root)}}
        ${if $(root),
           ${shell find $(root) -type f}
        }
    }
endef


# build the destination name for a configuration file
#   usage package.staging.config {package} {config-file}
define package.staging.config.file =
    ${addprefix $($(1).staging.defaults),
        ${subst $($(1).config.root),,$(2)}
    }
endef


# build the list of staged configuration files
#   usage package.staging.config {package} {config-files}
define package.staging.config =
    ${strip
        ${foreach file,$(2),${call package.staging.config.file,$(1),$(file)}}
    }
endef


# build the list of staging directories for configuration files
#   usage package.staging.config.directories {package}
define package.staging.config.dirs =
    ${strip
        ${sort ${dir $($(1).staging.config)}}
    }
endef


# end of file
