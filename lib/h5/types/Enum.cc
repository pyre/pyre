// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Enum.h"
// the reporting of library refusals
#include "../diagnostics.h"


// make an empty enumeration type with no handle yet
pyre::h5::types::Enum::Enum() : Datatype(static_cast<id_type>(H5I_INVALID_HID)) {}


// adopt an existing raw handle
pyre::h5::types::Enum::Enum(id_type id) : Datatype(id) {}


// the number of members i have
auto
pyre::h5::types::Enum::members() const -> int
{
    // ask the library
    auto answer = H5Tget_nmembers(id());
    // if it refused
    if (answer < 0) {
        // complain
        complain("pyre.h5.types", "counting the members of an enumeration type");
        // and hand back nothing
        return 0;
    }
    // otherwise, report
    return answer;
}


// the value of the member at {index}
auto
pyre::h5::types::Enum::memberValue(unsigned int index) const -> long
{
    // make room for the answer
    long value = 0;
    // ask the library; an answer it refuses to give is not one to read
    if (H5Tget_member_value(id(), index, &value) < 0) {
        // so complain
        complain(
            "pyre.h5.types",
            "retrieving the value of member " + std::to_string(index) + " of an enumeration type");
        // and hand back nothing
        return 0;
    }
    // and report
    return value;
}


// the name of the member with the given {value}
auto
pyre::h5::types::Enum::nameOf(long value) const -> string_t
{
    // the longest name we are prepared to retrieve
    constexpr std::size_t limit = 256;
    // make a buffer to hold it
    string_t name(limit, '\0');
    // ask the library to fill it; a value it does not know has no name
    if (H5Tenum_nameof(id(), &value, name.data(), limit) < 0) {
        // so complain
        complain(
            "pyre.h5.types",
            "looking up the name of value " + std::to_string(value) + " in an enumeration type");
        // and hand back nothing
        return "";
    }
    // trim to the actual contents, dropping the trailing nulls
    name.resize(std::char_traits<char>::length(name.data()));
    // and report
    return name;
}


// end of file
