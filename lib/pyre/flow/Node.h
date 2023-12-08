// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::flow::Node : public std::enable_shared_from_this<Node> {
    // type aliases
protected:
    struct sentinel_type {};

    // metamethods
protected:
    // constructors
    inline Node(sentinel_type);

    // accessors
public:
    inline auto stale() const -> bool;

    // implementation details - interface
protected:
    virtual auto flush() -> void;

    // implementation details - data
private:
    bool _stale;

    // default metamethods
public:
    // destructor
    virtual ~Node() = default;

    // suppressed constructors
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