// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the owner of an hdf5 object handle
class pyre::h5::Identifier {
    // types
public:
    // hdf5 refers to its objects through opaque integer handles
    using id_type = hid_t;

    // metamethods
public:
    // adopt an existing {id}, taking ownership of the reference it carries
    explicit Identifier(id_type id);
    // share the handle of {other}, taking out another reference to it
    Identifier(const Identifier & other);
    // steal the handle of {other}, leaving it empty
    Identifier(Identifier && other) noexcept;
    // release my handle and share {other}'s
    Identifier & operator=(const Identifier & other);
    // release my handle and steal {other}'s
    Identifier & operator=(Identifier && other) noexcept;
    // release my reference to my handle
    virtual ~Identifier();

    // interface
public:
    // my raw hdf5 handle
    auto id() const -> id_type;
    // whether my handle refers to a live hdf5 object
    auto valid() const -> bool;
    // the number of outstanding references to my handle
    auto refcount() const -> int;
    // contextual conversion to {bool}, true when i am {valid}
    explicit operator bool() const;

    // implementation details
protected:
    // take out a reference to my handle, if it is live
    auto _retain() const -> void;
    // give up a reference to my handle, if it is live
    auto _release() -> void;

    // data
protected:
    // the handle i own
    id_type _id;
};


// get the inline definitions
#include "Identifier.icc"


// end of file
