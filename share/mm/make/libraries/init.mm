# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the list of libraries encountered
libraries ?=

# the libraries constructor
#  usage: libraries.init {project instance} {library name}
define libraries.init =
    # add it to the pile
    ${eval libraries += $(2)}
    # save the project
    ${eval $(2).project := $(1)}
    # set the home
    ${eval $(2).home ?= $($(1).home)/}
    # the stem for generating library specific names; it gets used to build the archive name
    # and the include directory with the public headers
    ${eval $(2).stem ?= $($(1).stem)}
    # but the user may override either one explicitly
    ${eval $(2).libstem ?= $($(2).stem)}
    ${eval $(2).incstem ?= $($(2).stem)}
    # form the name
    ${eval $(2).name ?= lib$($(2).libstem)}
    # the name of the archive
    ${eval $(2).archive ?= $($(2).name)$(builder.ext.lib)}
    # the name of the dlink object with the CUDA device code
    ${eval $(2).dlink ?= $($(2).libstem).dlink}
    # the name of the shared object
    ${eval $(2).dll ?= $($(2).name)$(builder.ext.dll)}

    # the list of external dependencies as requested by the user
    ${eval $(2).extern ?=}
    # initialize the list of requested project dependencies
    ${eval $(2).extern.requested := $($(2).extern)}
    # the list of external dependencies that we have support for
    ${eval $(2).extern.supported ?= ${call extern.is.supported,$($(2).extern.requested)}}
    # the list of dependencies in the order they affect the compiler command lines
    ${eval $(2).extern.available ?= ${call extern.is.available,$($(2).extern.supported)}}

    # a list of additional prerequisites for the top target
    ${eval $(2).prerequisites ?=}

    # build locations
    # the destination for the archive
    ${eval $(2).libdir ?= $(builder.dest.lib)}
    # the destination for the public headers
    ${eval $(2).incdir ?= $(builder.dest.inc)$($(2).incstem)/}
    # the location of the build transients
    ${eval $(2).tmpdir ?= $($(1).tmpdir)$($(2).name)/}

    # artifacts
    # the root of the library source tree relative to the project home
    ${eval $(2).root ?= lib/$($(2).stem)/}
    # a list of extra headers and sources that don't match any pattern
    ${eval $(2).headers.extra ?=}
    ${eval $(2).sources.extra ?=}
    # a list of files with library repo metadata that require expansion; relative to {root}
    ${eval $(2).headers.autogen ?=}
    ${eval $(2).sources.autogen ?=}
    ${eval $(2).files.autogen ?= ${basename $($(2).headers.autogen) $($(2).sources.autogen)}}
    # the substitution table: space separated "in|out" pairs
    ${eval $(2).autogen ?=}

    # the absolute path to the library source tree
    ${eval $(2).prefix ?= $($($(2).project).home)/$($(2).root)}
    # the path to the top level headers relative to the library prefix
    # these headers get deposited one level above {incdir}
    ${eval $(2).gateway ?=}

    # directory exclusions
    ${eval $(2).directories.exclude ?=}
    # source exclusions
    ${eval $(2).sources.exclude ?=}
    # header exclusions
    ${eval $(2).headers.exclude ?=}

    # the directory structure
    ${eval $(2).directories ?= ${call library.directories,$(2)}}
    # the list of sources
    ${eval $(2).sources ?= ${call library.sources,$(2)}}
    # the list of CUDA sources
    ${eval $(2).sources.cuda ?= ${call library.sources.cuda,$(2)}}
    # the gateway headers
    ${eval $(2).headers.gateway ?= ${call library.headers.gateway,$(2)}}
    # the public headers
    ${eval $(2).headers ?= ${call library.headers,$(2)}}

    # build the language specific option database
    ${eval $(2).languages ?= ${call library.languages,$(2)}}
    # initialize the option database for each source language
    ${call library.languages.options,$(2)}

    # derived artifacts
    # the compiled products
    $(2).staging.objects = $${call library.objects,$(2)}
    $(2).staging.objects.cuda = $${call library.objects.cuda,$(2)}
    # the archive
    $(2).staging.archive = $$($(2).libdir)$($(2).archive)
    # the shared object
    $(2).staging.dll = $$($(2).libdir)$($(2).dll)
    # the include directories in the staging area
    $(2).staging.incdirs = $${call library.staging.incdirs,$(2)}
    # the gateway headers in the staging area
    $(2).staging.headers.gateway = $${call library.staging.headers.gateway,$(2)}
    # the public headers in the staging area
    $(2).staging.headers = $${call library.staging.headers,$(2)}


    # options to use while building the library
    # compile time
    $(2).internal.flags ?=
    $(2).internal.defines ?=
    $(2).internal.incpath += ${realpath $($(2).root)/..}
    # link time
    $(2).internal.ldflags ?=
    $(2).internal.libpath ?=
    $(2).internal.rpath ?=
    $(2).internal.libraries ?=

    # implement the external protocol
    $(2).dir ?= ${abspath $($(2).libdir)..}
    # compile time
    $(2).flags ?=
    $(2).defines ?=
    $(2).incpath ?= $(builder.dest.inc) # note: NOT ($(2).incdir)
    # link time
    $(2).ldflags ?=
    $(2).libpath ?= ${if $($(2).sources),$(builder.dest.lib:%/=%),} # that's where we put it
    $(2).rpath ?= $$($(2).libpath)
    $(2).libraries ?= ${if $($(2).sources),$($(2).libstem),} # that's what we call it

    # documentation
    $(2).meta.categories := general extern locations artifacts derived external

    # category documentation
    $(2).metadoc.general := "general information"
    $(2).metadoc.extern := "dependencies to external packages"
    $(2).metadoc.locations := "the locations of the build products"
    $(2).metadoc.artifacts := "information about the sources"
    $(2).metadoc.derived := "the compiled products"
    $(2).metadoc.external := "how to compile and link against this library"

    # build a list of all project attributes by category
    $(2).meta.general := project name stem
    $(2).meta.extern := extern.requested extern.supported extern.available
    $(2).meta.locations := incdir libdir tmpdir
    $(2).meta.artifacts := root prefix directories sources headers
    $(2).meta.derived := staging.archive staging.objects staging.incdirs staging.headers
    $(2).meta.external := flags defines incpath ldflags libpath rpath libraries

    # document each one
    # general
    $(2).metadoc.project := "the name of the project to which this library belongs"
    $(2).metadoc.name := "the name of the library"
    $(2).metadoc.stem := "the stem for generating product names"
    # dependencies
    $(2).metadoc.extern.requested := "requested dependencies"
    $(2).metadoc.extern.supported := "the dependencies for which there is mm support"
    $(2).metadoc.extern.available := "dependencies that were actually found and used"
    # locations
    $(2).metadoc.libdir := "the destination of the archive"
    $(2).metadoc.incdir := "the destination of the public headers"
    $(2).metadoc.tmpdir = "the staging area for object modules"
    # artifacts
    $(2).metadoc.root := "the path to the library sources relative to the project directory"
    $(2).metadoc.prefix := "the absolute path to the root of the library source tree"
    $(2).metadoc.directories := "the source directory structure"
    $(2).metadoc.sources := "the archive sources"
    $(2).metadoc.headers := "the public headers"
    # derived
    $(2).metadoc.staging.archive = "the archive"
    $(2).metadoc.staging.objects = "the object modules"
    $(2).metadoc.staging.incdirs = "the header directory structure"
    $(2).metadoc.staging.headers = "the public headers files"
    # external
    $(2).metadoc.flags := "compiler flags"
    $(2).metadoc.defines := "preprocessor macros"
    $(2).metadoc.incpath := "tell the compiler where the headers are"
    $(2).metadoc.ldflags := "link time flags"
    $(2).metadoc.libpath := "the path to the archives"
    $(2).metadoc.rpath := "the rpath to the archives"
    $(2).metadoc.libraries := "the list of archives to place on the link line"

