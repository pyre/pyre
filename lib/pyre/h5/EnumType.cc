// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "EnumType.h"


// make an empty enumeration type with no handle yet
pyre::h5::EnumType::EnumType() : DataType(static_cast<id_type>(H5I_INVALID_HID)) {}


// adopt an existing raw handle
pyre::h5::EnumType::EnumType(id_type id) : DataType(id) {}


// the number of members i have
auto
pyre::h5::EnumType::members() const -> int
{
    // ask the library
    return H5Tget_nmembers(id());
}


// the value of the member at {index}
auto
pyre::h5::EnumType::memberValue(unsigned int index) const -> long
{
    // make room for the answer
    long value = 0;
    // ask the library
    H5Tget_member_value(id(), index, &value);
    // and report
    return value;
}


// the name of the member with the given {value}
auto
pyre::h5::EnumType::nameOf(long value) const -> string_t
{
    // the longest name we are prepared to retrieve
    constexpr std::size_t limit = 256;
    // make a buffer to hold it
    string_t name(limit, '\0');
    // ask the library to fill it
    H5Tenum_nameof(id(), &value, name.data(), limit);
    // trim to the actual contents, dropping the trailing nulls
    name.resize(std::char_traits<char>::length(name.data()));
    // and report
    return name;
}


// end of file
