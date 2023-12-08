// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::flow::Node : public std::enable_shared_from_this<Node> {
    // type aliases
public:
    // names
    using name_type = string_t;
    // shared pointers to nodes
    using node_ref_type = node_ref_t;
    using factory_ref_type = factory_ref_t;
    using product_ref_type = product_ref_t;

protected:
    // internal type that is used to prohibit external access to the constructors
    // of all classes in my hierarchy
    struct sentinel_type {};

    // metamethods
protected:
    // constructors
    inline Node(sentinel_type);

    // interface
public:
    // invalidate me
    virtual auto flush() -> void;

    // implementation details - data
private:
    bool _stale;

    // default metamethods
public:
    // destructor
    virtual ~Node() = default;

    // suppressed metamethods
private:
    // constructors
    Node(const Node &) = delete;
    Node & operator=(const Node &) = delete;
    Node(Node &&) = delete;
    Node & operator=(Node &&) = delete;
};

// get the inline definitions
#include "Node.icc"

// end of file