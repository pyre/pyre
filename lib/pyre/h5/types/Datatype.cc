// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Datatype.h"
// my predefined-type sibling, so i can copy one
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::Datatype::Datatype(id_type id) : Identifier(id) {}


// make an independent copy of a predefined type
pyre::h5::types::Datatype::Datatype(const Predefined & type) :
    Identifier(static_cast<id_type>(H5Tcopy(type.id())))
{}


// the name of my class, for diagnostics
auto
pyre::h5::types::Datatype::className() const -> string_t
{
    // the generic case
    return "Datatype";
}


// my class: integer, float, string, ...
auto
pyre::h5::types::Datatype::cell() const -> class_type
{
    // ask the library
    return H5Tget_class(id());
}


// my size, in bytes
auto
pyre::h5::types::Datatype::bytes() const -> std::size_t
{
    // ask the library
    return H5Tget_size(id());
}


// resize me to {size} bytes
auto
pyre::h5::types::Datatype::setBytes(std::size_t size) -> void
{
    // hand it to the library
    H5Tset_size(id(), size);
    // all done
    return;
}


// the base type from which i am derived
auto
pyre::h5::types::Datatype::super() const -> Datatype
{
    // ask the library for the base type, which hands back a fresh handle, and adopt it
    return Datatype(static_cast<id_type>(H5Tget_super(id())));
}


// whether i am, or contain, a member of the given {cls}
auto
pyre::h5::types::Datatype::isA(class_type cls) const -> bool
{
    // ask the library; a positive answer means a match
    return H5Tdetect_class(id(), cls) > 0;
}


// a binary description of me, as raw bytes in a string
auto
pyre::h5::types::Datatype::encode() const -> string_t
{
    // find out how big the description is
    std::size_t size = 0;
    H5Tencode(id(), nullptr, &size);
    // make a buffer to hold it
    string_t buffer(size, '\0');
    // fill it
    H5Tencode(id(), buffer.data(), &size);
    // and report
    return buffer;
}


// the type described by the binary {buffer}
auto
pyre::h5::types::Datatype::decode(const string_t & buffer) const -> Datatype
{
    // ask the library to reconstitute the type, which hands back a fresh handle, and adopt it
#if H5_VERSION_GE(1, 14, 3)
    // newer releases want the buffer size, so out-of-bounds reads can be caught
    return Datatype(static_cast<id_type>(H5Tdecode2(buffer.data(), buffer.size())));
#else
    // older releases trust the buffer to be well formed
    return Datatype(static_cast<id_type>(H5Tdecode(buffer.data())));
#endif
}


// release my handle
auto
pyre::h5::types::Datatype::close() -> void
{
    // give up my reference; the library closes the type when the last one goes away
    _release();
    // all done
    return;
}


// end of file
