# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the list of special packages that don't need actual install locations to be available
fortran.self := true

# initialize the pile of external packages
extern :=


# initialize the internal variables of the various support package managers
# conda
conda.prefix ?=
conda.environment ?=


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

# include one package's configuration exactly once, then descend into its {.dependencies}. the
# recursion follows {.dependencies} only after the package's own {init.mm} has been read, so an edge
# computed at load time (e.g. a parallel {hdf5} electing {mpi}) is already defined when we reach it.
# {markers.required} and its hint are opt-in, so they are defaulted to empty here — otherwise the
# marker checks reference an undefined variable and trip -warn-undefined. these defaults cannot be
# written as comments inside the {define} because comment text would leak into the expansion
#   usage: extern.load.one {package}
define extern.load.one =
    ${if ${filter $(1),$(extern.loaded)},,
        ${eval extern.loaded += $(1)}
        ${foreach loc, ${extern.all},
            ${eval include ${realpath $(loc)/$(1)/init.mm $(loc)/$(1)/rules.mm}}
        }
        ${eval $(1).markers.required ?=}
        ${eval $(1).markers.required.hint ?=}
        ${eval $(1).dependencies ?=}
        ${foreach dep, $($(1).dependencies),
            ${call extern.load.one,$(dep)}
        }
    }
endef


# load the configuration files for a set of dependencies and their transitive {.dependencies},
# returning the full set of packages actually loaded
#   usage extern.load {dependencies}
define extern.load =
    ${eval extern.loaded :=}
    ${foreach dep, $(1),
        ${call extern.load.one,$(dep)}
    }
    $(extern.loaded)
endef


# end of file
