// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// the products i make
#include "../protocols/Product.h"


// what the catalog knows about a kind of product: the declaration of its type, a readable name,
// and how to make one with a given name and shape
class pyre::flow::catalog::ProductEntry {
    // type aliases
public:
    // me
    using self_type = ProductEntry;
    // the declarations of types, and the names of things
    using decl_type = string_t;
    using name_type = string_t;
    // the shape of the products i make
    using shape_type = pyre::grid::shape_t<2>;
    // the products i make
    using product_ref_type = std::shared_ptr<protocols::Product>;
    // how to make one
    using maker_type = std::function<product_ref_type(const name_type &, shape_type)>;

    // metamethods
public:
    // constructor
    inline ProductEntry(
        decl_type decl, name_type className, decl_type cell, bool makes, maker_type make);
    // destructor
    ~ProductEntry() = default;
    // entries are values: they copy and move freely
    ProductEntry(const ProductEntry &) = default;
    ProductEntry(ProductEntry &&) = default;
    ProductEntry & operator=(const ProductEntry &) = default;
    ProductEntry & operator=(ProductEntry &&) = default;

    // accessors
public:
    // the declaration of the type of my products, which is my key in the catalog
    inline auto decl() const -> const decl_type &;
    // the readable name of their class
    inline auto className() const -> const name_type &;
    // the declaration of the type of their cells; empty for products that are not grids of cells
    inline auto cell() const -> const decl_type &;
    // whether i can make products from a shape; products that wrap cells they do not own come
    // into a graph made by whoever owns the cells
    inline auto makes() const -> bool;

    // interface
public:
    // make a product named {name} of the given {shape}; nothing for products that wrap cells they
    // do not own, which come into a graph made by whoever owns the cells
    inline auto make(const name_type & name, shape_type shape) const -> product_ref_type;

    // implementation details - data
private:
    // the declaration of the type of my products
    decl_type _decl;
    // the readable name of their class
    name_type _className;
    // the declaration of the type of their cells
    decl_type _cell;
    // whether i can make them from a shape
    bool _makes;
    // how to make one
    maker_type _make;
};

// get the inline definitions
#include "ProductEntry.icc"


// end of file
