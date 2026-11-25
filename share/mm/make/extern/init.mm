# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# locate the configuration file of a package
#  usage: extern.config {package-names}
extern.config = \
    ${strip \
        ${foreach name,$(1), \
            ${or \
                ${and \
                    ${value $(name).dir}, \
                    ${realpath $($(name).dir)}, \
                    ${realpath ${addsuffix /$(name)/init.mm,$(extern.all)}} \
                }, \
                ${value $(name).self} \
            } \
        } \
    }


# existence test
#   usage: extern.exists {package-name}
extern.exists = \
    ${strip \
        ${if ${call extern.config,$(1)},$(1),} \
    }


# filter the set of external dependencies that are supported
#  usage extern.is.supported {dependencies}
define extern.is.supported =
    ${strip
        ${foreach dependency, $(1),
            ${filter $(dependency),$(extern.supported)}
        }
    }
endef


# filter the set of external dependencies that are available
#  usage extern.is.available {library}
define extern.is.available =
    ${strip
        ${foreach dependency, $(1),
            ${filter $(dependency),$(extern.available)}
        }
    }
endef


# conditional
#   usage extern.if.available {package-name} {value-if-available} {value-if-unavailable}
define extern.if.available =
    ${strip
        ${if ${filter $(1),$(extern.available)},$(2)}
    }
endef


# the name of {package} when it is available and its version is at least {floor}, and nothing
# otherwise. a package whose version is not known is taken at its word, since mm cannot yet read
# the version of every package from its install location; one that is older is reported at the
# severity of the other configuration complaints, so that a build that requires it can stop
#   usage: extern.is.atLeast {package} {floor}
extern.is.atLeast = \
    ${strip \
        ${if ${strip ${call extern.is.available,$(1)}}, \
            ${if ${strip ${call extern.version.atLeast,${call extern.version.of,$(1)},$(2)}}, \
                $(1), \
                ${call extern.complain,extern $(1): version $($(1).version) is older than $(2); leaving it out} \
            } \
        } \
    }


# the version of {package} as its package database recorded it, or empty when it did not; the
# {flavor} probe asks about the name without referencing it, so -warn-undefined stays quiet
#   usage: extern.version.of {package}
extern.version.of = ${if ${filter-out undefined,${flavor $(1).version}},$($(1).version)}


# whether {version} is at least {floor}: a version with no leading numbers is not known, and passes
#   usage: extern.version.atLeast {version} {floor}
extern.version.atLeast = ${if ${strip ${call extern.version.numbers,$(1)}},${call extern.version.ge,${call extern.version.numbers,$(1)},${call extern.version.numbers,$(2)}},unknown}


# the leading numbers of a version, as a list: a dpkg epoch goes, and so does the packaging suffix
# after a dash, a plus or a tilde, and every component from the first that is not a whole number;
# so {1:18.6-0ubuntu0.26.04.1} reads as {18 6}, and {18beta1} reads as nothing
#   usage: extern.version.numbers {version}
extern.version.numbers = ${call extern.version.leading,${subst ., ,${call extern.version.upstream,$(1)}}}

# the version as its authors gave it, without the epoch and the suffix a packager adds
#   usage: extern.version.upstream {version}
extern.version.upstream = ${firstword ${subst -, ,${subst +, ,${subst ~, ,${lastword ${subst :, ,$(1)}}}}}}

# the whole numbers at the head of a list of words, up to the first word that is not one
#   usage: extern.version.leading {words}
extern.version.leading = ${if ${call extern.version.isNumber,${firstword $(1)}},${firstword $(1)} ${call extern.version.leading,${call extern.version.rest,$(1)}}}

# {word} when it is made of digits alone, which it is when removing them leaves nothing
#   usage: extern.version.isNumber {word}
extern.version.isNumber = ${if $(1),${if ${subst 0,,${subst 1,,${subst 2,,${subst 3,,${subst 4,,${subst 5,,${subst 6,,${subst 7,,${subst 8,,${subst 9,,$(1)}}}}}}}}}},,$(1)}}

# every word of a list but the first
#   usage: extern.version.rest {words}
extern.version.rest = ${wordlist 2,${words $(1)},$(1)}


# compare two lists of numbers piece by piece, a missing piece counting as zero; {ge} when the
# first is at least the second, and nothing when it is less
#   usage: extern.version.ge {numbers} {numbers}
extern.version.ge = ${if ${or $(1),$(2)},${call extern.version.ge.step,${or ${firstword $(1)},0},${or ${firstword $(2)},0},$(1),$(2)},ge}

# one step of the comparison: settle it on the leading pieces, or move on when they are equal
#   usage: extern.version.ge.step {piece} {piece} {numbers} {numbers}
extern.version.ge.step = ${intcmp $(1),$(2),,${call extern.version.ge,${call extern.version.rest,$(3)},${call extern.version.rest,$(4)}},ge}


