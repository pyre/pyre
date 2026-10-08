// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// every node of a workflow lives in a shared pointer, because nodes hand out references to
// themselves: binding a product to a factory records each of them on the other, through {ref}, and
// {shared_from_this} only works on an object a shared pointer already owns; a node made any other
// way would fail the first time it is bound
//
// so nodes are made by the static {create} of each class, which builds the node with
// {std::make_shared}; {make_shared} can only call a public constructor, so the constructors of
// the classes that can be made are public, but each one takes a {sentinel_type} as its first
// argument; the sentinel is a protected member of {Node}, which only {Node} and the classes that
// derive from it can name, so only their {create} can build one, and every other caller has to
// go through {create}; {Node} itself is never made on its own, and its constructor is protected
//
// a constructor cannot hand out a reference to the node it is building, since no shared pointer
// owns it yet; anything that needs one, such as binding the node to others, happens once {create}
// has made it


// the base class for all workflow nodes
// it describes the basic obligations and
class pyre::flow::protocols::Node : public std::enable_shared_from_this<Node> {
    // type aliases
public:
    // me
    using self_type = Node;
    // my superclass
    using super_type = std::enable_shared_from_this<Node>;
    // names
    using name_type = string_t;
    // shared pointers to nodes; the bindings between products and factories hold these in both
    // directions, so a workflow keeps itself alive until its bindings are removed, and taking it
    // apart is the responsibility of its client
    using node_ref_type = std::shared_ptr<protocols::Node>;
    using factory_ref_type = std::shared_ptr<protocols::Factory>;
    using product_ref_type = std::shared_ptr<protocols::Product>;
    // weak pointers to nodes; holding one side of each binding through these would let a
    // workflow go away on its own; they have no ordering of their own, since what they point to can
    // expire, so an ordered container holds them with {std::owner_less}, which orders them by the
    // control block they share and stays valid after they expire
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
