# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the current build mode and the settings it resolves to
mode.info:
	@${call log.sec,"mode","the build mode and its resolved settings"}
	@${call log.var,current,$(project.mode)}
	@${call log.var,available,$(modes.available)}
	@${call log.sec,"  npm",}
	@${call log.var,locked,$(mode.npm.locked)}
	@${call log.sec,"  compiler",}
	@${call log.var,assertions,${if $(mode.compiler.assertions),yes,no}}
	@${call log.var,pinned,${if $(project.assertions),$(project.assertions),no}}
	@${call log.var,defines,$(mode.compiler.defines)}

# what the build mode controls and the values it can take
mode.help: | mm.banner
	@$(log) "the build mode tunes what the make layer does per deployment target"
	@$(log)
	@$(log) "select one on the command line, e.g."
	@$(log)
	@$(log) "    mm --mode=release"
	@$(log)
	@$(log) "pin the developer-time checks on or off whatever the mode says, e.g."
	@$(log)
	@$(log) "    mm --mode=conda --assertions=yes"
	@$(log)
	@${call log.help,"mode.info","show the current mode and its resolved settings"}
	@$(log)
	@${call log.sec,"available modes",}
	@${foreach mode,$(modes.available),$(log) $(log.indent)$(mode);}
	@$(log)
	@${call log.sec,"settings",}
	@${call log.help,"mode.npm.locked","install npm deps from the committed lock when set (otherwise resolve fresh)"}
	@${call log.help,"mode.compiler.assertions","compile in the developer-time checks (asserts, DEBUG blocks, journal debug/firewall) when set"}
	@$(log)


# end of file
