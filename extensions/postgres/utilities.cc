// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the helpers of the renderer
namespace pyre::postgres::py {
    // check that {text} can be the value of a postgres text, which cannot hold a zero byte
    inline auto checkText(const string_t & text) -> const string_t &
    {
        // a zero byte
        if (text.find('\0') != string_t::npos) {
            // has no place in it; refuse before anything is sent, rather than let libpq cut the
            // text short at the zero
            throw DataError(Diagnostic("text cannot hold a zero byte"));
        }
        // the rest is fine as it is
        return text;
    }

    // render {sequence}, a list or a tuple, as the literal of an array: every entry is quoted,
    // with its backslashes and double quotes escaped, a {None} is {NULL}, and an entry that is a
    // sequence itself is a level of the array
    inline auto renderArray(py::handle sequence) -> string_t
    {
        // the literal opens with a brace
        string_t literal = "{";
        // the entries, separated by commas
        bool first = true;
        // go through them
        for (const auto & entry : sequence) {
            // every entry after the first
            if (!first) {
                // is set apart from the one before it
                literal += ",";
            }
            // and none is the first any more
            first = false;
            // a missing entry
            if (entry.is_none()) {
                // is spelled as such
                literal += "NULL";
                // and that is all
                continue;
            }
            // an entry that is a sequence itself
            if (py::isinstance<py::list>(entry) || py::isinstance<py::tuple>(entry)) {
                // is a level of the array
                literal += renderArray(entry);
                // and that is all
                continue;
            }
            // any other entry is rendered as an argument would be
            const auto text = *render(entry);
            // and quoted
            literal += "\"";
            // with its backslashes and double quotes escaped
            for (const auto character : text) {
                // each of which gets a backslash in front of it
                if (character == '\\' || character == '"') {
                    literal += '\\';
                }
                // before the character itself
                literal += character;
            }
            // close the quote
            literal += "\"";
        }
        // and the literal closes with a brace
        literal += "}";
        // all done
        return literal;
    }
} // namespace pyre::postgres::py


// turn a python object into the text that fills one placeholder of a statement
//
// this is the python end of the {Codec} machinery. it cannot be the c++ one, because the type of
// a python value is not known until it arrives; so this walks the handful of types postgres and
// python already agree about, and falls back on whatever the object says it is
auto
pyre::postgres::py::render(py::handle value) -> argument_t
{
    // nothing at all; this is how a caller spells {NULL}, and there is no other way. note in
    // particular that {pyre.db.null} is not a value but a fragment of sql, meant for the
    // statement rather than for its arguments, and it has no business here
    if (value.is_none()) {
        return argument_t();
    }

    // truth, which must be sorted out before whole numbers, since python makes {bool} a
    // subclass of {int} and would otherwise render {False} as {0}
    if (py::isinstance<py::bool_>(value)) {
        // in the spelling postgres itself uses
        return value.cast<bool>() ? "t" : "f";
    }

    // whole numbers, which python carries to arbitrary precision. rendering these through any
    // fixed width c++ integer would raise on the way in, and postgres has a {numeric} that can
    // hold every one of them; so let python spell it, which it does exactly
    if (py::isinstance<py::int_>(value)) {
        return py::str(value).cast<string_t>();
    }

    // real numbers, which go through the codec that knows how many digits a round trip needs,
    // and that knows postgres spells infinity differently than c does
    if (py::isinstance<py::float_>(value)) {
        return postgres::encode(value.cast<double>());
    }

    // text, which goes as it is, as long as postgres can hold it
    if (py::isinstance<py::str>(value)) {
        return checkText(value.cast<string_t>());
    }

    // lists and tuples, which become arrays
    if (py::isinstance<py::list>(value) || py::isinstance<py::tuple>(value)) {
        return renderArray(value);
    }

    // dictionaries, which become json documents, in the spelling python's own encoder gives them
    if (py::isinstance<py::dict>(value)) {
        return checkText(py::module_::import("json").attr("dumps")(value).cast<string_t>());
    }

    // the byte buffers other than {bytes}, which go as the octets they hold
    if (py::isinstance<py::bytearray>(value) || py::isinstance<py::memoryview>(value)) {
        return render(py::module_::import("builtins").attr("bytes")(value));
    }

    // raw octets, which go as the hex escaping every server since 9.0 understands
    if (py::isinstance<py::bytes>(value)) {
        // take a look at them
        const auto view = value.cast<std::string_view>();
        // and copy them into the form the codec wants
        const bytes_t octets(
            reinterpret_cast<const std::byte *>(view.data()),
            reinterpret_cast<const std::byte *>(view.data()) + view.size());
        // which knows how to spell them
        return postgres::encode(octets);
    }

    // and everything else, on the strength of its own rendering. this is what carries a
    // {Decimal}, a {date}, a {datetime} and a {UUID} across, and it does so exactly: python
    // spells each of them the way postgres reads it
    return checkText(py::str(value).cast<string_t>());
}


// turn every argument of a call into the text of a statement's placeholders
auto
pyre::postgres::py::arguments(const py::args & args) -> arguments_t
{
    // room for them
    arguments_t rendered;
    rendered.reserve(args.size());
    // render each one
    for (const auto & argument : args) {
        rendered.push_back(render(argument));
    }
    // hand them off
    return rendered;
}


// the loose functions the module publishes
void
pyre::postgres::py::utilities(py::module & m)
{
    // the version of the client library we were built against, as a number: 16.2 is 160002
    m.def(
        // the name
        "version",
        // the implementation
        []() -> int { return PQlibVersion(); },
        // the docstring
        "the version of {libpq} this extension is linked against");

    // the copyright note
    m.def(
        // the name
        "copyright",
        // the implementation
        []() -> string_t { return "postgres: (c) 1998-2026 Michael A.G. Aïvázis"; },
        // the docstring
        "the module copyright string");

    // all done
    return;
}


// end of file
