// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

class pyre::flow::protocol::Product : public Node {
    // type aliases
public:
    // pair the factory slot name with a reference to the factory
    // ideally, these should be weak pointers but the STL doesn't seem to support
    // placing weak pointers in sets; so tearing down the workflow is the user's responsibility,
    // until an alternative is found
    using slot_type = std::tuple<name_type, factory_ref_type>;
    // my bindings
    using connections_type = std::set<slot_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", bool stale = false) -> product_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Product();
    // constructor; not usable directly. call {create} instead
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