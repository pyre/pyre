// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::flow::Product : public Node {
    // metamethods
protected:
    // constructors
    inline Product();

    // implementation details - interface
protected:
    virtual auto flush() -> void override;

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