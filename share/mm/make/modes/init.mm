# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the baseline shared by every mode
include make/modes/default.mm
# the selected mode's overrides; a mode with no file here is a fatal error
include make/modes/$(project.mode).mm

# the driver may pin the assertion disposition, e.g. to keep the developer-time checks in a
# deployment layout while testing it: {yes} compiles them in, {no} leaves them out, and an empty
# value defers to the mode
project.assertions ?=
ifneq ($(project.assertions),)
mode.compiler.assertions := ${filter yes,$(project.assertions)}
endif

# {mode.compiler} joins the compiler option sources as a flat, language-independent contributor,
# just like {mm}; declare its full category set so no slot is ever an undefined variable
mode.compiler.flags :=
# take ownership of the two disposition macros as a coherent pair: exactly one is defined at any
# time, so client code can never land in an ambiguous state. checks on ({assertions} set) means
# our {DEBUG} convention and no {NDEBUG}; checks off means the standard {NDEBUG} assert guard and
# no {DEBUG}. the exclusivity here is what makes {NDEBUG} dominate {DEBUG} -- the precedence the
# journal api already assumes -- moot in practice
mode.compiler.defines := ${if $(mode.compiler.assertions),DEBUG,NDEBUG}
mode.compiler.incpath :=
mode.compiler.ldflags :=
mode.compiler.libpath :=
mode.compiler.rpath :=
mode.compiler.libraries :=

# the implemented modes, discovered from the files present here, minus the framework files
modes.available := ${filter-out init default rules model,${basename ${notdir ${wildcard $(mm.home)/make/modes/*.mm}}}}


# end of file