# all done
endef

# methods

# build the set of library directories
#   usage: library.directories {library}
define library.directories
    ${strip
        ${addsuffix /,
            ${filter-out
                ${foreach dir,$($(1).directories.exclude),
                    ${shell find ${realpath $($(1).prefix)/$(dir)} -type d}
                },
                ${shell find ${realpath $($(1).prefix)} -type d}
            }
        }
    }
endef

# build the set of archive sources
#   usage: library.sources {library}
define library.sources
    ${strip
        ${filter-out $($(1).sources.exclude),
            ${foreach directory, $($(1).directories),
                ${wildcard ${addprefix $(directory)*,$(languages.sources)}}
            }
        }
        ${addprefix $($(1).prefix),$($(1).sources.extra)}
        ${addprefix $($(1).prefix),${basename $($(1).sources.autogen)}}
    }
endef

# build the set of CUDA sources
#   usage: library.sources.cuda {library}
define library.sources.cuda
    ${strip
        ${filter %$(languages.cuda.sources),$($(1).sources)}
    }
endef

# build the set of gateway headers
#   usage: library.headers {library}
define library.headers.gateway
    ${addprefix $($(1).prefix),$($(1).gateway)}
endef


# build the set of archive headers
#   usage: library.headers {library}
define library.headers
    ${strip
        ${filter-out $($(1).headers.exclude) $($(1).headers.gateway),
            ${foreach directory, $($(1).directories),
                ${wildcard ${addprefix $(directory)*,$(languages.headers)}}
            }
        }
        ${addprefix $($(1).prefix),$($(1).headers.extra)}
        ${addprefix $($(1).prefix),${basename $($(1).headers.autogen)}}
    }
