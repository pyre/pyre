// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"

class pyre::flow::protocols::Node : public std::enable_shared_from_this<Node> {
    // type aliases
public:
    // me
    using self_type = Node;
    // my superclass
    using super_type = std::enable_shared_from_this<Node>;
    // names
    using name_type = string_t;
    // shared pointers to nodes
    using node_ref_type = std::shared_ptr<protocols::Node>;
    using factory_ref_type = std::shared_ptr<protocols::Factory>;
    using product_ref_type = std::shared_ptr<protocols::Product>;
    // weak pointers to nodes
    using node_weakref_type = std::weak_ptr<protocols::Node>;
    using factory_weakref_type = std::weak_ptr<protocols::Factory>;
    using product_weakref_type = std::weak_ptr<protocols::Product>;

protected:
    // internal type that is used to prohibit external access to the constructors
    // of all classes in my hierarchy
    struct sentinel_type {};

    // metamethods
protected:
    // destructor
    virtual ~Node();
    // constructors
    inline Node(sentinel_type, const name_type &);

    // accessors
public:
    // my name
    inline auto name() const -> const name_type &;

    // mutators
public:
    // my name
    inline auto name(const name_type & name) -> node_ref_type;

    // interface
public:
    // build a reference to me
    inline auto ref() -> node_ref_type;
    // invalidate me
    virtual auto flush() -> void;

    // implementation detail
private:
    // my name
    name_type _name;

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
