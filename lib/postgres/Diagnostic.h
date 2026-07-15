// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// everything the server has to say about a statement that did not work out
//
// libpq keeps this report inside the {PGresult}, and hands out borrowed pointers into it. a
// diagnostic that only pointed there would die with the result it came from, and an exception
// that carried it would be a dangling reference by the time anybody caught it. so each field
// gets copied out, once, as the diagnostic is built
class pyre::postgres::Diagnostic {
    // types
public:
    // me
    using self_type = Diagnostic;
    using string_type = string_t;

    // metamethods
public:
    // harvest everything {result} knows about the failure of {command}
    explicit inline Diagnostic(const PGresult * result, string_type command = "");
    // build a report out of a bare {message}; a session that never came up has no result to
    // explain itself with, and neither does one whose socket died mid-statement
    explicit inline Diagnostic(string_type message, string_type command = "");
    // the full set, so the copy and move behavior is never left to inference
    inline Diagnostic(const Diagnostic &) = default;
    inline Diagnostic(Diagnostic &&) noexcept = default;
    inline Diagnostic & operator=(const Diagnostic &) = default;
    inline Diagnostic & operator=(Diagnostic &&) noexcept = default;
    inline ~Diagnostic() = default;

    // the statement, and the server's verdict on it
public:
    // the sql we sent, if anybody bothered to tell us
    inline auto command() const -> const string_type &;
    // how bad the server thinks this is; one of ERROR, FATAL, PANIC, WARNING, NOTICE, DEBUG,
    // INFO or LOG, and always in english, whatever language the server was configured to speak
    inline auto severity() const -> const string_type &;
    // the five character code that names the condition. this is the only part of a complaint
    // that is portable, and hence the only part worth branching on
    inline auto sqlstate() const -> const string_type &;
    // the first two characters of the SQLSTATE, which name the family the condition belongs to
    inline auto category() const -> view_t;
    // the one line explanation, written for a human
    inline auto message() const -> const string_type &;

    // the optional elaborations; each is empty when the server chose not to supply it
public:
    // a second paragraph, with the particulars
    inline auto detail() const -> const string_type &;
    // the server's suggestion for how to resolve the problem, when it offered one
    inline auto hint() const -> const string_type &;
    // where in the sql the server was when it gave up; a one based character index into
    // {command}, or zero when it did not say
    inline auto position() const -> int;
    // the same, but into a statement the server generated for itself
    inline auto internalPosition() const -> int;
    // the statement the server generated for itself
    inline auto internalQuery() const -> const string_type &;
    // the call stack, in the server's terms: a pl/pgsql function, a trigger, a cursor
    inline auto context() const -> const string_type &;

    // the object the complaint is about; populated for the constraint violations, and for
    // little else. these are what let a caller tell one unique index from another without
    // parsing english
public:
    inline auto schema() const -> const string_type &;
    inline auto table() const -> const string_type &;
    inline auto column() const -> const string_type &;
    inline auto datatype() const -> const string_type &;
    inline auto constraint() const -> const string_type &;

    // interface
public:
    // a one line rendering, suitable as the {what} of an exception
    inline auto describe() const -> string_type;

    // implementation details
private:
    // copy the field named by {code} out of {result}; libpq hands back a null pointer for the
    // ones the server chose not to send, and we render those as the empty string
    static inline auto _field(const PGresult * result, int code) -> string_type;
    // the same, for the two fields the server sends as decimal text
    static inline auto _index(const PGresult * result, int code) -> int;

    // data
private:
    // the sql that provoked all this
    string_type _command;
    // the verdict
    string_type _severity;
    string_type _sqlstate;
    string_type _message;
    // the elaborations
    string_type _detail;
    string_type _hint;
    string_type _internalQuery;
    string_type _context;
    int _position;
    int _internalPosition;
    // the object at fault
    string_type _schema;
    string_type _table;
    string_type _column;
    string_type _datatype;
    string_type _constraint;
};


// get the inline definitions
#include "Diagnostic.icc"


// end of file
