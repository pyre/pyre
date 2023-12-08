// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::flow::Factory : public Node {
    // metamethods
protected:
    // constructors
    inline Factory(sentinel_type);

    // implementation details - interface
protected:
    virtual auto flush() -> void override;

    // default metamethods
public:
    // destructor
    virtual ~Factory() = default;

    // suppressed metamethods
private:
    // constructors
    Factory(const Factory &) = delete;
    Factory & operator=(const Factory &) = delete;
    Factory(Factory &&) = delete;
    Factory & operator=(Factory &&) = delete;
};

// get the inline definitions
#include "Factory.icc"

// end of file