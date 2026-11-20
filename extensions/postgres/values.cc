// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the translation of the text the server sends into python values
//
// every value arrives as the text its type's output function produced. the session pins the
// settings that shape that text when it opens, so a date is always written the ISO way; what is
// left is to read each type's text into the python value that holds the same thing, and to say so
// when python has no value that does
namespace pyre::postgres::py::values {
    // the python modules whose types hold what the server sends
    struct Modules {
        // exact numbers
        py::object decimal;
        // the calendar and the clock
        py::object date;
        py::object time;
        py::object datetime;
        py::object timedelta;
        py::object timezone;
        // json documents
        py::object loads;
        // universally unique identifiers
        py::object uuid;
    };

    // find the modules once, the first time a value needs them
    inline auto modules() -> const Modules &
    {
        // the store, which keeps them for the life of the interpreter
        PYBIND11_CONSTINIT static py::gil_safe_call_once_and_store<Modules> store;
        // fill it on the first call
        return store
            .call_once_and_store_result([]() -> Modules {
                // the calendar and the clock all come from the same module
                const auto datetime = py::module::import("datetime");
                // collect the types
                return Modules {
                    py::module::import("decimal").attr("Decimal"),
                    datetime.attr("date"),
                    datetime.attr("time"),
                    datetime.attr("datetime"),
                    datetime.attr("timedelta"),
                    datetime.attr("timezone"),
                    py::module::import("json").attr("loads"),
                    py::module::import("uuid").attr("UUID"),
                };
            })
            .get_stored();
    }

    // complain that {text}, the value of {column}, is not a {what} python can hold
    [[noreturn]] inline auto reject(view_t column, view_t text, view_t what) -> void
    {
        // say which column, what it held, and what that was supposed to be
        string_t message = "the value '";
        message += text;
        message += "' of column '";
        message += column;
        message += "' is not ";
        message += what;
        message += " that python can represent";
        // a value that does not fit its type is a data exception, as postgres would call it
        throw DataError(Diagnostic(std::move(message)));
    }

    // read exactly {width} digits off the front of {text}, or report that {whole} is not a {what}
    inline auto digits(view_t & text, std::size_t width, view_t column, view_t whole, view_t what)
        -> int
    {
        // there must be enough of them
        if (text.size() < width) {
            reject(column, whole, what);
        }
        // room for the answer
        int number = 0;
        // read them
        const auto outcome = std::from_chars(text.data(), text.data() + width, number);
        // all of them, and nothing but them
        if (outcome.ec != std::errc() || outcome.ptr != text.data() + width) {
            reject(column, whole, what);
        }
        // step over them
        text.remove_prefix(width);
        // and hand off the number
        return number;
    }

    // step over {mark} at the front of {text}, or report that {whole} is not a {what}
    inline auto expect(view_t & text, char mark, view_t column, view_t whole, view_t what) -> void
    {
        // the mark must be there
        if (text.empty() || text.front() != mark) {
            reject(column, whole, what);
        }
        // step over it
        text.remove_prefix(1);
        // all done
        return;
    }

    // the calendar date, as python wants its parts
    struct Calendar {
        int year;
        int month;
        int day;
    };

    // read a calendar date, {YYYY-MM-DD}, off the front of {text}
    inline auto calendar(view_t & text, view_t column, view_t whole, view_t what) -> Calendar
    {
        // the year has exactly four digits in every year python can hold; a fifth digit is a
        // year past 9999, and the words 'infinity' and '-infinity' have none at all
        const auto year = digits(text, 4, column, whole, what);
        expect(text, '-', column, whole, what);
        // the month
        const auto month = digits(text, 2, column, whole, what);
        expect(text, '-', column, whole, what);
        // and the day
        const auto day = digits(text, 2, column, whole, what);
        // assemble the parts; a year before the common era carries a suffix that the caller
        // finds left over, and refuses, since python has no such years
        return Calendar { year, month, day };
    }

    // the time of day, as python wants its parts
    struct Clock {
        int hour;
        int minute;
        int second;
        int microsecond;
    };

    // read a time of day, {HH:MM:SS[.ffffff]}, off the front of {text}
    inline auto clock(view_t & text, view_t column, view_t whole, view_t what) -> Clock
    {
        // the hour
        const auto hour = digits(text, 2, column, whole, what);
        // postgres allows '24:00:00', the end of a day, which python has no way to say
        if (hour > 23) {
            reject(column, whole, what);
        }
        expect(text, ':', column, whole, what);
        // the minute
        const auto minute = digits(text, 2, column, whole, what);
        expect(text, ':', column, whole, what);
        // the second
        const auto second = digits(text, 2, column, whole, what);
        // and the fraction of a second, which the server writes only when there is one, with
        // as many digits as it needs, and never more than six
        auto microsecond = 0;
        // if it is there
        if (!text.empty() && text.front() == '.') {
            // step over the point
            text.remove_prefix(1);
            // count the digits
            std::size_t width = 0;
            while (width < text.size() && text[width] >= '0' && text[width] <= '9') {
                ++width;
            }
            // there must be some, and no more than python can hold
            if (width == 0 || width > 6) {
                reject(column, whole, what);
            }
            // read them
            microsecond = digits(text, width, column, whole, what);
            // and scale them to microseconds
            for (auto missing = width; missing < 6; ++missing) {
                microsecond *= 10;
            }
        }
        // assemble the parts
        return Clock { hour, minute, second, microsecond };
    }

