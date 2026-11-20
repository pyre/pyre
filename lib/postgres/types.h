// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the identifiers postgres assigns to its built in types
//
// these are fixed in the server's own catalog, the same in every database and every release, and
// they are how a result set says what each of its columns holds. the names are the ones sql
// gives the types, since several of postgres's own spellings are c++ keywords
namespace pyre::postgres::types {
    // truth
    inline constexpr oid_t boolean = 16;
    // raw octets
    inline constexpr oid_t bytea = 17;
    // the single octet the server uses in its own catalog, spelled {"char"} in sql
    inline constexpr oid_t internalChar = 18;
    // the identifiers of the catalog
    inline constexpr oid_t name = 19;
    // whole numbers, in each of their widths
    inline constexpr oid_t bigint = 20;
    inline constexpr oid_t smallint = 21;
    inline constexpr oid_t integer = 23;
    // text of any length
    inline constexpr oid_t text = 25;
    // the identifiers of the catalog's own rows
    inline constexpr oid_t oid = 26;
    // json documents, as text and in the server's parsed form
    inline constexpr oid_t json = 114;
    inline constexpr oid_t jsonb = 3802;
    // real numbers, in each of their widths
    inline constexpr oid_t real = 700;
    inline constexpr oid_t doublePrecision = 701;
    // text padded to a fixed length, and text limited to one
    inline constexpr oid_t character = 1042;
    inline constexpr oid_t characterVarying = 1043;
    // the calendar and the clock
    inline constexpr oid_t date = 1082;
    inline constexpr oid_t time = 1083;
    inline constexpr oid_t timestamp = 1114;
    inline constexpr oid_t timestampWithTimeZone = 1184;
    inline constexpr oid_t interval = 1186;
    inline constexpr oid_t timeWithTimeZone = 1266;
    // exact numbers
    inline constexpr oid_t numeric = 1700;
    // universally unique identifiers
    inline constexpr oid_t uuid = 2950;
} // namespace pyre::postgres::types


// the identifiers of the arrays of each of them
namespace pyre::postgres::types::arrays {
    // truth
    inline constexpr oid_t boolean = 1000;
    // raw octets
    inline constexpr oid_t bytea = 1001;
    // the catalog's single octets and identifiers
    inline constexpr oid_t internalChar = 1002;
    inline constexpr oid_t name = 1003;
    // whole numbers
    inline constexpr oid_t bigint = 1016;
    inline constexpr oid_t smallint = 1005;
    inline constexpr oid_t integer = 1007;
    // text
    inline constexpr oid_t text = 1009;
    // the identifiers of the catalog's own rows
    inline constexpr oid_t oid = 1028;
    // json documents
    inline constexpr oid_t json = 199;
    inline constexpr oid_t jsonb = 3807;
    // real numbers
    inline constexpr oid_t real = 1021;
    inline constexpr oid_t doublePrecision = 1022;
    // padded and limited text
    inline constexpr oid_t character = 1014;
    inline constexpr oid_t characterVarying = 1015;
    // the calendar and the clock
    inline constexpr oid_t date = 1182;
    inline constexpr oid_t time = 1183;
    inline constexpr oid_t timestamp = 1115;
    inline constexpr oid_t timestampWithTimeZone = 1185;
    inline constexpr oid_t interval = 1187;
    inline constexpr oid_t timeWithTimeZone = 1270;
    // exact numbers
    inline constexpr oid_t numeric = 1231;
    // universally unique identifiers
    inline constexpr oid_t uuid = 2951;
} // namespace pyre::postgres::types::arrays


// the type of the entries of the arrays above
namespace pyre::postgres::types {
    // the type of the entries of an array of type {array}, or {invalidOid} when {array} is not
    // one of the arrays of a built in type
    constexpr auto element(oid_t array) -> oid_t
    {
        // go through the arrays this file knows
        switch (array) {
            case arrays::boolean:
                return boolean;
            case arrays::bytea:
                return bytea;
            case arrays::internalChar:
                return internalChar;
            case arrays::name:
                return name;
            case arrays::bigint:
                return bigint;
            case arrays::smallint:
                return smallint;
            case arrays::integer:
                return integer;
            case arrays::text:
                return text;
            case arrays::oid:
                return oid;
            case arrays::json:
                return json;
            case arrays::jsonb:
                return jsonb;
            case arrays::real:
                return real;
            case arrays::doublePrecision:
                return doublePrecision;
            case arrays::character:
                return character;
            case arrays::characterVarying:
                return characterVarying;
            case arrays::date:
                return date;
            case arrays::time:
                return time;
            case arrays::timestamp:
                return timestamp;
            case arrays::timestampWithTimeZone:
                return timestampWithTimeZone;
            case arrays::interval:
                return interval;
            case arrays::timeWithTimeZone:
                return timeWithTimeZone;
            case arrays::numeric:
                return numeric;
            case arrays::uuid:
                return uuid;
        }
        // anything else is not an array this file knows
        return invalidOid;
    }
} // namespace pyre::postgres::types


// end of file