# a token's {.dependencies}, or empty when the variable was never defined; the {flavor} probe lets
# the closure walk a heterogeneous {.extern} (internal libraries, externals that never set the field)
# without tripping -warn-undefined, since {flavor} reports on a name without referencing it
#   usage: extern.deps.of {token}
extern.deps.of = ${if ${filter-out undefined,${flavor $(1).dependencies}},$($(1).dependencies)}


# the depth-first visitor behind {extern.closure}; a 3-color walk that marks a node {gray} while it
# is on the current stack and {black} once finished, so a {gray} hit is a genuine cycle (warn) while
# a {black} hit is a shared dependency (skip). prepending each node as it finishes yields the post
# order already reversed, i.e. link order: a dependent always precedes the packages it pulls in.
# kept on a single logical line on purpose — newlines inside a {define} leak into the expansion
#   usage: extern.closure.visit {package}
define extern.closure.visit =
${if ${filter $(1),$(extern.closure.black)},,${if ${filter $(1),$(extern.closure.gray)},${warning extern: dependency cycle detected at '$(1)'},${eval extern.closure.gray += $(1)}${foreach dep,${call extern.deps.of,$(1)},${call extern.closure.visit,$(dep)}}${eval extern.closure.black += $(1)}${eval extern.closure.order := $(1) $(extern.closure.order)}}}
endef


# the transitive {.dependencies} closure of a set of root packages, in link order (each dependent
# ahead of the packages it requires); the result is a superset of {roots}. relies on globals mutated
# through {eval}, so it must not be called while it is already expanding (it is not re-entrant)
#   usage: extern.closure {roots}
extern.closure = ${strip ${eval extern.closure.gray :=}${eval extern.closure.black :=}${eval extern.closure.order :=}${foreach root,$(1),${call extern.closure.visit,$(root)}}$(extern.closure.order)}


# resolve an asset's external dependencies now that the whole graph is loaded: {requested} is the
# transitive {.dependencies} closure of the declared {.extern}, while {supported} and {available}
# narrow it to what mm can configure and what is actually installed, all in link order. this runs
# post-load because a load-time edge (a parallel {hdf5} electing {mpi}) is invisible at the earlier,
# pre-load pass that seeds the loader. the final step folds the asset's internal dependencies and its
# installed external closure back into {.extern} — computed once here — so the build recipes pick
# them up unchanged; the induced-but-uninstalled complaint runs first, while {.extern} still holds
# the original declaration that tells an induced package apart from a directly requested one
#   usage: extern.resolve {asset}
define extern.resolve =
    ${eval $(1).extern.requested := ${call extern.closure,$($(1).extern)}}
    ${eval $(1).extern.supported := ${call extern.is.supported,$($(1).extern.requested)}}
    ${eval $(1).extern.available := ${call extern.is.available,$($(1).extern.supported)}}
    ${eval _induced := ${call extern.unsatisfied.induced,$(1)}}
    ${if $(_induced),
        ${call extern.complain,extern $(1): induced dependency '$(_induced)' is not installed (no <pkg>.dir); the link will likely fail}
    }
    ${eval $(1).extern := ${filter-out $(extern.supported),$($(1).extern)} $($(1).extern.available)}
endef


# the externals an asset needs that mm can configure but cannot find installed (no {<pkg>.dir}),
# restricted to the ones induced by the dependency closure rather than declared directly. these are
# the surprising failures the user cannot see in their own config, so they are worth a build-time
# complaint; directly-declared shortfalls are left for {extern.verify} to audit
#   usage: extern.unsatisfied.induced {asset}
extern.unsatisfied.induced = \
    ${filter-out $($(1).extern) $($(1).extern.available),$($(1).extern.supported)}


# a package's own direct {.dependencies} that are not installed; used by the verify report to flag,
# for instance, a parallel {hdf5} whose {mpi} has no install to link against
#   usage: extern.deps.missing {package}
extern.deps.missing = ${filter-out $(extern.available),$($(1).dependencies)}


# the severity of a build-configuration complaint. {warning} lets the build proceed so the user can
# reach a real authority — the compiler or the linker — before stopping; flip to {error} to fail
# early instead. {extern.verify} audits the configuration on its own and is never gated by this
extern.complain.severity ?= warning

# emit a build-configuration complaint at the configured severity. the severity must select a
# literal {warning}/{error} function name: make resolves the function at parse time, so an indirect
# {${$(severity) ...}} would be read as a reference to an undefined variable instead
#   usage: extern.complain {message}
extern.complain = ${if ${filter error,$(extern.complain.severity)},${error $(1)},${warning $(1)}}


