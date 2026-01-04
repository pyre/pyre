# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-data for all projects
project.assetTypes ?= packages libraries extensions vite webpack verbatim
project.testTypes ?= tests
project.extraTypes ?= docker-images docs
# put it all together
project.contentTypes ?= $(project.assetTypes) $(project.testTypes) $(project.extraTypes)

# the project constructor
#   usage: project.init {project}
define project.init =
    # save the name
    ${eval $(1).name := $(1)}

     # content types
    ${eval $(1).assetTypes ?= $(project.assetTypes)}
    ${eval $(1).testTypes ?= $(project.testTypes)}
    ${eval $(1).extraTypes ?= $(project.extraTypes)}
    # put it all together
    ${eval $(1).contentTypes ?= $($(1).assetTypes) $($(1).testTypes) $($(1).extraTypes)}

    # meta-data
    ${eval $(1).major ?= ${repo.major}}
    ${eval $(1).minor ?= ${repo.minor}}
    ${eval $(1).micro ?= ${repo.micro}}
    ${eval $(1).revision ?= ${repo.revision}}
    ${eval $(1).ahead ?= ${repo.ahead}}
    ${eval $(1).now.year ?= $${strip $${shell $(date.year)}}}
    ${eval $(1).now.date ?= $${strip $${shell $(date.stamp)}}}

    # stem to use when building project specific filenames
    ${eval $(1).stem ?= $($(1).name)}

    # directories
    # the top-most directory where we found {.mm}
    ${eval $(1).home ?= $(project.home)}
    # the directory for build products
    ${eval $(1).bldroot ?= $(project.bldroot)}
    # the installation target directory
    ${eval $(1).prefix ?= $(project.prefix)}
    # the staging area for the build intermediate products
    ${eval $(1).tmpdir ?= $(builder.staging)$(1)/}

    # make
    # the directory from where {make} was invoked, i.e. the nearest parent with a local
    # makefile
    ${eval $(1).base ?= $(project.anchor)}
    # the user's {cwd} when they invoked mm
    ${eval $(1).origin ?= $(project.origin)}
    # the local makefile
    ${eval $(1).makefile ?= $(project.makefile)}
    # the project configuration file
    ${eval $(1).config ?= ${wildcard $(project.config)/$(1).mm}}

    # contents
    # assets
    ${eval $(1).contents ?=}
    # initialize the list of libraries
    ${eval $(1).libraries ?=}
    # the list of python extensions
    ${eval $(1).extensions ?=}
    # the list of python packages
    ${eval $(1).packages ?=}
    # ux bundles
    ${eval $(1).vite ?=}
    ${eval $(1).webpack ?=}
    # bulk content
    ${eval $(1).verbatim ?=}

    # extra
    # the list of docker containers
    ${eval $(1).docker-images ?=}
    # documentation
    ${eval $(1).docs ?=}

    # and the list of tests
    ${eval $(1).tests ?=}


    # dependencies
    # initialize the list of requested project dependencies
    ${eval $(1).extern.requested ?=}
    # the list of external dependencies that we have support for
    ${eval $(1).extern.supported ?=}
    # the list of dependencies in the order they affect the compiler command lines
    ${eval $(1).extern.available ?=}

    # cleanup
    ${eval  $(1).clean ?=}
    # documentation
    # the project metadata categories
    $(1).meta.categories := contents extern directories make

    # build a list of all the project attributes by category
    $(1).meta.directories := home bldroot prefix tmpdir
    $(1).meta.make := base origin makefile config
    $(1).meta.extern := extern.requested extern.supported extern.available
    $(1).meta.contents := $($(1).contentTypes)

    # category documentation
    $(1).metadoc.directories := "the layout of the build directories"
    $(1).metadoc.contents := "categories of build products"
    $(1).metadoc.extern := "dependencies to external packages"
    $(1).metadoc.make := "information about the builder"

    # document each one
    $(1).metadoc.name := "the name of the project"
    # directories
    $(1).metadoc.home := "the top level project directory"
    $(1).metadoc.bldroot := "the directory where build products get delivered"
    $(1).metadoc.prefix := "the install target directory"
    $(1).metadoc.tmpdir := "the directory with the intermediate build products"
    # make
    $(1).metadoc.base := "the directory from which mm invoked make"
    $(1).metadoc.origin := "the directory from which you invoked mm"
    $(1).metadoc.makefile := "the local makefile"
    $(1).metadoc.config := "the project configuration file"
    # dependencies
    $(1).metadoc.extern.requested := "requested dependencies"
    $(1).metadoc.extern.supported := "the dependencies for which there is mm support"
    $(1).metadoc.extern.available := "dependencies that were actually found and used"
    # contents
    $(1).metadoc.libraries := "the project libraries"
    $(1).metadoc.extensions := "the python extensions built by this project"
    $(1).metadoc.packages := "the python packages built by this project"
    $(1).metadoc.vite := "the vite ux bundles built by this project"
    $(1).metadoc.webpack := "the webpack ux bundles built by this project"
    $(1).metadoc.docker-images := "the docker images built by this project"
    $(1).metadoc.docs := "documentation for this project"
    $(1).metadoc.tests := "the project test suite"
    $(1).metadoc.verbatim := "project content that just get copied to the install location"
# all done
endef


# instantiate the project assets
#  usage: project.init.contents {project}
define project.init.contents =
    # go through all types of project assets
    ${foreach type,$($(1).contentTypes),
        # check whether the support file is loaded
        ${if ${findstring $(type),$(projects.contentTypes.imported)},,
            ${eval projects.contentTypes.imported += $(type)}
            ${foreach category,$(categories),
                ${eval -include make/$(type)/$(category).mm}
           }
        }
        # go through the assets of the given {type}
        ${foreach item, $($(1).$(type)),
            # invoke their constructors
            ${call $(type).init,$(1),$(item)}
        }
    }
# all done
endef


# scan through the project contents and collect all the requested dependencies
# usage project.extern.requested {project}
define project.extern.requested =
    ${sort
        ${foreach asset,$($(1).contents),$($(asset).extern.requested)}
    }
# all done
endef


# scan through the project contents and collect all the supported dependencies
# usage project.extern.supported {project}
define project.extern.supported =
    ${sort
        ${foreach asset,$($(1).contents),$($(asset).extern.supported)}
    }
# all done
endef


# scan through the project contents and collect all the available dependencies
# usage project.extern.available {project}
define project.extern.available =
    ${sort
        ${foreach asset,$($(1).contents),$($(asset).extern.available)}
    }
# all done
endef


# end of file
