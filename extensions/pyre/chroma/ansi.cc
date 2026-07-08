// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// bind the {ansi} serializers
void
pyre::py::chroma::ansi(py::module & m)
{
    // create the {ansi} submodule
    auto ansi = m.def_submodule(
        // the name of the module
        "ansi",
        // its docstring
        "serialize a color as an ANSI terminal escape sequence");

    // the reset sequence
    ansi.def(
        // the name
        "reset",
        // the serializer
        &pyre::chroma::ansi::reset,
        // the docstring
        "the sequence that returns the terminal to its default attributes");
    // a 24-bit truecolor sequence from a color
    ansi.def(
        // the name
        "rgb",
        // the serializer
        &pyre::chroma::ansi::rgb,
        // the signature
        "color"_a, "foreground"_a = true,
        // the docstring
        "a 24-bit truecolor escape sequence for {color}");
    // a 256-color-cube sequence from a color
    ansi.def(
        // the name
        "rgb256",
        // the serializer
        &pyre::chroma::ansi::rgb256,
        // the signature
        "color"_a, "foreground"_a = true,
        // the docstring
        "a 256-color-cube escape sequence for {color}");
    // a grayscale-ramp sequence from a level
    ansi.def(
        // the name
        "gray",
        // the serializer
        &pyre::chroma::ansi::gray,
        // the signature
        "level"_a, "foreground"_a = true,
        // the docstring
        "a grayscale-ramp escape sequence for {level}");
    // a 16-color sequence from a terminal-palette code
    ansi.def(
        // the name
        "csi3",
        // the serializer
        &pyre::chroma::ansi::csi3,
        // the signature
        "code"_a, "bright"_a = false,
        // the docstring
        "a 16-color escape sequence for the terminal-palette {code}");

    // all done
    return;
}


// end of file
