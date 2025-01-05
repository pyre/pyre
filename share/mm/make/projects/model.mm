# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# global variable that records content types as they are encountered to ensure that their support
# files are included only once
projects.contentTypes.imported :=

# hunt for projects among the contents of $(project.config), assuming that each file there is
# the configuration file for some project
projects ?= ${basename ${notdir ${wildcard $(project.config)/*.mm}}}

# load the project files
include ${wildcard $(project.config)/*.mm}


# bootstrap a project
define project.boot =
    # call the project constructor
    ${eval ${call project.init,$(1)}}
    # call the constructors of the various project assets
    ${eval ${call project.init.contents,$(1)}}
    # assemble the project contents
    ${eval $(1).contents := ${foreach asset,$($(1).contentTypes),$($(1).$(asset))}}
    # collect the requested external dependencies
    ${eval $(1).extern.requested := ${call project.extern.requested,$(1)}}
    # collect the supported external dependencies
    ${eval $(1).extern.supported := ${call project.extern.supported,$(1)}}
    # collect the available external dependencies
    ${eval $(1).extern.available := ${call project.extern.available,$(1)}}
# all done
endef


define project.boot.workflows =
    # build the project workflows
    ${eval ${call project.workflows,$(1)}}
    # build the asset workflows
    ${foreach category, $($(1).contentTypes),
        ${foreach asset, $($(1).$(category)),
            ${eval ${call $(category).workflows,$(asset)}}
        }
    }
# all done
endef


# bootstrap
# ${info --   project constructors}
${foreach project,$(projects), ${eval ${call project.boot,$(project)}}}

# ${info --   loading support for external packages}
#${foreach \
    #dependency, \
    #${sort ${foreach project,$(projects),$($(project).extern.available)}}, \
    #${eval include $(extern.mm)/$(dependency)/init.mm $(extern.mm)/$(dependency)/rules.mm} \
#}

projects.extern.requested := ${sort \
    ${foreach project,$(projects),$($(project).extern.available)} \
}

projects.extern.loaded := ${sort \
    ${call extern.load, $(projects.extern.requested)} \
}

# ${info --   project workflows}
${foreach project,$(projects), ${eval ${call project.boot.workflows,$(project)}}}

# ${info --   computing the default goal}
.DEFAULT_GOAL := ${if $(projects),projects,help}

# target that builds all known projects
projects: $(projects)

# target that runs all known tests
tests: projects ${if ${value testsuites},$(testsuites)}

# clean everything
clean: ${addsuffix .clean,$(projects) ${if ${value testsuites},$(testsuites)}}

# clean the test suites
tests.clean: ${if ${value testsuites},${addsuffix .clean,$(testsuites)}}

# tidy up
tidy:
	find $(project.home) -name \*~ -delete

# protect the above
.PHONY: projects tests clean


# end of file
