// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// bind the {rgb_t} triplet as the python {Color} type
void
pyre::py::chroma::color(py::module & m)
{
    // wrap {rgb_t}
    auto cls = py::class_<rgb_t>(
        // the scope
        m,
        // the name of the class
        "Color",
        // its docstring
        "an {r,g,b} color with each channel in [0, 1]");

    // build a color from its three channels
    cls.def(
        // the constructor, as a factory since {rgb_t} is an aggregate
        py::init([](color_t red, color_t green, color_t blue) {
            // assemble the triplet
            return rgb_t { red, green, blue };
        }),
        // the signature
        "red"_a, "green"_a, "blue"_a,
        // the docstring
        "make a color from its three channels");

    // expose the red channel
    cls.def_readwrite(
        // the name
        "red",
        // the member
        &rgb_t::red,
        // the docstring
        "the red channel");
    // expose the green channel
    cls.def_readwrite(
        // the name
        "green",
        // the member
        &rgb_t::green,
        // the docstring
        "the green channel");
    // expose the blue channel
    cls.def_readwrite(
        // the name
        "blue",
        // the member
        &rgb_t::blue,
        // the docstring
        "the blue channel");

    // two colors compare equal when their channels agree; python derives {!=} from this
    cls.def(py::self == py::self);

    // a readable representation
    cls.def(
        // the name
        "__repr__",
        // the handler spells out the three channels
        [](const rgb_t & value) {
            // assemble the representation
            return "Color(" + std::to_string(value.red) + ", " + std::to_string(value.green) + ", "
                 + std::to_string(value.blue) + ")";
        });

    // all done
    return;
}


// end of file
