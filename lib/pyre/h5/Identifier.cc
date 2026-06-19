// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Identifier.h"


// adopt an existing {id}, taking ownership of the reference it carries
pyre::h5::Identifier::Identifier(id_type id) : _id { id } {}


// share the handle of {other}, taking out another reference to it
pyre::h5::Identifier::Identifier(const Identifier & other) : _id { other._id }
{
    // record that there is now one more owner of the handle
    _retain();
    // all done
    return;
}


// steal the handle of {other}, leaving it empty
pyre::h5::Identifier::Identifier(Identifier && other) noexcept : _id { other._id }
{
    // so that the source no longer refers to the handle
    other._id = H5I_INVALID_HID;
}


// release my handle and share {other}'s
pyre::h5::Identifier &
pyre::h5::Identifier::operator=(const Identifier & other)
{
    // guard against self-assignment
    if (this != &other) {
        // give up my current handle
        _release();
        // adopt the new one
        _id = other._id;
        // and record the additional owner
        _retain();
    }
    // hand off a reference to me
    return *this;
}


// release my handle and steal {other}'s
pyre::h5::Identifier &
pyre::h5::Identifier::operator=(Identifier && other) noexcept
{
    // guard against self-assignment
    if (this != &other) {
        // give up my current handle
        _release();
        // steal the source's
        _id = other._id;
        // and empty it
        other._id = H5I_INVALID_HID;
    }
    // hand off a reference to me
    return *this;
}


// release my reference to my handle
pyre::h5::Identifier::~Identifier()
{
    // give up my reference
    _release();
    // all done
    return;
}


// give up a reference to my handle, if it is live
auto
pyre::h5::Identifier::_release() -> void
{
    // a dead handle has nothing to release
    if (!valid()) {
        // so there is nothing to do
        return;
    }
    // otherwise, decrement the library's reference count, which closes the object at zero
    if (H5Idec_ref(_id) < 0) {
        // a failure here means the handle bookkeeping is inconsistent: a bug
        auto channel = pyre::journal::firewall_t("pyre.h5.identifier");
        // so complain
        channel
            // mark
            << pyre::journal::here()
            // what
            << "failed to release the hdf5 handle " << _id
            << pyre::journal::newline
            // flush
            << pyre::journal::endl;
    }
    // mark me empty so a later access doesn't touch a stale handle
    _id = H5I_INVALID_HID;
    // all done
    return;
}


// end of file
