# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# host info
host.info:
	@${call log.sec,"host", "host info"}
	@${call log.var,name,$(host.name)}
	@${call log.var,nickname,$(host.nickname)}
	@${call log.var,os,$(host.os)}
	@${call log.var,arch,$(host.arch)}
	@${call log.var,cores,$(host.cores)}


# end of file