    // read an offset from UTC, {+HH[:MM[:SS]]}, off the front of {text}
    inline auto offset(view_t & text, view_t column, view_t whole, view_t what) -> py::object
    {
        // the sign must be there
        if (text.empty() || (text.front() != '+' && text.front() != '-')) {
            reject(column, whole, what);
        }
        // remember which way it goes
        const auto sign = text.front() == '-' ? -1 : 1;
        // and step over it
        text.remove_prefix(1);
        // the hours are always there
        auto seconds = 3600 * digits(text, 2, column, whole, what);
        // the minutes, when there are any
        if (!text.empty() && text.front() == ':') {
            // step over the colon
            text.remove_prefix(1);
            // and add them in
            seconds += 60 * digits(text, 2, column, whole, what);
        }
        // and the seconds, which only the offsets of local mean time have
        if (!text.empty() && text.front() == ':') {
            // step over the colon
            text.remove_prefix(1);
            // and add them in
            seconds += digits(text, 2, column, whole, what);
        }
        // build the zone
        const auto & python = modules();
        return python.timezone(python.timedelta("seconds"_a = sign * seconds));
    }

    // make sure the whole of the text was read
    inline auto done(view_t text, view_t column, view_t whole, view_t what) -> void
    {
        // anything left over means this was not the value its type said it was
        if (!text.empty()) {
            reject(column, whole, what);
        }
        // all done
        return;
    }

    // read a date
    inline auto date(view_t text, view_t column) -> py::object
    {
        // what this is
        constexpr view_t what = "a date";
        // a copy of the text to read from
        auto cursor = text;
        // read the date
        const auto parts = calendar(cursor, column, text, what);
        // and make sure that was all of it
        done(cursor, column, text, what);
        // build the date
        return modules().date(parts.year, parts.month, parts.day);
    }

    // read a time of day, with an offset from UTC when {zoned}
    inline auto time(view_t text, view_t column, bool zoned) -> py::object
    {
        // what this is
        constexpr view_t what = "a time of day";
        // a copy of the text to read from
        auto cursor = text;
        // read the clock
        const auto parts = clock(cursor, column, text, what);
        // and the zone, if there is one
        auto zone = zoned ? offset(cursor, column, text, what) : py::none();
        // make sure that was all of it
        done(cursor, column, text, what);
        // and build the time
        return modules().time(
            parts.hour, parts.minute, parts.second, parts.microsecond, "tzinfo"_a = zone);
    }

    // read a moment, with an offset from UTC when {zoned}
    inline auto timestamp(view_t text, view_t column, bool zoned) -> py::object
    {
        // what this is
        constexpr view_t what = "a date and time";
        // a copy of the text to read from
        auto cursor = text;
        // the date
        const auto day = calendar(cursor, column, text, what);
        // the separator
        expect(cursor, ' ', column, text, what);
        // the clock
        const auto parts = clock(cursor, column, text, what);
        // the zone, if there is one
        auto zone = zoned ? offset(cursor, column, text, what) : py::none();
        // and nothing else, in particular no era
        done(cursor, column, text, what);
        // build the moment
        return modules().datetime(
            day.year, day.month, day.day, parts.hour, parts.minute, parts.second, parts.microsecond,
            "tzinfo"_a = zone);
    }

    // the decoder of every type, declared here so that arrays can decode their entries
    inline auto decode(oid_t type, view_t text, view_t column) -> py::object;

