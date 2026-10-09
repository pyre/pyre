// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the descriptions of the slots and the settings of factories, which python reads but does not
// make
void
pyre::py::flow::descriptions(py::module & m)
{
    // the description of a slot
    auto slot = py::class_<slot_t>(
        // the scope
        m,
        // the name of the class
        "Slot",
        // the docstring
        "the description of a slot of a factory");
    // its name
    slot.def_property_readonly(
        // the name
        "name",
        // the implementation
        &slot_t::name,
        // the docstring
        "my name");
    // whether the factory reads the product bound to it
    slot.def_property_readonly(
        // the name
        "reads",
        // the implementation
        &slot_t::reads,
        // the docstring
        "whether my factory reads the product bound to me");
    // whether the factory writes it
    slot.def_property_readonly(
        // the name
        "writes",
        // the implementation
        &slot_t::writes,
        // the docstring
        "whether my factory writes the product bound to me");
    // the declaration of the products it takes
    slot.def_property_readonly(
        // the name
        "product",
        // the implementation
        &slot_t::product,
        // the docstring
        "the declaration of the type of the products i take");
    // whether a product fits
    slot.def(
        // the name
        "accepts",
        // the implementation
        &slot_t::accepts,
        // the signature
        "product"_a,
        // the docstring
        "check whether {product} is one of the products i take");

    // the description of a setting
    auto setting = py::class_<setting_t>(
        // the scope
        m,
        // the name of the class
        "Setting",
        // the docstring
        "the description of a setting of a factory");
    // its name
    setting.def_property_readonly(
        // the name
        "name",
        // the implementation
        &setting_t::name,
        // the docstring
        "my name");
    // the type of its values
    setting.def_property_readonly(
        // the name
        "type",
        // the implementation
        &setting_t::type,
        // the docstring
        "the name of the type of my values: int, double, or interval");

    // all done
    return;
}


// end of file
