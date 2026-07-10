// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


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

    // text, which goes as it is
    if (py::isinstance<py::str>(value)) {
        return value.cast<string_t>();
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
    return py::str(value).cast<string_t>();
}


// turn the value of {field} into a python object
auto
pyre::postgres::py::pythonize(const Field & field) -> py::object
{
    // a value the server did not send becomes {None}. this is what the database api asks for,
    // and what the sqlite back end has always done; the bindings this package replaces handed
    // back {pyre.db.null} instead, which is a fragment of sql and not a value at all
    if (field.isNull()) {
        return py::none();
    }

    // everything else arrives as the text the server's output function produced
    const auto text = field.bytes();
    // which becomes a python string; the server tells us it is encoded the way the session
    // negotiated, and that is very nearly always utf-8
    return py::str(text.data(), text.size());
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
