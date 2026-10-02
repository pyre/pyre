# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# {dev} resolves dependencies fresh rather than from the committed lock
mode.npm.locked :=

# {dev} keeps the developer-time checks live: {assert}s fire, the {#if defined(DEBUG)} blocks
# compile in, and journal's {debug}/{firewall} channels are real -- even in an optimized build
mode.compiler.assertions := yes

# {dev} builds the bundle for development, with whatever source maps the project asks for
mode.webpack.production :=


# end of file
