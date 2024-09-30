# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# the list of docker images encountered
docker-images ?=

# the docker-images constructor
#  usage: docker-images.init {project instance} {image set}
define docker-images.init =
    # add it to the pile
    ${eval docker-images += $(2)}
    # save the project
    ${eval $(2).project := $(1)}
    # the image name; must be provided by the user
    ${eval $(2).name ?=}
    # use the name to derive the image tag
    ${eval $(2).tag ?= $($(2).project):$($(2).name)}

    # set the home
    ${eval $(2).home ?= $($(1).home)/}
    # the path to the docker folder relative to the project home
    ${eval $(2).root ?= etc/docker/}
    # the dockerfile
    ${eval $(2).dockerfile ?= $($(2).root)$($(2).name)/Dockerfile}

    # command line options
    ${eval $(2).build.options ?=}
    ${eval $(2).run.options ?=}
    ${eval $(2).launch.options ?=}

    # mounts
    ${eval $(2).mounts ?=}
    # extra directories specific to container use type
    ${eval $(2).run.mounts ?=}
    ${eval $(2).launch.mounts ?=}

    # default locations for directory mounts
    # from the host, one level above the project home directory
    ${eval $(2).mounts.source ?= ${realpath $($(2).home)..}/}
    # to the container, at /usr/local/src
    ${eval $(2).mounts.destination ?= /usr/local/src/}

    # the list of external dependencies as requested by the user
    ${eval $(2).extern ?=}
    # initialize the list of requested project dependencies
    ${eval $(2).extern.requested := $($(2).extern)}
    # the list of external dependencies that we have support for
    ${eval $(2).extern.supported ?= ${call extern.is.supported,$($(2).extern.requested)}}
    # the list of dependencies in the order they affect the compiler command lines
    ${eval $(2).extern.available ?= ${call extern.is.available,$($(2).extern.supported)}}

    # documentation
    $(2).meta.categories := general locations

    # category documentation
    $(2).metadoc.general := "general information"
    $(2).metadoc.locations := "the locations of the build products"

    # build a list of all project attributes by category
    $(2).meta.general := project name tag
    $(2).meta.locations := home root dockerfile

    # document each one
    # general
    $(2).metadoc.project := "the name of the project to which this docker image belongs"
    $(2).metadoc.name := "the name of the image"
    $(2).metadoc.tag := "the image tag"
    # locations
    $(2).metadoc.home := "the home of the project to which this docker image belongs"
    $(2).metadoc.root := "the relative path to the docker support"
    $(2).metadoc.dockerfile := "the location of the dockerfile"

# all done
endef


# end of file