endef


# build the set of archive objects
#   usage: library.objects {library}
define library.objects =
    ${addprefix $($(1).tmpdir),
        ${addsuffix $(builder.ext.obj),
            ${subst /,~,
                ${subst $($(1).prefix),,
                    ${foreach source, $($(1).sources),
                        ${basename $(source)}
                    }
                }
            }
            ${if $($(1).sources.cuda),$($(1).dlink)}
        }
    }
endef


# build the set of CUDA objects
#   usage: library.objects {library}
define library.objects.cuda =
    ${addprefix $($(1).tmpdir),
        ${addsuffix $(builder.ext.obj),
            ${subst /,~,
                ${subst $($(1).prefix),,
                    ${foreach source, $($(1).sources.cuda),
                        ${basename $(source)}
                    }
                }
            }
        }
    }
endef


# analyze the set of sources of a library and deduce the set of source languages
#   usage library.languages {library}
define library.languages =
    ${strip
        ${sort
            ${foreach extension,${sort ${suffix $($(1).sources)}},$(ext$(extension))}
        }
    }
endef


# build default values for the language specific option database
#   usage library.languages.options {library}
define library.languages.options =
    ${foreach language,$($(1).languages),
        ${foreach category,$(languages.$(language).categories),
            ${eval $(1).$(language).$(category) ?=}
        }
    }
endef


# build the name of an object given the name of a source
#   usage library.staging.object: {library} {source}
library.staging.object = \
    $($(1).tmpdir)${subst /,~,${basename ${subst $($(1).prefix),,$(2)}}}$(builder.ext.obj)


# build the list of staging directories for the public headers
#   usage: library.staging.incdirs {library}
define library.staging.incdirs
    ${strip
        ${subst $($(1).prefix),$($(1).incdir),
            ${sort ${dir $($(1).headers) $($(1).headers.gateway)}}
        }
    }
endef


# build the path of the staging directory for a public header
#   usage: library.staging.incdir {library} {header}
define library.staging.incdir
    ${dir
        ${subst $($(1).prefix),$($(1).incdir),$(2)}
    }
endef


# build the list of the paths of the library public headers
#   usage: library.staging.headers {library}
define library.staging.headers
    ${subst $($(1).prefix),$($(1).incdir),$($(1).headers)}
endef


# build the list of the paths of the library gateway headers
#   usage: library.staging.headers {library}
define library.staging.headers.gateway
    ${subst $($(1).prefix),${abspath $($(1).incdir)..}/,$($(1).headers.gateway)}
endef


# build the path to the library gateway header
#   usage: library.staging.header.gateway {library} {header}
define library.staging.header.gateway
    ${subst $($(1).prefix),${abspath $($(1).incdir)..}/,$(2)}
endef


# build the path to the library public header
#   usage: library.staging.header {library} {header}
define library.staging.header
    ${subst $($(1).prefix),$($(1).incdir),$(2)}
endef


# build the set of library external dependencies requested by the user
#  usage library.extern.requested {library}
define library.extern.requested =
    ${strip $($(1).extern)}
endef


# end of file
