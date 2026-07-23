# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the baseline (non-dev) value of every mode-dependent knob, grouped by consumer

# npm: empty installs fresh ({npm i}); non-empty installs from the committed lock ({npm ci})
mode.npm.locked := yes

# compiler: whether the developer-time checks are compiled in -- the {assert}s, the code under
# {#if defined(DEBUG)}, and journal's {debug}/{firewall} channels. this is a mode disposition,
# orthogonal to the opt/debug optimization target; {make/modes/init.mm} turns it into the
# coherent {DEBUG}/{NDEBUG} macro pair. the baseline is a deployment build, so the checks are off
mode.compiler.assertions :=


# end of file
