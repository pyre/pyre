// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Compound.h"
// the reporting of library refusals
#include "../diagnostics.h"


// adopt an existing raw handle
pyre::h5::types::Compound::Compound(id_type id) : Datatype(id) {}


// make a fresh compound type of the given {size}, in bytes
pyre::h5::types::Compound::Compound(std::size_t size) :
    Datatype(static_cast<id_type>(H5Tcreate(H5T_COMPOUND, size)))
{
    // if the library refused
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "creating a compound datatype");
    }
}


// the number of members i have
auto
pyre::h5::types::Compound::members() const -> int
{
    // ask the library
    auto answer = H5Tget_nmembers(id());
    // if it refused
    if (answer < 0) {
        // complain
        complain("pyre.h5.types", "counting the members of a compound datatype");
        // and hand back nothing
        return 0;
    }
    // otherwise, report
    return answer;
}


// the name of the member at {index}
auto
pyre::h5::types::Compound::memberName(unsigned int index) const -> string_t
{
    // the library hands back a freshly allocated c string
    char * raw = H5Tget_member_name(id(), index);
    // or nothing, when it refuses
    if (raw == nullptr) {
        // in which case complain
        complain(
            "pyre.h5.types",
            "retrieving the name of member " + std::to_string(index) + " of a compound datatype");
        // and there is no name
        return "";
    }
    // copy it into a managed string
    string_t name(raw);
    // give the library's buffer back
    H5free_memory(raw);
    // and report
    return name;
}


// the index of the member by the given {name}
auto
pyre::h5::types::Compound::memberIndex(const string_t & name) const -> int
{
    // ask the library
    auto answer = H5Tget_member_index(id(), name.data());
    // if it refused
    if (answer < 0) {
        // complain
        complain("pyre.h5.types", "looking up a member of a compound datatype by name");
        // and hand back nothing
        return -1;
    }
    // otherwise, report
    return answer;
}


// the byte offset of the member at {index}
auto
pyre::h5::types::Compound::memberOffset(unsigned int index) const -> std::size_t
{
    // ask the library; a refusal answers zero, which is also the offset of the first member,
    // so there is no telling the two apart here and the answer travels as it is
    return H5Tget_member_offset(id(), index);
}


// the class of the member at {index}
auto
pyre::h5::types::Compound::memberClass(unsigned int index) const -> class_type
{
    // ask the library
    auto answer = H5Tget_member_class(id(), index);
    // if it refused
    if (answer == H5T_NO_CLASS) {
        // complain
        complain("pyre.h5.types", "retrieving the class of a member of a compound datatype");
        // and hand back nothing
        return H5T_NO_CLASS;
    }
    // otherwise, report
    return answer;
}


// the type of the member at {index}, as a fresh handle the caller adopts
auto
pyre::h5::types::Compound::memberType(unsigned int index) const -> id_type
{
    // ask the library; the result is a fresh handle the caller owns
    auto hid = H5Tget_member_type(id(), index);
    // if it refused
    if (hid < 0) {
        // complain
        complain(
            "pyre.h5.types",
            "retrieving the type of member " + std::to_string(index) + " of a compound datatype");
    }
    // hand off the handle, invalid if the library refused
    return static_cast<id_type>(hid);
}


// insert {name} of {type} at the given {offset}
auto
pyre::h5::types::Compound::insert(const string_t & name, std::size_t offset, const Datatype & type)
    -> void
{
    // hand it to the library
    if (H5Tinsert(id(), name.data(), offset, type.id()) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "inserting member '" + name + "' into a compound datatype");
    }
    // all done
    return;
}


// recursively remove padding from within me
auto
pyre::h5::types::Compound::pack() -> void
{
    // ask the library
    if (H5Tpack(id()) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "packing a compound datatype");
    }
    // all done
    return;
}


// end of file
