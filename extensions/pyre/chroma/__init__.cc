// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// package declarations
#include "__init__.h"


// build the submodule
void
pyre::py::chroma::__init__(py::module & m)
{
    // create a {chroma} submodule
    auto chroma = m.def_submodule(
        // the name of the module
        "chroma",
        // its docstring
        "wrappers over {pyre::chroma}: the single source of color truth");

    // bind the color type first, since the converters and serializers traffic in it
    color(chroma);
    // add the {rgb} converters and the color palette
    rgb(chroma);
    // add the {ansi} serializers
    ansi(chroma);

    // all done
    return;
}


// end of file
