// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DataType.h"
// my predefined-type sibling, so i can copy one
#include "PredType.h"


// adopt an existing raw handle
pyre::h5::DataType::DataType(id_type id) : Identifier(id) {}


// make an independent copy of a predefined type
pyre::h5::DataType::DataType(const PredType & type) :
    Identifier(static_cast<id_type>(H5Tcopy(type.id())))
{}


// the name of my class, for diagnostics
auto
pyre::h5::DataType::className() const -> string_t
{
    // the generic case
    return "DataType";
}


// my class: integer, float, string, ...
auto
pyre::h5::DataType::cell() const -> class_type
{
    // ask the library
    return H5Tget_class(id());
}


// my size, in bytes
auto
pyre::h5::DataType::bytes() const -> std::size_t
{
    // ask the library
    return H5Tget_size(id());
}


// resize me to {size} bytes
auto
pyre::h5::DataType::setBytes(std::size_t size) -> void
{
    // hand it to the library
    H5Tset_size(id(), size);
    // all done
    return;
}


// the base type from which i am derived
auto
pyre::h5::DataType::super() const -> DataType
{
    // ask the library for the base type, which hands back a fresh handle, and adopt it
    return DataType(static_cast<id_type>(H5Tget_super(id())));
}


// whether i am, or contain, a member of the given {cls}
auto
pyre::h5::DataType::isA(class_type cls) const -> bool
{
    // ask the library; a positive answer means a match
    return H5Tdetect_class(id(), cls) > 0;
}


// a binary description of me, as raw bytes in a string
auto
pyre::h5::DataType::encode() const -> string_t
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
pyre::h5::DataType::decode(const string_t & buffer) const -> DataType
{
    // ask the library to reconstitute the type, which hands back a fresh handle, and adopt it
#if H5_VERSION_GE(1, 14, 3)
    // newer releases want the buffer size, so out-of-bounds reads can be caught
    return DataType(static_cast<id_type>(H5Tdecode2(buffer.data(), buffer.size())));
#else
    // older releases trust the buffer to be well formed
    return DataType(static_cast<id_type>(H5Tdecode(buffer.data())));
#endif
}


// release my handle
auto
pyre::h5::DataType::close() -> void
{
    // give up my reference; the library closes the type when the last one goes away
    _release();
    // all done
    return;
}


// end of file
