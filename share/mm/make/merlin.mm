# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# user configuration
# look for a generic configuration file
-include config.mm
# developer choices
-include $(user.username).mm
# and a user/host specific configuration file
-include $(user.username)@$(host.nickname).mm

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


# end of file
