# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# the mm banner
palette.banner := $(palette.amber)

# help
# sections
palette.section.name := $(palette.amber)
# documentation
palette.topic := $(palette.lavender)
# variables
palette.variable.name := $(palette.sage)
palette.variable.value := $(palette.normal)

# list of known targets
palette.targets := $(palette.steel-blue)

# actions
palette.asset := $(palette.steel-blue)
palette.action := $(palette.lavender)
palette.attn := $(palette.purple)

# diagnostics
palette.info := ${call csi8,38,28}
palette.warning := ${call csi8,38,214}
palette.error := ${call csi8,38,196}
palette.debug := ${call csi8,38,75}
palette.firewall := $(palette.light-red)


# end of file
