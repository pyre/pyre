# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# initialize the list of known languages
languages := c c++ fortran python cython cuda javascript graphql

# load the known languages
include $(languages:%=make/languages/%.mm)

# separate them into categories
define languages.compiled :=
${strip
    ${foreach
        language,
        $(languages),
        ${if $(languages.$(language).compiled),$(language),}
    }
}
endef

define languages.interpreted :=
${strip
    ${foreach
        language,
        $(languages),
        ${if $(languages.$(language).interpreted),$(language),}
    }
}
endef

# invoke the language constructor
# ${info --   language constructor}
${foreach \
    language, \
    $(languages), \
    ${eval ${call language.init,$(language)}} \
}

# build the info recipes
# ${info --   language info recipes}

# language info
${foreach \
    language, \
    $(languages), \
    ${eval ${call language.recipes.info,$(language)}} \
}

# collect the set of known source extensions
languages.sources := \
    ${sort \
        ${foreach language, $(languages), $(languages.$(language).sources)} \
    }

# collect the set of known header extensions
languages.headers := \
    ${sort \
        ${foreach language, $(languages), $(languages.$(language).headers)} \
    }


# dispatch a compile event to the registered compiler for a given language
#   usage: languages.compile {language} {source} {object} {external dependencies}
define languages.compile =
${strip
    ${if $(compiler.$(1)),
        ${call languages.$(1).compile,$(2),$(3),$(4)},
        ${call log.error,"no $(1) compiler available"}
    }
}
endef


# dispatch a device link event to the registered compiler for a given language
#   usage: languages.dlink {language} {source} {object} {external dependencies}
define languages.dlink =
${strip
    ${if $(compiler.$(1)),
        ${call languages.$(1).dlink,$(2),$(3),$(4)},
        ${call log.error,"no $(1) compiler available"}
    }
}
endef


# ask the compiler to generate a file with the include dependencies of a translation unit and
# convert it in to a makefil
#   usage: languages.makedep {language} {source} {depfile} {external dependencies}
define languages.makedep =
${strip
    ${if $(compiler.$(1)),
        ${call $(compiler.$(1)).makedep,$(2),$(3),$(4)},
    }
}
endef


# dispatch a link event to the registered compiler for a given language
#   usage: languages.link {language} {source} {executable} {external dependencies}
define languages.link =
${strip
    ${if $(compiler.$(1)),
        ${call languages.$(1).link,$(2),$(3),$(4)},
        ${call log.error,"no $(1) compiler available"}
    }
}
endef


# dispatch a dll event to the registered compiler for a given language
#   usage: languages.dll {language} {source} {dll} {external dependencies}
define languages.dll =
${strip
    ${if $(compiler.$(1)),
        ${call languages.$(1).dll,$(2),$(3),$(4)},
        ${call log.error,"no $(1) compiler available"}
    }
}
endef


# dispatch an ext event to the registered compiler for a given language
#   usage: languages.ext {language} {source} {ext} {external dependencies}
define languages.ext =
${strip
    ${if $(compiler.$(1)),
        ${call languages.$(1).ext,$(2),$(3),$(4)},
        ${call log.error,"no $(1) compiler available"}
    }
}
endef


# end of file
