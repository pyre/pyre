# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# rendering functions
log ?= echo
# indentation
log.halfdent = "  "
log.indent = "    "

# sections
log.sec = \
    $(log) \
    $(palette.section.name)$(1)$(palette.normal): $(2)

# variables
log.var = \
    $(log) \
    $(palette.variable.name)$(log.indent)$(1)$(palette.normal) \
    = \
    $(palette.variable.value)$(2)$(palette.normal)

# commands and targets
log.help = \
    $(log) \
    $(palette.lavender)$(log.indent)$(1)$(palette.normal) \
    : \
    $(palette.normal)$(2)$(palette.normal)

# text
log.info = \
    $(log) \
    $(palette.info)"  [info]"$(palette.normal) \
    $(palette.info)$(1)$(palette.normal) \

log.warning = \
    $(log) \
    $(palette.warning)"  [warning]"$(palette.normal) \
    $(palette.warning)$(1)$(palette.normal) \

log.error = \
    $(log) \
    $(palette.error)"  [error]"$(palette.normal) \
    $(palette.error)$(1)$(palette.normal) \

log.debug = \
    $(log) \
    $(palette.debug)"  [debug]"$(palette.normal) \
    $(palette.debug)$(1)$(palette.normal) \

log.firewall = \
    $(log) \
    $(palette.firewall)"  [firewall]"$(palette.normal) \
    $(palette.firewall)$(1)$(palette.normal) \

# render a build action
log.asset = \
    $(log) \
    $(palette.asset)"  [$(1)]"$(palette.normal) \
    $(2)

log.action = \
    $(log) \
    $(palette.action)"  [$(1)]"$(palette.normal) \
    $(2)

log.action.attn = \
    $(log) \
    $(palette.attn)"  [$(1)]"$(palette.normal) \
    $(2)


# terminals that support the ansi color commands
terminals.ansi = ansi vt100 vt102 xterm xterm-color xterm-256color

# initialize the {TERM} environment variable
TERM ?= dumb
# colors
ifeq ($(TERM),${findstring $(mm.color)$(TERM),$(terminals.ansi)})
include make/log/ansi.mm
else
include make/log/dumb.mm
endif

# color database
include make/log/colordb.mm

# theme locations
log.themes.mm := $(mm.home)/make/log/$(mm.palette).mm
log.themes.user = $(user.config)/themes/$(mm.palette).mm
log.themes.project := $(project.config)/themes/$(mm.palette).mm

# assemble them in priority order and filter out locations that don't exist
log.themes := ${realpath $(log.themes.mm) $(log.themes.project) $(log.themes.user)}

# load the requested palette, and fall back to the built in one
include ${if $(log.themes),$(log.themes),make/log/builtin.mm}


# end of file
