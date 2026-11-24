// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// a value that will not parse is a {DataError}, and that is the whole reason this file knows
// about the exception hierarchy
#include "Error.h"


// the translation between the values of a c++ program and the text postgres exchanges
//
// postgres talks to its clients in one of two formats. the binary one is the internal
// representation of each type, and is neither documented nor stable across releases; the text
// one is what the type's own output function produces, and is both. this package speaks text,
// which is what every other client library does by default, and for the same reason
//
// the specializations below cover the types that c++ and postgres already agree about. a client
// with a type of its own writes one more, in its own header, and everything here picks it up


// the machinery the specializations share
namespace pyre::postgres::codecs {
    // complain that {value} is not the text of a {what}, and give up
    [[noreturn]] inline auto reject(view_t value, view_t what) -> void
    {
        // assemble an explanation that names both the text and what we wanted it to be
        string_t message = "cannot interpret '";
        message += value;
        message += "' as ";
        message += what;
        // a value that does not fit its type is precisely what postgres calls a data exception,
        // so raise the exception it would have raised had it caught this on its own side
        throw DataError(Diagnostic(std::move(message)));
    }

    // read a whole number off the front of {value}, and insist that it is the whole of it
    template <typename valueT>
    inline auto whole(view_t value, view_t what) -> valueT
    {
        // room for the answer
        valueT number = 0;
        // parse, which for the integral types is the one conversion the standard library does
        // without a locale, without an allocation, and without a null terminator
        const auto outcome = std::from_chars(value.data(), value.data() + value.size(), number);
        // text that is not a number at all, and text that names one too large for {valueT},
        // are both failures of the same kind as far as a caller is concerned
        if (outcome.ec != std::errc()) {
            codecs::reject(value, what);
        }
        // trailing garbage means the column did not hold what its type said it did
        if (outcome.ptr != value.data() + value.size()) {
            codecs::reject(value, what);
        }
        // hand it off
        return number;
    }

    // read a real number out of {value}
    template <typename valueT>
    inline auto real(view_t value, view_t what) -> valueT
    {
        // room for the answer
        valueT number = 0;
        // parse, the same way whatever the locale of the process; postgres always writes a
        // point, never a comma, and this reads its 'Infinity' and 'NaN' in any case
        const auto outcome = std::from_chars(value.data(), value.data() + value.size(), number);
        // text that is not a number at all, and text that names one too large for {valueT},
        // are both failures of the same kind as far as a caller is concerned
        if (outcome.ec != std::errc()) {
            codecs::reject(value, what);
        }
        // trailing garbage means the column did not hold what its type said it did
        if (outcome.ptr != value.data() + value.size()) {
            codecs::reject(value, what);
        }
        // hand it off
        return number;
    }

    // render the real number {value} as the text postgres reads back without loss
    template <typename valueT>
    inline auto render(valueT value) -> string_t
    {
        // the three values whose spelling postgres does not share with C
        if (std::isnan(value)) {
            return "NaN";
        }
        if (std::isinf(value)) {
            return value > 0 ? "Infinity" : "-Infinity";
        }

        // room for the longest rendering: sign, digits, point and exponent
        char buffer[64];
        // write the shortest text that reads back as exactly {value}, with a point whatever the
        // locale of the process
        const auto outcome = std::to_chars(buffer, buffer + sizeof(buffer), value);
        // running out of room cannot happen for a buffer this size
        if (outcome.ec != std::errc()) {
            auto channel = pyre::journal::firewall_t("pyre.postgres.codecs");
            channel
                // where
                << pyre::journal::here()
                // what
                << "failed to render a floating point value"
                // flush
                << pyre::journal::endl;
            // in a build with firewalls disabled, hand back something the server will reject
            return string_t();
        }

        // hand back exactly the characters that were written
        return string_t(buffer, outcome.ptr);
    }
} // namespace pyre::postgres::codecs


