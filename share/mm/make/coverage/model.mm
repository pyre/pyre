# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a coverage build is one whose variants include {cov}; the target machinery has already folded the
# {cov} compile and link flags in by this point, so all that is left is to arrange the post-run
# reporting
coverage.active := ${filter cov,$(target.variants)}

# pick the instrumentation back end from the c++ compiler: the clang family emits llvm source based
# coverage that {llvm-profdata}/{llvm-cov} consume, while gcc emits gcov data that {gcovr} reads
coverage.backend := ${if ${filter clang%,$(compiler.c++)},llvm,gcov}

# anchor the derived products under the staging area, in a sibling of the build tree so a
# {coverage.clean} can wipe them without touching object files
coverage.raw := $(builder.staging)coverage/raw/
coverage.report := $(builder.staging)coverage/report/
# the lcov file lands at the root of the coverage area, at a stable path the editor can watch
coverage.info := $(builder.staging)coverage/lcov.info
# the merged profile the llvm reporters index against
coverage.profdata := $(builder.staging)coverage/merged.profdata

# when the llvm back end is active, steer every instrumented process launched during the build --
# most importantly the test drivers -- to write its own raw profile into the collection directory.
# {%p} keys the file by pid and {%m} by the binary's coverage signature, so concurrent drivers and
# distinct binaries never clobber one another; the runtime creates the directory tree on first
# write. exporting it here, once, spares every test recipe from having to thread it through by hand
ifneq ($(strip $(coverage.active)),)
ifeq ($(coverage.backend),llvm)
export LLVM_PROFILE_FILE := $(coverage.raw)%p-%m.profraw
endif
endif

# tie the top level {coverage} target to the back end specific reporter now that {coverage.backend} is
# final; the report recipes themselves live in the rules pass, following mm's split of rule templates
# in {rules.mm} from their instantiation here
${eval coverage: coverage.$(coverage.backend)}

# the raw profiles the llvm reporter folds together; a recursively expanded {wildcard} so the glob
# runs when the recipe fires, by which point the test run has deposited the files
coverage.raws = ${wildcard $(coverage.raw)*.profraw}

# the compiled test drivers, gathered from every registered suite. this matters because a header-only
# template library instantiates most of its code into the drivers rather than into any shared library,
# so a report built only from the installed {.so}s would not see it. recursively expanded so the walk
# runs when a reporter fires: this class loads before {projects}, so the suite metadata is not yet final
# here and a deferred read is required. each suite's {staging.targets} mixes compiled, staged, and
# interpreted cases, so keep the ones flagged {compiled} and take their {base} binary
coverage.drivers = \
    ${if $(coverage.active), \
        ${foreach suite,$(testsuites), \
            ${foreach case,$($(suite).staging.targets), \
                ${if $($(case).compiled),$($(case).base)} \
            } \
        } \
    }
# the instrumented binaries to attribute the profiles to: every shared library installed under the
# prefix, the compiled test drivers, and whatever extra objects a project names through
# {coverage.objects}. the {wildcard} over the drivers keeps only those a given run actually built, so a
# partial test run never hands llvm-cov a missing {-object}
coverage.binaries = \
    ${wildcard $(builder.dest.lib)*.so $(builder.dest.lib)*.dylib} \
    ${wildcard $(coverage.drivers)} \
    $(coverage.objects)
# llvm-cov takes the first binary as a positional argument and every subsequent one behind its own
# {-object} flag; assemble that argument vector once for the three reporters to share
coverage.objargs = \
    ${firstword $(coverage.binaries)} \
    ${patsubst %,-object %,${wordlist 2,${words $(coverage.binaries)},$(coverage.binaries)}}

# rewrite installed header paths back to source. a test driver includes its project's headers from the
# install prefix, so the coverage data records the installed copy's path; that makes gcov's reporter --
# rooted at the project -- drop the headers, and makes the llvm reporter attribute them to the prefix
# rather than to the tree the developer edits. for each library, map its installed header directory back
# to the source directory the headers were copied from; both are already known to the library model. the
# {sort} keys on the {incdir} left-hand side, and because a parent directory string sorts before any
# child of it, this yields the general-to-specific order the compilers' last-match-wins mapping requires.
# recursively expanded so it is evaluated where it is consumed -- in each object's compile options during
# the projects pass -- by which point the libraries that object depends on have registered
coverage.prefixmap = ${sort ${foreach lib,$(libraries),$($(lib).incdir)=$($(lib).prefix)}}

# expose the coverage contribution to the compiler option machinery as a per language party:
# {compiler.option.sources} adds a {coverage.<language>} source, but only when {cov} is selected and the
# language's compiler instruments -- so these flags reach a compile if and only if the compiler actually
# does coverage. a language participates only if its compiler names a non-trivial {cov} flag; an empty
# {cov} means the compiler does not instrument, so it contributes nothing. for a participating language,
# first initialize each option category to empty -- exactly as {target.init} does for its own party -- so
# the option assembly, which queries every category, never expands an undefined
# {coverage.<language>.<category>}. then, if the compiler also names a {cov.prefixmap} flag, fill in the
# flags category with the map: recursively expanded so the map is computed at each object's bake, and
# defined here -- before {projects} -- so it exists by the time the first workflow bakes. only the map
# lookup is deferred; the language and its compiler's flag name are fixed now. {value} reads the compiler
# slot and {origin} tests the prefix-map flag without expanding either, so a missing compiler or flag
# trips no undefined-variable warning
${foreach \
    language, \
    $(languages.compiled), \
    ${if ${value compiler.$(language)}, \
        ${if $($(compiler.$(language)).cov), \
            ${foreach \
                category, \
                $(languages.$(language).categories), \
                ${eval coverage.$(language).$(category) ?=} \
            } \
            ${if ${filter-out undefined,${origin $(compiler.$(language)).cov.prefixmap}}, \
                ${eval \
                    coverage.$(language).flags = \
                        $${foreach pair,$$(coverage.prefixmap),$($(compiler.$(language)).cov.prefixmap)=$$(pair)} \
                } \
            } \
        } \
    } \
}


# end of file
