// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Datatype.h"
// the reporting of library refusals
#include "../diagnostics.h"
// my predefined-type sibling, so i can copy one
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::Datatype::Datatype(id_type id) : Location(id) {}


// make an independent copy of a predefined type
pyre::h5::types::Datatype::Datatype(const Predefined & type) :
    Location(static_cast<id_type>(H5Tcopy(type.id())))
{
    // if the library refused
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "copying a predefined datatype");
    }
}


// whether i describe the same datatype as {other}
auto
pyre::h5::types::Datatype::operator==(const Datatype & other) const -> bool
{
    // ask the library
    auto answer = H5Tequal(id(), other.id());
    // if it refused to compare them
    if (answer < 0) {
        // complain
        complain("pyre.h5.types", "comparing two datatypes");
        // and call them different
        return false;
    }
    // otherwise, a positive answer means the two types are equal
    return answer > 0;
}


// whether i describe a different datatype than {other}
auto
pyre::h5::types::Datatype::operator!=(const Datatype & other) const -> bool
{
    // the negation of equality
    return !(*this == other);
}


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
    auto answer = H5Tget_class(id());
    // if it refused
    if (answer == H5T_NO_CLASS) {
        // complain
        complain("pyre.h5.types", "retrieving the class of a datatype");
        // and hand back nothing
        return H5T_NO_CLASS;
    }
    // otherwise, report
    return answer;
}


// my size, in bytes
auto
pyre::h5::types::Datatype::bytes() const -> std::size_t
{
    // ask the library
    auto answer = H5Tget_size(id());
    // if it refused
    if (answer == 0) {
        // complain
        complain("pyre.h5.types", "retrieving the size of a datatype");
        // and hand back nothing
        return 0;
    }
    // otherwise, report
    return answer;
}


// resize me to {size} bytes
auto
pyre::h5::types::Datatype::setBytes(std::size_t size) -> void
{
    // hand it to the library
    if (H5Tset_size(id(), size) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "resizing a datatype");
    }
    // all done
    return;
}


// the base type from which i am derived
auto
pyre::h5::types::Datatype::super() const -> Datatype
{
    // ask the library for the base type, which hands back a fresh handle
    auto hid = H5Tget_super(id());
    // if it refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.types", "retrieving the base type of a datatype");
    }
    // adopt the fresh handle, empty if the library refused
    return Datatype(static_cast<id_type>(hid));
}


// whether i am, or contain, a member of the given {cls}
auto
pyre::h5::types::Datatype::isA(class_type cls) const -> bool
{
    // ask the library
    auto answer = H5Tdetect_class(id(), cls);
    // if it refused to look
    if (answer < 0) {
        // complain
        complain("pyre.h5.types", "looking for a class within a datatype");
        // and report no match
        return false;
    }
    // otherwise, a positive answer means a match
    return answer > 0;
}


// a binary description of me, as raw bytes in a string
auto
pyre::h5::types::Datatype::encode() const -> string_t
{
    // find out how big the description is
    std::size_t size = 0;
    // a datatype the library will not describe has no description
    if (H5Tencode(id(), nullptr, &size) < 0) {
        // so complain
        complain("pyre.h5.types", "sizing the binary description of a datatype");
        // and hand back nothing
        return "";
    }
    // make a buffer to hold it
    string_t buffer(size, '\0');
    // fill it; the library will not change its mind between the two calls
    if (H5Tencode(id(), buffer.data(), &size) < 0) {
        // unless something is badly wrong
        complain("pyre.h5.types", "encoding a datatype");
        // in which case there is no description
        return "";
    }
    // and report
    return buffer;
}


// the type described by the binary {buffer}
auto
pyre::h5::types::Datatype::decode(const string_t & buffer) const -> Datatype
{
    // ask the library to reconstitute the type, which hands back a fresh handle
#if H5_VERSION_GE(2, 0, 0)
    // {H5Tdecode2} first appears in 2.0.0; it wants the buffer size, so out-of-bounds reads can be
    // caught
    auto hid = H5Tdecode2(buffer.data(), buffer.size());
#else
    // older releases trust the buffer to be well formed
    auto hid = H5Tdecode(buffer.data());
#endif
    // if the library refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.types", "decoding a datatype from its binary description");
    }
    // adopt the fresh handle, empty if the library refused
    return Datatype(static_cast<id_type>(hid));
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
