// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// the description of a slot of a factory: its name, whether the factory reads or writes the
// product bound to it, the declaration of the products it takes, and a check that a given product
// is one of them; factories describe their slots so that an editor can draw them before anything
// is bound, and so that a binding made by name can be checked against the types the factory
// computes with
class pyre::flow::protocols::Slot {
    // type aliases
public:
    // me
    using self_type = Slot;
    // the names of slots
    using name_type = string_t;
    // the declarations of the products a slot takes
    using decl_type = string_t;
    // the products
    using product_ref_type = std::shared_ptr<Product>;
    // the check that a product fits
    using accepts_type = std::function<bool(const product_ref_type &)>;

    // factories
public:
    // describe a slot {name} that reads products of type {productT}
    template <class productT>
    static inline auto input(const name_type & name) -> self_type;
    // describe a slot {name} that writes products of type {productT}
    template <class productT>
    static inline auto output(const name_type & name) -> self_type;

    // metamethods
public:
    // constructor
    inline Slot(name_type name, bool reads, decl_type product, accepts_type accepts);
    // destructor
    ~Slot() = default;
    // descriptions are values: they copy and move freely
    Slot(const Slot &) = default;
    Slot(Slot &&) = default;
    Slot & operator=(const Slot &) = default;
    Slot & operator=(Slot &&) = default;

    // accessors
public:
    // my name
    inline auto name() const -> const name_type &;
    // whether my factory reads the product bound to me
    inline auto reads() const -> bool;
    // whether my factory writes the product bound to me
    inline auto writes() const -> bool;
    // the declaration of the products i take
    inline auto product() const -> const decl_type &;

    // interface
public:
    // check whether {product} is one of the products i take
    inline auto accepts(const product_ref_type & product) const -> bool;

    // implementation details - data
private:
    // my name
    name_type _name;
    // whether my factory reads the product bound to me, rather than writes it
    bool _reads;
    // the declaration of the products i take
    decl_type _product;
    // the check that a product is one of them
    accepts_type _accepts;
};

// get the inline definitions
#include "Slot.icc"


// end of file
