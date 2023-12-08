// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::flow::Product : public Node {
    // type aliases
public:
    // pair the factory slot name with a reference to the fatcory
    using slot_type = std::tuple<name_type, factory_ref_type>;
    // my bindings
    using connections_type = std::set<slot_type>;

    // metamethods
protected:
    // constructors
    inline Product(sentinel_type);

    // accessors
public:
    inline auto stale() const -> bool;
    inline auto readers() const -> const connections_type &;
    inline auto writers() const -> const connections_type &;

    // mutators
public:
    inline auto clean() -> void;

    // interface
public:
    // ask my factories to remake me
    virtual auto sync() -> void;
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

    // default metamethods
public:
    // destructor
    virtual ~Product() = default;

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