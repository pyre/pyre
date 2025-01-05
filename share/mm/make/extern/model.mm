# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the list of special packages that don't need actual install locations to be available
fortran.self := true

# initialize the pile of external packages
extern :=

# set up the management of the package database
${eval ${call extern.workflows.pkgdb}}

# the locations where package definitions may live
extern.mm ?= $(mm.extern)
extern.user ?= $(user.config)/extern
extern.project ?= $(project.config)/extern

# assemble them in priority order and filter out the locations that don't exist
extern.all := ${realpath ${extern.mm} ${extern.project} ${extern.user}}

# the set of known packages
extern.supported := \
    ${sort \
        ${foreach location, ${extern.all}, \
            ${subst $(location)/,, \
                ${shell find $(location)/* -type d -prune} \
            } \
        } \
    }

# the set of available packages, i.e. the ones we know where they live
extern.available := \
    ${foreach package, $(extern.supported), \
        ${if ${call extern.exists,$(package)},$(package),} \
    }

# load the configuration files for a set of dependencies
#   usage extern.load {dependencies}
define extern.load =
    ${foreach dep, $(1),
        ${foreach loc, ${extern.all},
            ${eval include ${realpath $(loc)/$(dep)/init.mm $(loc)/$(dep)/rules.mm}}
        }
	$(dep)
    }
endef


# end of file