    // read one array, {{a,b,...}}, off the front of {text}, decoding its entries as {element}
    inline auto list(view_t & text, oid_t element, view_t column, view_t whole) -> py::list
    {
        // what this is
        constexpr view_t what = "an array";
        // the opening brace
        expect(text, '{', column, whole, what);
        // room for the entries
        py::list entries;
        // an empty array is just its braces
        if (!text.empty() && text.front() == '}') {
            // step over the closing brace
            text.remove_prefix(1);
            // and hand off the empty list
            return entries;
        }
        // otherwise, read the entries
        while (true) {
            // an entry that is itself an array is one dimension further in
            if (!text.empty() && text.front() == '{') {
                entries.append(list(text, element, column, whole));
            }
            // an entry in quotes is text with its quotes and backslashes escaped
            else if (!text.empty() && text.front() == '"') {
                // step over the opening quote
                text.remove_prefix(1);
                // room for the entry
                string_t entry;
                // copy it, undoing the escapes, up to the closing quote
                while (!text.empty() && text.front() != '"') {
                    // a backslash means the next character is part of the entry
                    if (text.front() == '\\') {
                        text.remove_prefix(1);
                    }
                    // the text must not end in the middle of an entry
                    if (text.empty()) {
                        reject(column, whole, what);
                    }
                    // take the character
                    entry += text.front();
                    text.remove_prefix(1);
                }
                // step over the closing quote
                expect(text, '"', column, whole, what);
                // and decode the entry; a quoted entry is never {NULL}
                entries.append(decode(element, entry, column));
            }
            // and anything else runs up to the next comma or closing brace
            else {
                // find the end of it
                const auto end = text.find_first_of(",}");
                // there must be one
                if (end == view_t::npos || end == 0) {
                    reject(column, whole, what);
                }
                // the entry
                const auto entry = text.substr(0, end);
                // step over it
                text.remove_prefix(end);
                // the server writes a missing entry as an unquoted {NULL}
                if (entry == "NULL") {
                    entries.append(py::none());
                } else {
                    entries.append(decode(element, entry, column));
                }
            }
            // after each entry comes either the end of the array
            if (!text.empty() && text.front() == '}') {
                // step over it
                text.remove_prefix(1);
                // and hand off the entries
                return entries;
            }
            // or the comma before the next entry
            expect(text, ',', column, whole, what);
        }
    }

    // read an array whose entries are of type {element}
    inline auto array(view_t text, oid_t element, view_t column) -> py::object
    {
        // a copy of the text to read from
        auto cursor = text;
        // an array that does not start at one says where its dimensions start and end, as in
        // '[0:2]={a,b,c}'; python lists start at zero, whatever the bounds, so step over them
        if (!cursor.empty() && cursor.front() == '[') {
            // find the end of the bounds
            const auto equals = cursor.find('=');
            // there must be one
            if (equals == view_t::npos) {
                reject(column, text, "an array");
            }
            // and step over it
            cursor.remove_prefix(equals + 1);
        }
        // read the array
        auto value = list(cursor, element, column, text);
        // and make sure that was all of it
        done(cursor, column, text, "an array");
        // hand it off
        return value;
    }

    // turn {text}, the value of {column}, into the python value of its {type}
    inline auto decode(oid_t type, view_t text, view_t column) -> py::object
    {
        // go through the types that have a python value of their own
        switch (type) {
            // truth
            case types::boolean:
                return py::bool_(postgres::decode<bool>(text));
            // whole numbers of every width
            case types::smallint:
            case types::integer:
            case types::bigint:
                return py::int_(postgres::decode<std::int64_t>(text));
            // the identifiers of the catalog's rows, which are unsigned
            case types::oid:
                return py::int_(postgres::decode<oid_t>(text));
            // real numbers of every width
            case types::real:
            case types::doublePrecision:
                return py::float_(postgres::decode<double>(text));
            // exact numbers, including the 'NaN' and 'Infinity' that python reads too
            case types::numeric:
                return modules().decimal(py::str(text.data(), text.size()));
            // raw octets
            case types::bytea: {
                // undo the escaping
                const auto octets = postgres::decode<bytes_t>(text);
                // and copy them into python
                return py::bytes(reinterpret_cast<const char *>(octets.data()), octets.size());
            }
            // json documents, in either form
            case types::json:
            case types::jsonb:
                return modules().loads(py::str(text.data(), text.size()));
            // universally unique identifiers
            case types::uuid:
                return modules().uuid(py::str(text.data(), text.size()));
            // the calendar
            case types::date:
                return date(text, column);
            // the clock, with or without a zone
            case types::time:
                return time(text, column, false);
            case types::timeWithTimeZone:
                return time(text, column, true);
            // moments, with or without a zone
            case types::timestamp:
                return timestamp(text, column, false);
            case types::timestampWithTimeZone:
                return timestamp(text, column, true);
        }
        // the arrays of the types above
        if (const auto element = types::element(type); element != invalidOid) {
            return array(text, element, column);
        }
        // and everything else is the text the server wrote, which is also what python makes of
        // the server's own strings; the session pinned their encoding to utf-8 when it opened
        return py::str(text.data(), text.size());
    }
} // namespace pyre::postgres::py::values


// turn the value of {field} into a python object
auto
pyre::postgres::py::pythonize(const Field & field) -> py::object
{
    // a value the server did not send becomes {None}, which is what the database api asks for,
    // and what the sqlite back end does; {pyre.db.null} is a fragment of sql, not a value
    if (field.isNull()) {
        return py::none();
    }

    // everything else becomes the python value of the field's type
    return values::decode(field.type(), field.bytes(), field.name());
}


// end of file
