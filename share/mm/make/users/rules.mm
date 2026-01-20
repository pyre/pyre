# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# user info
user.info:
	@${call log.sec,"user", "user info"}
	@${call log.var,username,$(user.username)}
	@${call log.var,uid,$(user.uid)}
	@${call log.var,home,$(user.home)}
	@${call log.var,name,$(user.name)}
	@${call log.var,email,$(user.email)}
	@${call log.var,environment,$(user.environment)}


# end of file
