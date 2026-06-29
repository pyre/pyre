# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the toolchain registry summary
toolchains.info:
	@${call log.sec,"toolchains","environment-level developer tools installed once per environment"}
	@${call log.sec,"  location",}
	@${call log.var,"root",$(toolchains.home)}
	@${call log.sec,"  available tools",}
	@${foreach tool,$(toolchains),${call log.var,$(tool),$(toolchain.$(tool).doc)};}
	@${call log.sec,"  actions",}
	@${call log.help,"<tool>.install","fetch and install it (a deliberate online action)"}
	@${call log.help,"<tool>.verify","check it is present; fails a build if it is missing"}
	@${call log.help,"<tool>.update","reinstall it against the pinned version"}
	@${call log.help,"<tool>.info","show its settings"}
	@${call log.help,"<tool>.clean","remove the installation"}


# make the universal recipes every toolchain provides: info, verify, clean. the bodies differ by
# {kind} — a {node} tool mm installs and owns, a {vendor} tool mm only locates — so each recipe
# dispatches to a {kind}-specific fragment. the install and update recipes are not universal; they
# live in each tool's own definition
#  usage: toolchain.workflows {tool}
define toolchain.workflows =

# report this tool's settings
$(1).info:
	@${call log.sec,$(1),$(toolchain.$(1).doc)}
	@${call log.var,kind,$(toolchain.$(1).kind)}
	@${call log.var,version,$$(toolchain.$(1).version)}
${call toolchain.info.$(toolchain.$(1).kind),$(1)}

# confirm the tool is present; if it isn't, fail with a one-line instruction so a build that
# depends on it stops with an actionable message instead of a cryptic error further downstream
$(1).verify:
${call toolchain.verify.$(toolchain.$(1).kind),$(1)}

# remove whatever mm is responsible for
$(1).clean:
${call toolchain.clean.$(toolchain.$(1).kind),$(1)}

# all done
endef


# the {node} fragments: mm installs the tool under a home it owns

# {node}: report the install location and the sentinel that proves it is intact
define toolchain.info.node =
	@${call log.var,home,$(toolchain.$(1).home)}
	@${call log.var,sentinel,$(toolchain.$(1).sentinel)}
endef

# {node}: the sentinel proves the install; a miss points the user at this tool's install recipe
define toolchain.verify.node =
	@test -e "$(toolchain.$(1).sentinel)" || ( \
	    ${call log.error,"the '$(1)' toolchain is not installed"} ; \
	    ${call log.info,"expected it under $(toolchain.$(1).home)"} ; \
	    ${call log.info,"install it with: mm $(1).install"} ; \
	    exit 1 \
	)
	@${call log.action,"verify","$(1) $(toolchain.$(1).version) is available"}
endef

# {node}: remove the entire installation so the next install starts from a clean slate
define toolchain.clean.node =
	@${call log.action,"rm",$(toolchain.$(1).home)}
	$(rm.force-recurse) $(toolchain.$(1).home)
endef


# the {vendor} fragments: a third party ships the tool; mm only locates and verifies it

# {vendor}: report the resolved command and the vendor's download page
define toolchain.info.vendor =
	@${call log.var,cli,$(toolchain.$(1).cli)}
	@${call log.var,url,$(toolchain.$(1).url)}
endef

# {vendor}: presence is decided by resolving the {cli} on the {PATH}; a miss sends the user to the
# vendor rather than to an install recipe, since mm cannot fetch the tool
define toolchain.verify.vendor =
	@command -v "$(toolchain.$(1).cli)" > /dev/null 2>&1 || ( \
	    ${call log.error,"the '$(1)' tool is not installed"} ; \
	    ${call log.info,"it is vendor-distributed; mm cannot install it for you"} ; \
	    ${call log.info,"download and install it from $(toolchain.$(1).url)"} ; \
	    exit 1 \
	)
	@${call log.action,"verify","$(1) is available"}
endef

# {vendor}: mm does not own the installation, so there is nothing for it to remove
define toolchain.clean.vendor =
	@${call log.action,"skip","$(1) is vendor-managed; nothing for mm to remove"}
endef


# end of file