// the specializations
namespace pyre::postgres {
    // text, which postgres and c++ spell the same way
    template <>
    struct Codec<string_t> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // a copy of the value, which the caller then owns
        static inline auto decode(view_t value) -> string_t { return string_t(value); }
        // and back the other way
        static inline auto encode(const string_t & value) -> argument_t { return value; }
    };

    // a borrowed look at the text, for a caller that will read it and move on
    template <>
    struct Codec<view_t> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // note the lifetime: the characters belong to the result set the field came from, and
        // they go away with it. a caller that wants them to outlive it asks for a {string_t}
        static inline auto decode(view_t value) -> view_t { return value; }
        // and back the other way
        static inline auto encode(view_t value) -> argument_t { return string_t(value); }
    };

    // string literals, and anything else that decays to a pointer to characters; these go out
    // to the server, and nothing ever comes back as one
    template <typename charT>
    struct Codec<charT *, std::enable_if_t<std::is_same_v<std::remove_cv_t<charT>, char>>> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // take a copy of whatever the pointer is pointing at
        static inline auto encode(const charT * value) -> argument_t { return string_t(value); }
    };

    // truth, which postgres writes as a single letter
    template <>
    struct Codec<bool> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // read it
        static inline auto decode(view_t value) -> bool
        {
            // the one spelling postgres ever writes
            if (value == "t") {
                return true;
            }
            if (value == "f") {
                return false;
            }
            // and the ones it accepts on the way in, which a hand written query may echo back
            if (value == "true" || value == "1" || value == "y" || value == "yes"
                || value == "on") {
                return true;
            }
            if (value == "false" || value == "0" || value == "n" || value == "no"
                || value == "off") {
                return false;
            }
            // anything else is not a truth value
            codecs::reject(value, "a boolean");
        }

        // write it, in the spelling postgres itself uses
        static inline auto encode(bool value) -> argument_t { return value ? "t" : "f"; }
    };

    // every whole number, in one stroke; spelling out {int64_t} and {long} separately would be
    // a redefinition on the platforms where they are the same type, and leaving either out
    // would surprise a caller on the platforms where they are not
    template <typename valueT>
    struct Codec<
        valueT, std::enable_if_t<std::is_integral_v<valueT> && !std::is_same_v<valueT, bool>>> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // read it
        static inline auto decode(view_t value) -> valueT
        {
            return codecs::whole<valueT>(value, "a whole number");
        }
        // write it
        static inline auto encode(valueT value) -> argument_t { return std::to_string(value); }
    };

    // every real number, likewise
    template <typename valueT>
    struct Codec<valueT, std::enable_if_t<std::is_floating_point_v<valueT>>> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // read it
        static inline auto decode(view_t value) -> valueT
        {
            return codecs::real<valueT>(value, "a real number");
        }
        // write it, with enough digits to survive the round trip
        static inline auto encode(valueT value) -> argument_t { return codecs::render(value); }
    };

    // a value that may be absent; this is how a caller spells {NULL}, which is a thing no
    // string can say and no number can mean
    template <typename valueT>
    struct Codec<std::optional<valueT>> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // a value that arrived is a value that is there
        static inline auto decode(view_t value) -> std::optional<valueT>
        {
            return std::optional<valueT>(postgres::decode<valueT>(value));
        }
        // and an absent one becomes the {NULL} that {argument_t} spells the same way
        static inline auto encode(const std::optional<valueT> & value) -> argument_t
        {
            // nothing to send
            if (!value.has_value()) {
                return argument_t();
            }
            // or the value it holds
            return postgres::encode(*value);
        }
    };

    // raw octets, as they live in a {bytea} column
    template <>
    struct Codec<bytes_t> {
        // types
    public:
        // me
        using self_type = Codec;

        // metamethods
    public:
        // the full set, so the copy and move behavior is never left to inference
        Codec() = default;
        Codec(const Codec &) = default;
        Codec(Codec &&) noexcept = default;
        Codec & operator=(const Codec &) = default;
        Codec & operator=(Codec &&) noexcept = default;
        ~Codec() = default;

        // interface
    public:
        // postgres writes these in one of two escapings, and libpq knows both; it wants a
        // terminated string, and it hands back a buffer that only it may free
        static inline auto decode(view_t value) -> bytes_t
        {
            // terminate the text
            const string_t text(value);
            // room for the length of the answer
            std::size_t length = 0;
            // undo whichever escaping the server chose
            unsigned char * octets =
                PQunescapeBytea(reinterpret_cast<const unsigned char *>(text.c_str()), &length);
            // a null answer means the text was not an escaped byte string, or libpq ran out of
            // memory; either way there is nothing to hand back
            if (octets == nullptr) {
                codecs::reject(value, "an octet string");
            }
            // copy the octets into storage the caller owns
            bytes_t bytes(
                reinterpret_cast<std::byte *>(octets),
                reinterpret_cast<std::byte *>(octets) + length);
            // give libpq its buffer back
            PQfreemem(octets);
            // and hand off the copy
            return bytes;
        }

        // going the other way, use the hex escaping, which every server since 9.0 understands
        // and which costs half of what the historical one does
        static inline auto encode(const bytes_t & value) -> argument_t
        {
            // the digits, in the order postgres reads them
            static constexpr char digits[] = "0123456789abcdef";
            // room for the marker and two characters per octet
            string_t text;
            text.reserve(2 + 2 * value.size());
            // the marker that says which escaping this is
            text += "\\x";
            // and then each octet, high nibble first
            for (const std::byte octet : value) {
                const auto number = std::to_integer<unsigned char>(octet);
                text += digits[number >> 4];
                text += digits[number & 0x0f];
            }
            // hand it off
            return text;
        }
    };
} // namespace pyre::postgres


// the free functions that dispatch to the recipes above
// turn the text in {value} into a {valueT}
template <typename valueT>
auto
pyre::postgres::decode(view_t value) -> valueT
{
    // ask the recipe for this type; a type with no recipe is an incomplete {Codec}, and the
    // compiler says so in those words
    return Codec<valueT>::decode(value);
}


// turn {value} into the text postgres expects
template <typename valueT>
auto
pyre::postgres::encode(const valueT & value) -> argument_t
{
    // strip the reference, the constness and, for a string literal, the array bound, so that
    // the recipe is found under the name a caller would have written
    return Codec<std::decay_t<valueT>>::encode(value);
}


// end of file
