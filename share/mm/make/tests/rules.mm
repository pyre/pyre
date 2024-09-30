# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# test suite help
tests.info: mm.banner
	@$(log) "known test suites: "$(palette.targets)$(testsuites)$(palette.normal)
	@$(log)
	@$(log) "to build one of them, use its name as a target"
	@$(log) "    mm ${firstword $(testsuites)}"
	@$(log)
	@$(log) "to get more information about a specific library, use"
	@$(log) "    mm ${firstword $(testsuites)}.info"
	@$(log)

# bootstrap
# make the test suite specific targets
#  usage: test.workflows {test suite}
define tests.workflows =
    # build recipes
    ${call test.workflows.build,$(1)}
    # info recipes: show values
    ${call test.workflows.info,$(1)}
    # help recipes: show documentation
    ${call test.workflows.help,$(1)}
# all done
endef


# build targets
# target factory for building a test suite
define test.workflows.build =

# the main recipe
$(1): $($(1).prerequisites) $(1).testcases
	@${call log.asset,"test suite",$(1)}

# the test cases depend on the individual test targets
$(1).testcases: $($(1).staging.targets)

# clean up
$(1).clean:: ${addsuffix .clean,$($(1).staging.containers) $($(1).staging.targets)}

# make recipes for the individual test targets
${foreach target, $($(1).staging.targets), \
    ${eval
        ${if $($(target).compiled),
            ${call test.workflows.target.compiled,$(target),$(1)}, \
            ${call test.workflows.target.interpreted,$(target),$(1)} \
        }
    }
}

# go through the directories in the test suite, convert them into targets, and register a clean
# up rule if the user has specified files they want removed
${foreach dir,$($(1).staging.directories), \
    ${eval _container := ${patsubst %.,%,${subst /,.,$(dir)}}}
    ${eval $(_container).clean:: ; \
        ${if ${value $(_container).clean}, \
            ${call log.action,clean,$(_container)}; \
            $(rm.force-recurse) ${addprefix $($(1).home)$(dir),$($(_container).clean)} \
        } \
    } \
}

# make container targets
${foreach case,$($(1).staging.targets), \
    ${eval ${call test.workflows.containers,$(1),$(case)} \
    } \
}

# make local aliases
${foreach case,$($(1).staging.targets), \
    ${eval ${call test.workflows.aliases,$(1),$(case)} \
    } \
}

# all done
endef


# build targets
# target factory that builds a target for an interpreted test case
#   usage: test.workflows.target.interpreted {target} {testsuite}
define test.workflows.target.interpreted =

    # local variables
    ${eval _tag := ${subst $($(2).home),,$($(1).source)}}
    ${eval _launcher := $(compiler.$($(1).language)) $($(1).source)}
    ${eval _harness := ${if $($(1).harness),$($(1).harness) $(_launcher),$(_launcher)}}

# the aggregator
$(1): $(1).pre $(1).cases $(1).post

# dependencies
# startup
$(1).pre: $($(1).pre)

# cleanup
$(1).post: $(1).pre $(1).cases $($(1).post)

# make sure cleanup happens after startup; because this rule is in addition to its definition,
# we must use a double colon; this in turn implies that the rule definition must be a
# double-colon rule
${if $($(1).post),\
    ${eval $($(1).post) :: $($(1).pre) $(1).cases} \
}

# invoking the driver for each registered test case
$(1).cases: $($($(1).suite).prerequisites) $(1).pre
	@$(cd) $${dir $($(1).source)} ; \
        ${if $($(1).cases), \
            ${foreach case, $($(1).cases), \
                ${call log.action,test,$($(case).harness) $(_tag) $($(case).argv)}; \
                $($(case).harness) $(_launcher) $($(case).argv); \
                }, \
	    ${call log.action,test,$(_tag)}; \
                $($(1).harness) $(_launcher) $($(1).argv) \
        }

# clean up; double colon, since it may be used as a {post} rule
$(1).clean::
	@${if $($(1).clean), \
            ${call log.action,clean,$(1)}; \
            $(rm.force-recurse) ${addprefix $($(1).home),$($(1).clean)}, \
        }

# show info
$(1).info:
	@${call log.sec,$(1),"a test driver in test suite '$(2)' of project '$($(2).project)'"}
	@${call log.var,source,$($(1).source)}
	@${call log.var,interpreted,yes}
	@${call log.var,language,$($(1).language)}
	@${call log.var,compiler,$(compiler.$($(1).language))}
	@${call log.sec,$(log.indent)cases,}
	@${if $($(1).cases), \
            ${foreach case,$($(1).cases),\
                ${call log.var,$(log.indent)$(case),${strip \
                    $($(case).harness) $(_launcher) $($(case).argv)}};}, \
            $(log) $(log.indent)$(log.indent)$($(1).harness) $(_launcher) $($(1).argv)}

