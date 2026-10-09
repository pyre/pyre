// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the protocols of nodes, products, and factories; python holds every node through a smart
// holder, so a node python made through the catalog stays one object however often it crosses
// the boundary
void
pyre::py::flow::nodes(py::module & m)
{
    // the base of all nodes
    auto node = py::classh<node_t>(
        // the scope
        m,
        // the name of the class
        "Node",
        // the docstring
        "the base of the nodes of a flow graph");
    // its name
    node.def_property_readonly(
        // the name
        "name",
        // the implementation
        [](const node_t & self) -> string_t { return self.name(); },
        // the docstring
        "my name");
    // invalidation
    node.def(
        // the name
        "flush",
        // the implementation
        &node_t::flush,
        // the docstring
        "mark what depends on me as stale");

    // products
    auto product = py::classh<product_t, node_t>(
        // the scope
        m,
        // the name of the class
        "Product",
        // the docstring
        "the base of the products of a flow graph");
    // whether i must be rebuilt before i am read
    product.def_property_readonly(
        // the name
        "stale",
        // the implementation
        &product_t::stale,
        // the docstring
        "whether i must be rebuilt before i am read");
    // rebuild
    product.def(
        // the name
        "make",
        // the implementation
        [](product_t & self) -> void {
            // ask my writers to refresh me
            self.make();
            // all done
            return;
        },
        // the docstring
        "ask my writers to refresh me");

    // factories
    auto factory = py::classh<factory_t, node_t>(
        // the scope
        m,
        // the name of the class
        "Factory",
        // the docstring
        "the base of the factories of a flow graph");
    // the descriptions of my slots
    factory.def_property_readonly(
        // the name
        "slots",
        // the implementation
        [](const factory_t & self) -> factory_t::slots_type { return self.slots(); },
        // the docstring
        "the descriptions of my slots, in the order i declare them");
    // the descriptions of my settings
    factory.def_property_readonly(
        // the name
        "settings",
        // the implementation
        [](const factory_t & self) -> factory_t::settings_type { return self.settings(); },
        // the docstring
        "the descriptions of my settings");
    // the products bound to my inputs
    factory.def_property_readonly(
        // the name
        "inputs",
        // the implementation
        [](const factory_t & self) -> factory_t::connectors_type { return self.inputs(); },
        // the docstring
        "the products bound to my input slots, by slot name");
    // the products bound to my outputs
    factory.def_property_readonly(
        // the name
        "outputs",
        // the implementation
        [](const factory_t & self) -> factory_t::connectors_type { return self.outputs(); },
        // the docstring
        "the products bound to my output slots, by slot name");
    // checked binding
    factory.def(
        // the name
        "bind",
        // the implementation
        &factory_t::bind,
        // the signature
        "slot"_a, "product"_a,
        // the docstring
        "bind my {slot} to {product}; false, and nothing bound, if i have no such slot or "
        "{product} is not one it takes");
    // undoing a binding
    factory.def(
        // the name
        "unbind",
        // the implementation
        &factory_t::unbind,
        // the signature
        "slot"_a,
        // the docstring
        "undo the binding of my {slot}; false if i have no such slot or it is not bound");
    // reading a setting
    factory.def(
        // the name
        "get",
        // the implementation
        &factory_t::get,
        // the signature
        "setting"_a,
        // the docstring
        "the value of my {setting}; None if i have no such setting");
    // changing a setting
    factory.def(
        // the name
        "set",
        // the implementation
        &factory_t::set,
        // the signature
        "setting"_a, "value"_a,
        // the docstring
        "change my {setting} to {value}; false if i have no such setting or {value} is not of "
        "its type");

    // all done
    return;
}


// end of file
