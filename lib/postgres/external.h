// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <charconv>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <exception>
#include <iterator>
#include <limits>
#include <memory>
#include <optional>
#include <string>
#include <string_view>
#include <type_traits>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
// the postgres client library; {pyre::postgres} is a wrapper over it, and depends on nothing
// else. in particular, nothing python ever reaches this far: the library stands on its own,
// and the bindings are just one of its clients
#include <libpq-fe.h>


// the type aliases that shape this namespace
namespace pyre::postgres {
    // names, sql text, and other things we own
    using string_t = std::string;
    // a borrowed look at text that libpq owns; every value in a result set is handed out this
    // way, so that reading a table does not copy it
    using view_t = std::string_view;
    // the identifier postgres assigns to each type in its catalog
    using oid_t = Oid;
    // the way libpq counts rows and columns; deliberately not {size_t}, which would shadow the
    // global for every unqualified use inside this namespace, and which would also lose the
    // {-1} that libpq returns when it cannot find a column
    using size_type = int;
    // an uninterpreted payload, as it arrives from a {bytea} column
    using bytes_t = std::vector<std::byte>;

    // the name and value of one entry in a connection specification; keeping the two apart is
    // what lets a value, such as a password, contain a space
    using parameter_t = std::pair<string_t, string_t>;
    // a full connection specification
    using parameters_t = std::vector<parameter_t>;

    // the value bound to one placeholder of a parameterized statement; an empty {optional} is
    // how a caller says {NULL}, which is a thing no string can spell
    using argument_t = std::optional<string_t>;
    // the full set of values bound to a parameterized statement
    using arguments_t = std::vector<argument_t>;
} // namespace pyre::postgres


// the libpq constants, hoisted out of the macros the c api hands us
namespace pyre::postgres {
    // the type identifier that names no type at all
    inline constexpr oid_t invalidOid = InvalidOid;
    // the answer when a result cannot find a column under the name it was given
    inline constexpr size_type unknownColumn = -1;
} // namespace pyre::postgres


// end of file