# construct the contribution of an external package to the compile line
#   usage: extern.compile.options.this {language} {package}
extern.compile.options.this = \
    ${foreach category, $(languages.$(1).categories.compile), \
        ${addprefix $($(compiler.$(1)).prefix.$(category)),$($(2).$(category))} \
    }


# build the contribution to the compile command line from a set of packages
#  usage: extern.compile.options {language} {packages}
extern.compile.options = \
    ${foreach package, $(2), \
        ${call extern.compile.options.this,$(1),$(package)} \
    }


# construct the contribution of an external package to the link line
#   usage: extern.link.options.this {language} {package}
extern.link.options.this = \
    ${foreach category, $(languages.$(1).categories.link), \
        ${addprefix $($(compiler.$(1)).prefix.$(category)),$($(2).$(category))} \
    }


# build the contribution to the link command line from a set of packages
#  usage: extern.link.options {language} {packages}
extern.link.options = \
    ${foreach package, $(2), \
        ${call extern.link.options.this,$(1),$(package)} \
    }


# the header markers of a package that do not resolve anywhere on its include path; a
# non-empty result is proof the package cannot be compiled against as currently configured
#  usage: extern.markers.headers.missing {package}
extern.markers.headers.missing = \
    ${strip \
        ${foreach marker, $($(1).markers.headers), \
            ${if ${wildcard ${addsuffix /$(marker),$($(1).incpath)}},,$(marker)} \
        } \
    }


# the candidate linker filenames for a library across a package's library path; the linker
# resolves {-lfoo} to {libfoo} with a shared or static suffix, so probe all three
#  usage: extern.markers.lib.candidates {package} {library}
extern.markers.lib.candidates = \
    ${foreach dir, $($(1).libpath), \
        ${addprefix $(dir)/lib$(2),.so .dylib .a} \
    }


# the libraries of a package that resolve to no file on its library path; a non-empty result
# is proof the package cannot be linked against as currently configured
#  usage: extern.markers.libraries.missing {package}
extern.markers.libraries.missing = \
    ${strip \
        ${foreach lib, $($(1).libraries), \
            ${if ${wildcard ${call extern.markers.lib.candidates,$(1),$(lib)}},,$(lib)} \
        } \
    }


# the required values of a package that came out empty; a non-empty result names the critical
# variables (e.g. {libraries}) the package could not set, proving it is misconfigured even when
# its declared headers and libraries happen to resolve. packages opt in via {<pkg>.markers.required}
#  usage: extern.markers.required.missing {package}
extern.markers.required.missing = \
    ${strip \
        ${foreach var, $($(1).markers.required), \
            ${if ${strip $($(1).$(var))},,$(var)} \
        } \
    }


# the module markers of a package that the interpreter of the build cannot import; a non-empty
# result is proof that a tool which runs in that interpreter is not installed there. the import
# leaves the current directory off the module search path, so a source tree cannot answer it
#  usage: extern.markers.modules.missing {package}
extern.markers.modules.missing = \
    ${strip \
        ${foreach module, $($(1).markers.modules), \
            ${if ${shell $($(compiler.python).driver) -P -c "import $(module)" >/dev/null 2>&1 && echo ok},,$(module)} \
        } \
    }


# the complete set of unresolved markers for a package; empty when the package checks out
#  usage: extern.markers.problems {package}
extern.markers.problems = \
    ${strip \
        ${call extern.markers.headers.missing,$(1)} \
        ${call extern.markers.libraries.missing,$(1)} \
        ${call extern.markers.modules.missing,$(1)} \
        ${call extern.markers.required.missing,$(1)} \
    }


# the loaded externals whose every marker resolves
extern.markers.ok = \
    ${strip \
        ${foreach package, $(projects.extern.loaded), \
            ${if ${call extern.markers.problems,$(package)},,$(package)} \
        } \
    }


# the loaded externals with at least one unresolved marker
extern.markers.broken = \
    ${strip \
        ${foreach package, $(projects.extern.loaded), \
            ${if ${call extern.markers.problems,$(package)},$(package),} \
        } \
    }


# emit a build-time warning for every loaded package that left a required value empty; this runs at
# load time, so a misconfiguration (e.g. an unrecognized {mpi.flavor} that yields no {libraries})
# surfaces immediately as a loud, self-describing warning instead of an opaque link failure further
# downstream. a package may set {<pkg>.markers.required.hint} to append the likely cause and fix
#  usage: extern.markers.required.warn {packages}
define extern.markers.required.warn =
    ${foreach package, $(1),
        ${eval _missing := ${call extern.markers.required.missing,$(package)}}
        ${if $(_missing),
            ${warning extern $(package): required value(s) '$(_missing)' empty ${strip $($(package).markers.required.hint)} -- the link will likely fail}
        }
    }
endef


# end of file