# just in case...
.PHONY: $(1) $(1).cases $(1).clean

# all done
endef


# target factory that builds a target for a compiled test case
#   usage: test.workflows.target.compiled {target} {testsuite}
define test.workflows.target.compiled =

    # local variables
    ${eval _tag := ${subst $($(2).home),,$($(1).source)}}
    ${eval _base := ${subst $($(2).home)$($(2).root),,$($(1).base)}}

# the aggregator
$(1): $(1).pre $(1).driver $(1).cases $(1).post

# dependencies
# startup
$(1).pre: $($(1).pre)

# cleanup
$(1).post: $(1).pre $(1).cases $($(1).post)

# make sure cleanup happens after startup; because this rule is in addition to its definition,
# we must use a double colon; this in turn implies that the rule definition must be a
# double-colon rule
${if $($(1).post),\
    ${eval $($(1).post) :: $($(1).pre) $(1).cases} \
}

$(1).driver: $($(1).base)

$($(1).base): $($($(1).suite).prerequisites) $($(1).source)
	@${call log.action,$($(1).language),$(_tag)}
	${call \
            languages.$($(1).language).link, \
            $($(1).source), \
            $($(1).base), \
            $(1).$($(1).language) $(1) $($(1).suite).$($(1).language) $($(1).extern) }


$(1).cases: $(1).driver $(1).pre
	@$(cd) $${dir $($(1).source)} ; \
	${if $($(1).cases), \
            ${foreach case, $($(1).cases), \
                ${call log.action,test,$($(case).harness) $(_base) $($(case).argv)}; \
                $($(case).harness) $($(1).base) $($(case).argv); \
                }, \
	    ${call log.action,test,$($(1).harness) $(_base) $($(1).argv)}; \
                $($(1).harness) $($(1).base) $($(1).argv); \
        }

# clean up; double colon, since it may be used as a {post} rule
$(1).clean::
	@${call log.action,clean,$(_tag)}
	$(rm.force-recurse) ${addprefix $($(1).home),$($(1).clean)} $($(1).base) \
            ${foreach case,$($(1).cases),$($(case).clean)} \
            ${call $(compiler.$($(1).language)).clean,$($(1).base)} \
            ${call platform.clean,$($(1).base)}

# show info
$(1).info:
	@${call log.sec,$(1),"a test driver in test suite '$(2)' of project '$($(2).project)'"}
	@${call log.var,source,$($(1).source)}
	@${call log.var,compiled,yes}
	@${call log.var,language,$($(1).language)}
	@${call log.var,compiler,$(compiler.$($(1).language))}
	@${call log.var,extern,$($(1).extern)}
	@${call log.sec,$(log.indent)cases,}
	@${if $($(1).cases), \
            ${foreach case,$($(1).cases), \
                ${call log.var,$(log.indent)$(case),${strip \
                    $($(case).harness) $($(1).base) $($(case).argv)}}; \
                }, \
            $(log) $(log.indent)$(log.indent)${strip $($(1).harness) $($(1).base) $($(1).argv)} \
            }

# just in case...
.PHONY: $(1) $(1).driver $(1).cases $(1).clean

# all done
endef


# target factory that makes targets out of the intermediate directories in the test suite
# usage: test.workflows.containers {testsuite} {testcase}
define test.workflows.containers =
    ${eval _root := ${subst $(space),.,${strip ${subst /,$(space),$($(1).root)}}}}
    # local variables
    ${eval _suite := $(1)}
    ${eval _case := $(2)}
    # split on the dots
    ${eval _split := ${subst ., ,$(_case)}}
    # compute its length
    ${eval _len := ${words $(_split)}}
    # compute the length of the list that is one shorter than the cases
    ${eval _len-1 := ${words ${wordlist 2,$(_len),$(_split)}}}
    # build the parent by dropping the last word
    ${eval _parent := ${subst $(space),.,${wordlist 1,$(_len-1),$(_split)}}}

    # build the rule and recurse
    ${if ${subst $(_root),,$(_case)}, \
      ${eval $(_parent) :: $(_case);} \
      ${eval $(_parent).drivers :: $(_case).driver;} \
      ${eval $(_parent).clean :: $(_case).clean;} \
      ${call test.workflows.containers,$(_suite),$(_parent)}, \
    }

# all done
endef


