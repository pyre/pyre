# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the location of the built-in toolchain definitions
toolchains.mm ?= $(mm.home)/make/toolchains

# the root under which toolchains get installed; the mm driver resolves this from the
# {toolchains} trait, keyed by the active environment so the installation is shared across
# every build context while still tracking where node and python come from; the fallback
# mirrors the driver's formula from the same driver-supplied variables, covering a direct
# {make} invocation that bypasses the driver
toolchains.home ?= $(user.home)/tools/mm/$(user.environment)/toolchains


# the toolchain constructor; fills in whatever a tool definition left unset and resolves the
# installation directory under the shared root
#   usage: toolchain.init {tool}
define toolchain.init =
    # the human readable description
    ${eval toolchain.$(1).doc ?=}
    # the ecosystem the tool belongs to; drives how the pin is stored and installed
    ${eval toolchain.$(1).kind ?= node}
    # the exact version to pin
    ${eval toolchain.$(1).version ?=}
    # the directory that holds both the installation and mm's configuration for the tool
    ${eval toolchain.$(1).home := $(toolchains.home)/$(1)}
    # the artifact whose presence proves the tool is installed and intact; only a {node} tool lives
    # under a home that mm owns, so the sentinel is meaningful there. a {vendor} tool is verified by
    # resolving its {cli} on the {PATH} instead, so it leaves this empty
    ${eval toolchain.$(1).sentinel ?= ${if ${filter node,$(toolchain.$(1).kind)},$(toolchain.$(1).home)/node_modules/.bin/$(1),}}

    # the consumer interface: what a project that declares it uses this tool needs in order to
    # reach the installation. a {node} tool contributes its {node_modules} to {NODE_PATH} so the
    # suite's own sources resolve their bare imports, and its {node_modules/.bin} to {PATH} so the
    # runner can invoke the tool's executable; other kinds contribute nothing here and rely entirely
    # on {env} below
    ${eval toolchain.$(1).modules ?= ${if ${filter node,$(toolchain.$(1).kind)},$(toolchain.$(1).home)/node_modules,}}
    ${eval toolchain.$(1).bin ?= ${if ${filter node,$(toolchain.$(1).kind)},$(toolchain.$(1).home)/node_modules/.bin,}}
    # the vendor's download/install page; a {vendor} tool's {install} recipe sends the user here
    # rather than fetching anything, since mm does not own these installations
    ${eval toolchain.$(1).url ?=}
    # the executable a consumer invokes. a {node} tool's binary lives in its own {bin}; a {vendor}
    # tool is resolved off the {PATH} as the bare command, overridable to an absolute path when the
    # tool is installed somewhere non-standard
    ${eval toolchain.$(1).cli ?= ${if ${filter node,$(toolchain.$(1).kind)},$(toolchain.$(1).bin)/$(1),$(1)}}
    # extra environment a consumer must set to use the tool, beyond {NODE_PATH} and {PATH}; tool
    # specific, so each definition fills it in (e.g. a browser path); empty when nothing more is needed
    ${eval toolchain.$(1).env ?=}
# all done
endef


# end of file
