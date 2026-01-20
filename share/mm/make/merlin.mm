# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# user configuration
config.db := config
# if we know the username, look for user specific settings
config.db += ${if $(user.username),$(user.username) $(user.username)@$(host.nickname)}
# if the user has specified an environment
config.db += ${if $(user.environment),$(user.environment) $(user.environment)@$(host.nickname)}

# load the configuration file
-include ${addsuffix .mm, $(config.db)}

# this list used to include the various project content types; these are now initialized
# dynamically whenever a project that declares assets of that type is encountered; also,
# projects can now declare new asset types and provide support for them in their {mm}
# configuration directory
define model :=
    log mm
    languages platforms hosts users developers
    compilers targets builder
	extern projects
endef

# the categories of methods each object provides
categories := init rules model

# import the interface
-include \
    ${foreach category, $(categories), \
        ${foreach class, $(model), \
            make/$(class)/$(category).mm \
    } \
}

# make a target that shows the configuration filename seeds
config.info:
	@${call log.sec,"config","mm configuration files"}
	@${call log.var,"seeds",$(config.db)}


# end of file
