# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# make a recipe that logs information about a language
#  usage: language.recipes.info {language}
define language.recipes.info =
# make the recipe; note the {$$} that enables delayed evaluation until after the compiler name
# is known
languages.$(language).info:
	@${call log.sec,$(language),}
	@${call log.var,compiler,$$(compiler.$(language))}
	@${call log.var,compiled,$(languages.$(language).compiled)}
	@${call log.var,interpreted,$(languages.$(language).interpreted)}
	@${call log.var,source extensions,$(languages.$(language).sources)}
	@${call log.var,header extensions,$(languages.$(language).headers)}
# all done
endef


# make a recipe that displays the known languages
languages.info:
	@${call log.var,"languages",$(languages)}


# make a recipe that logs the map from extensions to languages
suffixes.info:
	@${call log.sec,"suffixes","a map of recognized file extensions for each language"}
	@${call log.sec,"  sources",}
	@${foreach \
            language, \
            $(languages), \
	    ${call log.var,$(language),$(languages.$(language).sources)}; \
        }


# end of file
