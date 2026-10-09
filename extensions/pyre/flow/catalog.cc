// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the catalog of the kinds of nodes this extension was compiled with; it holds descriptions and
// the functions that make nodes, never a node, so it may outlive the interpreter
auto
pyre::py::flow::registry() -> catalog_t &
{
    // the one catalog
    static catalog_t catalog;
    // hand it off
    return catalog;
}


// the catalog and its entries
void
pyre::py::flow::catalog(py::module & m)
{
    // the shape of the products the catalog makes
    using shape_t = catalog_t::shape_type;

    // what the catalog knows about a kind of product
    auto productEntry = py::class_<product_entry_t>(
        // the scope
        m,
        // the name of the class
        "ProductEntry",
        // the docstring
        "what the catalog knows about a kind of product");
    // the declaration of its type
    productEntry.def_property_readonly(
        // the name
        "decl",
        // the implementation
        &product_entry_t::decl,
        // the docstring
        "the declaration of the type of my products, which is my key in the catalog");
    // its readable name
    productEntry.def_property_readonly(
        // the name
        "className",
        // the implementation
        &product_entry_t::className,
        // the docstring
        "the readable name of the class of my products");
    // the declaration of the type of its cells
    productEntry.def_property_readonly(
        // the name
        "cell",
        // the implementation
        &product_entry_t::cell,
        // the docstring
        "the declaration of the type of the cells of my products; empty for products that are "
        "not grids of cells");

    // what the catalog knows about a kind of factory
    auto factoryEntry = py::class_<factory_entry_t>(
        // the scope
        m,
        // the name of the class
        "FactoryEntry",
        // the docstring
        "what the catalog knows about a kind of factory");
    // the declaration of its type
    factoryEntry.def_property_readonly(
        // the name
        "decl",
        // the implementation
        &factory_entry_t::decl,
        // the docstring
        "the declaration of the type of my factories, which is my key in the catalog");
    // its readable name
    factoryEntry.def_property_readonly(
        // the name
        "className",
        // the implementation
        &factory_entry_t::className,
        // the docstring
        "the readable name of the class of my factories");
    // the descriptions of its slots
    factoryEntry.def_property_readonly(
        // the name
        "slots",
        // the implementation
        &factory_entry_t::slots,
        // the docstring
        "the descriptions of the slots of my factories, in the order they declare them");
    // the descriptions of its settings
    factoryEntry.def_property_readonly(
        // the name
        "settings",
        // the implementation
        &factory_entry_t::settings,
        // the docstring
        "the descriptions of the settings of my factories");

    // the catalog
    auto cls = py::class_<catalog_t>(
        // the scope
        m,
        // the name of the class
        "Catalog",
        // the docstring
        "the catalog of the kinds of nodes that were compiled in");
    // the kinds of products
    cls.def_property_readonly(
        // the name
        "products",
        // the implementation
        &catalog_t::products,
        // the docstring
        "the kinds of products i know, by the declarations of their types");
    // the kinds of factories
    cls.def_property_readonly(
        // the name
        "factories",
        // the implementation
        &catalog_t::factories,
        // the docstring
        "the kinds of factories i know, by the declarations of their types");
    // making a product
    cls.def(
        // the name
        "makeProduct",
        // the implementation
        [](const catalog_t & self, const string_t & decl, const string_t & name,
           std::tuple<int, int> shape) -> catalog_t::product_ref_type {
            // unpack the shape
            auto [lines, samples] = shape;
            // and ask the catalog
            return self.makeProduct(decl, name, shape_t { lines, samples });
        },
        // the signature
        "decl"_a, "name"_a, "shape"_a,
        // the docstring
        "make a product of the type declared as {decl}, named {name}, of the given {shape}; "
        "None if i do not know the type");
    // making a factory
    cls.def(
        // the name
        "makeFactory",
        // the implementation
        &catalog_t::makeFactory,
        // the signature
        "decl"_a, "name"_a,
        // the docstring
        "make a factory of the type declared as {decl}, named {name}; None if i do not know "
        "the type");

    // the catalog of this extension
    m.def(
        // the name
        "catalog",
        // the implementation
        &registry,
        // the return value policy: the catalog belongs to the extension
        py::return_value_policy::reference,
        // the docstring
        "the catalog of the kinds of nodes this extension was compiled with");

    // all done
    return;
}


// end of file
