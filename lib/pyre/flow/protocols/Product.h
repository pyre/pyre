// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "Node.h"

class pyre::flow::protocols::Product : public Node {
    // type aliases
public:
    // me
    using self_type = Product;
    // my superclass
    using super_type = Node;
    // a binding: the name of the factory slot, and the factory that reads or writes me through it,
    // which i do not keep alive
    using slot_type = std::tuple<name_type, factory_weakref_type>;
    // bindings are ordered by the name of the slot, and then by the factory, compared by the block
    // that manages it, so a factory that has gone away keeps its place
    struct slot_order_type {
        // compare two bindings
        inline auto operator()(const slot_type &, const slot_type &) const -> bool;
    };
    // my bindings
    using connections_type = std::set<slot_type, slot_order_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", bool stale = false) -> product_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Product();
    // constructor. not usable directly; call {create} instead
    inline Product(sentinel_type, const name_type & name, bool stale);

    // accessors
public:
    inline auto stale() const -> bool;
    inline auto readers() const -> const connections_type &;
    inline auto writers() const -> const connections_type &;

    // mutators
public:
    inline auto dirty() -> void;
    inline auto clean() -> void;

    // interface
public:
    // bindings
    virtual auto addReader(name_type slot, factory_ref_type factory) -> product_ref_type;
    virtual auto addWriter(name_type slot, factory_ref_type factory) -> product_ref_type;

    virtual auto removeReader(name_type slot, factory_ref_type factory) -> product_ref_type;
    virtual auto removeWriter(name_type slot, factory_ref_type factory) -> product_ref_type;

    // build a reference to me
    inline auto ref() -> product_ref_type;
    // ask my factories to remake me
    virtual auto make() -> product_ref_type;
    // invalidate me and my upstream graph
    virtual auto flush() -> void override;

    // implementation details - data
private:
    // flag that indicates whether i should be refreshed
    bool _stale;
    // the set of factories that consume my data
    connections_type _readers;
    // the set of factories that produce my data
    connections_type _writers;

    // suppressed metamethods
private:
    // constructors
    Product(const Product &) = delete;
    Product & operator=(const Product &) = delete;
    Product(Product &&) = delete;
    Product & operator=(Product &&) = delete;
};

// get the inline definitions
#include "Product.icc"


// end of file
