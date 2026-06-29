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

# what the build mode controls and the values it can take
mode.help: | mm.banner
	@$(log) "the build mode tunes what the make layer does per deployment target"
	@$(log)
	@$(log) "select one on the command line, e.g."
	@$(log)
	@$(log) "    mm --mode=release"
	@$(log)
	@${call log.help,"mode.info","show the current mode and its resolved settings"}
	@$(log)
	@${call log.sec,"available modes",}
	@${foreach mode,$(modes.available),$(log) $(log.indent)$(mode);}
	@$(log)
	@${call log.sec,"settings",}
	@${call log.help,"mode.npm.locked","install npm deps from the committed lock when set (otherwise resolve fresh)"}
	@$(log)


# end of file