# target factory that gives short names to the tests cases in {project.origin}
# usage: test.workflows.aliases {testsuite} {testcase}
define test.workflows.aliases =
    # local variables
    ${eval _suite := $(1)}
    ${eval _case := $(2)}
    # project geography
    ${eval _origin := $(project.origin)}
    ${eval _anchor := $(project.anchor)}
    # project the {cwd} onto the test suite
    ${eval _parent := ${subst /,.,${subst $(_anchor)/,,$(_origin)}}}
    # project the test case onto the {parent}
    ${eval _alias := ${subst $(_parent).,,$(_case)}}
    #  deduce the driver name
    ${eval _driver := ${strip \
        ${if ${subst $(_case),,$(_alias)}, \
            $(_alias),\
        } \
    }}

    # if the driver is non-empty, make rule aliases
    ${if $(_driver),\
        ${eval $(_alias) : $(_case);} \
        ${eval $(_alias).cases : $(_case).cases;} \
        ${eval $(_alias).driver : $(_case).driver;} \
        ${eval $(_alias).clean : $(_case).clean;} \
        ${eval $(_alias).info : $(_case).info;}, \
    }

# all done
endef


# target factory to log the metadata of a specific test suite
define test.workflows.info =

# the main recipe
$(1).info:
	@${call log.sec,$(1),"a testsuite in project '$($(1).project)'"}
	@$(log)
	@${foreach category,$($(1).meta.categories),\
            ${call log.sec,"  "$(category),$($(1).metadoc.$(category))}; \
            ${foreach var,$($(1).meta.$(category)), \
                ${call log.var,$(1).$(var),$$($(1).$(var))}; \
             } \
        }
	@$(log)
	@$(log) "for an explanation of their purpose, try"
	@$(log)
	@$(log) "    mm $(1).help"
	@$(log)
	@$(log) "related targets:"
	@$(log)
	@${call log.help,$(1).info.directories,"the layout of the test suite directories"}
	@${call log.help,$(1).info.drivers,"the test case drivers"}
	@${call log.help,$(1).info.targets,"the test case make targets"}
	@${call log.help,$(1).info.staging.targets,"the make targets for individual test cases"}

# all done
endef


# make targets that display meta-data documentation for a specific test suite
#   usage: test.workflows.build {testsuite}
# target factory for building a test suite
define test.workflows.help =

# the main recipe
$(1).help:
	@$(log)
	@${call log.sec,$(1),library attributes}
	@$(log)
	@${foreach category,$($(1).meta.categories),\
            ${call log.sec,"  "$(category),$($(1).metadoc.$(category))}; \
            ${foreach var,$($(1).meta.$(category)), \
                ${call log.help,$(1).$(var),$($(1).metadoc.$(var))}; \
             } \
        }
	@$(log)
	@$(log) "for a listing of their values, try"
	@$(log)
	@$(log) "    mm $(1).info"
	@$(log)

# make a recipe that prints the directory layout of a test suite
$(1).info.directories:
	@${call log.sec,$(1),"a test suite in project '$($(1).project)'"}
	@${call log.sec,"  test directories",}
	@${foreach directory,$($(1).directories),$(log) $(log.indent)$(directory);}

# make a recipe that prints the set of drivers that comprise a test suite
$(1).info.drivers:
	@${call log.sec,$(1),"a test suite in project '$($(1).project)'"}
	@${call log.sec,"  drivers",}
	@${foreach driver,$($(1).drivers),$(log) $(log.indent)$(driver);}

# make a recipe that prints the set of source languages
$(1).info.languages:
	@${call log.sec,$(1),"a test suite in project '$($(1).project)'"}
	@${call log.var,"languages",$($(1).languages)}
	@${foreach language,$($(1).languages),\
            ${call log.sec,"  $(language)","flags and options"}; \
            ${foreach category,$(languages.$(language).categories), \
                ${call log.var,$(category),$($(1).$(language).$(category))}; \
            } \
        }

# make a recipe that prints the set of make targets for individual test cases
$(1).info.staging.targets:
	@${call log.sec,$(1),"a test suite in project '$($(1).project)'"}
	@${call log.sec,"  individual test case targets",}
	@${foreach target,$($(1).staging.targets), \
            ${call log.sec,$(log.indent)$(target),}; \
            ${call log.var,$(log.indent)"source",$($(target).source)}; \
            ${call log.var,$(log.indent)"language",$($(target).language)}; \
            ${call log.var,$(log.indent)"extern",$($(target).extern)}; \
            ${call log.var,$(log.indent)"compiled",$($(target).compiled)}; \
            ${call log.var,$(log.indent)"interpreted",$($(target).interpreted)}; \
            ${call log.var,$(log.indent)"doc",$($(target).doc)}; \
            ${call log.var,$(log.indent)"cases",$($(target).cases)}; \
            ${call log.var,$(log.indent)"clean",$($(target).clean)}; \
        }


# all done
endef


# end of file
