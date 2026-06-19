// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Compound.h"


// adopt an existing raw handle
pyre::h5::types::Compound::Compound(id_type id) : Datatype(id) {}


// make a fresh compound type of the given {size}, in bytes
pyre::h5::types::Compound::Compound(std::size_t size) :
    Datatype(static_cast<id_type>(H5Tcreate(H5T_COMPOUND, size)))
{}


// the number of members i have
auto
pyre::h5::types::Compound::members() const -> int
{
    // ask the library
    return H5Tget_nmembers(id());
}


// the name of the member at {index}
auto
pyre::h5::types::Compound::memberName(unsigned int index) const -> string_t
{
    // the library hands back a freshly allocated c string
    char * raw = H5Tget_member_name(id(), index);
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
    return H5Tget_member_index(id(), name.data());
}


// the byte offset of the member at {index}
auto
pyre::h5::types::Compound::memberOffset(unsigned int index) const -> std::size_t
{
    // ask the library
    return H5Tget_member_offset(id(), index);
}


// the class of the member at {index}
auto
pyre::h5::types::Compound::memberClass(unsigned int index) const -> class_type
{
    // ask the library
    return H5Tget_member_class(id(), index);
}


// the type of the member at {index}, as a fresh handle the caller adopts
auto
pyre::h5::types::Compound::memberType(unsigned int index) const -> id_type
{
    // ask the library; the result is a fresh handle the caller owns
    return static_cast<id_type>(H5Tget_member_type(id(), index));
}


// insert {name} of {type} at the given {offset}
auto
pyre::h5::types::Compound::insert(const string_t & name, std::size_t offset, const Datatype & type) -> void
{
    // hand it to the library
    H5Tinsert(id(), name.data(), offset, type.id());
    // all done
    return;
}


// recursively remove padding from within me
auto
pyre::h5::types::Compound::pack() -> void
{
    // ask the library
    H5Tpack(id());
    // all done
    return;
}


// end of file
