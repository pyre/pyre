// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my entries
#include "ProductEntry.h"
#include "FactoryEntry.h"


// the catalog of the kinds of nodes that were compiled in: every factory and product is an
// instantiation of a template, so an editor can make only the ones some code registered here;
// each kind is filed under the declaration of its type, which reads the same on every compiler,
// and the catalog knows nothing of the protocols the kinds implement, which belong to python
class pyre::flow::catalog::Catalog {
    // type aliases
public:
    // me
    using self_type = Catalog;
    // the declarations of types, and the names of things
    using decl_type = string_t;
    using name_type = string_t;
    // my entries
    using product_entry_type = ProductEntry;
    using factory_entry_type = FactoryEntry;
    // and their indices
    using products_type = std::map<decl_type, product_entry_type>;
    using factories_type = std::map<decl_type, factory_entry_type>;
    // the shape of the products i make
    using shape_type = product_entry_type::shape_type;
    // the nodes i make
    using product_ref_type = product_entry_type::product_ref_type;
    using factory_ref_type = factory_entry_type::factory_ref_type;

    // metamethods
public:
    // constructor
    Catalog() = default;
    // destructor
    ~Catalog() = default;
    // a catalog is a value: it copies and moves freely
    Catalog(const Catalog &) = default;
    Catalog(Catalog &&) = default;
    Catalog & operator=(const Catalog &) = default;
    Catalog & operator=(Catalog &&) = default;

    // registration
public:
    // file the products of type {productT}, replacing an earlier entry for the same type
    template <class productT>
    inline auto registerProduct() -> const product_entry_type &;
    // file the factories of type {factoryT}, replacing an earlier entry for the same type
    template <class factoryT>
    inline auto registerFactory() -> const factory_entry_type &;

    // accessors
public:
    // the kinds of products i know, by the declarations of their types
    inline auto products() const -> const products_type &;
    // the kinds of factories i know, likewise
    inline auto factories() const -> const factories_type &;

    // lookups
public:
    // the entry of the products whose type is declared as {decl}; nothing if i have none
    inline auto product(const decl_type & decl) const -> const product_entry_type *;
    // the entry of the factories whose type is declared as {decl}; nothing if i have none
    inline auto factory(const decl_type & decl) const -> const factory_entry_type *;

    // interface
public:
    // make a product of the type declared as {decl}, named {name}, of the given {shape};
    // nothing if i do not know the type, or if its products wrap cells they do not own
    inline auto makeProduct(const decl_type & decl, const name_type & name, shape_type shape) const
        -> product_ref_type;
    // make a factory of the type declared as {decl}, named {name}; nothing if i do not know
    // the type
    inline auto makeFactory(const decl_type & decl, const name_type & name) const
        -> factory_ref_type;

    // implementation details - data
private:
    // the kinds of products i know
    products_type _products;
    // the kinds of factories i know
    factories_type _factories;
};

// get the inline definitions
#include "Catalog.icc"


// end of file
