# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the runner registry summary
runners.info: mm.banner
	@${call log.sec,"runners","the available test runners"}
	@$(log)
	@${foreach runner,$(runners),${call log.var,$(runner),$(runner.$(runner).doc)};}
	@$(log)
	@$(log) "a test suite delegates to one with"
	@$(log) "    <suite>.runner := ${firstword $(runners)}"
	@$(log)
	@$(log) "for the settings of a specific runner, use"
	@$(log) "    mm runners.${firstword $(runners)}.info"
	@$(log)


# make a recipe that logs the settings of a single runner
#  usage: runner.recipes.info {runner}
define runner.recipes.info =
runners.$(runner).info:
	@${call log.sec,$(runner),$(runner.$(runner).doc)}
	@${call log.var,prepare,$(runner.$(runner).prepare)}
	@${call log.var,language,$(runner.$(runner).language)}
	@${call log.var,launch,$(runner.$(runner).launch)}
	@${call log.var,libraries,$(runner.$(runner).libraries)}
	@${call log.var,argv,$(runner.$(runner).argv)}
	@${call log.var,env,$(runner.$(runner).env)}
	@${call log.var,suite,$(runner.$(runner).suite)}
# all done
endef


# end of file
