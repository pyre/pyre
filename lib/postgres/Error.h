// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// every exception carries one of these, so it must be complete before any of them is declared
#include "Diagnostic.h"


// the base of everything {pyre::postgres} throws
//
// the shape of this hierarchy is not ours: it is the one the python database api, in its
// version 2.0, obliges every driver to present. it is a peculiar classification, sorting
// failures by the part of the system that is to blame rather than by what a caller might do
// about them, but it is the one that clients of every other driver already know, and there is
// nothing to be gained by inventing a second
class pyre::postgres::Exception : public std::exception {
    // types
public:
    using string_type = string_t;
    using diagnostic_type = Diagnostic;

    // metamethods
public:
    // adopt the server's report of what went wrong
    explicit inline Exception(diagnostic_type diagnostic);
    // the full set, so the copy and move behavior is never left to inference
    inline Exception(const Exception &) = default;
    inline Exception(Exception &&) noexcept = default;
    inline Exception & operator=(const Exception &) = default;
    inline Exception & operator=(Exception &&) noexcept = default;
    inline ~Exception() override = default;

    // interface
public:
    // everything the server had to say, in full
    inline auto diagnostic() const -> const diagnostic_type &;
    // the one line summary of it
    inline auto description() const -> const string_type &;
    // the same summary, through the {std::exception} face
    inline auto what() const noexcept -> const char * override;

    // data
private:
    // the report i was built from
    diagnostic_type _diagnostic;
    // its one line rendering, computed once at construction so that {what} has something whose
    // lifetime it can promise
    string_type _description;
};


// something the back end wants us to know about, but that did not stop it
//
// note that this does not derive from {Error}: the database api puts the two side by side, so
// that a warning, which is not a failure, is not caught by a {catch} that is looking for one
class pyre::postgres::Warning : public pyre::postgres::Exception {
    // metamethods
public:
    // adopt the server's report
    explicit inline Warning(diagnostic_type diagnostic);
    // the full set
    inline Warning(const Warning &) = default;
    inline Warning(Warning &&) noexcept = default;
    inline Warning & operator=(const Warning &) = default;
    inline Warning & operator=(Warning &&) noexcept = default;
    inline ~Warning() override = default;
};


// the base of everything that did stop the back end
class pyre::postgres::Error : public pyre::postgres::Exception {
    // metamethods
public:
    // adopt the server's report
    explicit inline Error(diagnostic_type diagnostic);
    // the full set
    inline Error(const Error &) = default;
    inline Error(Error &&) noexcept = default;
    inline Error & operator=(const Error &) = default;
    inline Error & operator=(Error &&) noexcept = default;
    inline ~Error() override = default;
};


// a mistake made on this side of the wire, before the back end ever saw the statement
//
// asking a closed connection to run something, or a result for a column it does not have, are
// the two ways to get one of these. the server is not involved, and so has nothing to say: a
// diagnostic built here carries a message we wrote ourselves and no SQLSTATE at all
class pyre::postgres::InterfaceError : public pyre::postgres::Error {
    // metamethods
public:
    // explain, in our own words, what the caller did wrong
    explicit inline InterfaceError(string_type message);
    // or adopt a report somebody else assembled
    explicit inline InterfaceError(diagnostic_type diagnostic);
    // the full set
    inline InterfaceError(const InterfaceError &) = default;
    inline InterfaceError(InterfaceError &&) noexcept = default;
    inline InterfaceError & operator=(const InterfaceError &) = default;
    inline InterfaceError & operator=(InterfaceError &&) noexcept = default;
    inline ~InterfaceError() override = default;
};


// a complaint that came back from the server
class pyre::postgres::DatabaseError : public pyre::postgres::Error {
    // metamethods
public:
    // adopt the server's report
    explicit inline DatabaseError(diagnostic_type diagnostic);
    // the full set
    inline DatabaseError(const DatabaseError &) = default;
    inline DatabaseError(DatabaseError &&) noexcept = default;
    inline DatabaseError & operator=(const DatabaseError &) = default;
    inline DatabaseError & operator=(DatabaseError &&) noexcept = default;
    inline ~DatabaseError() override = default;
};


// the data in the statement was wrong; SQLSTATE class 22
class pyre::postgres::DataError : public pyre::postgres::DatabaseError {
    // metamethods
public:
    explicit inline DataError(diagnostic_type diagnostic);
    inline DataError(const DataError &) = default;
    inline DataError(DataError &&) noexcept = default;
    inline DataError & operator=(const DataError &) = default;
    inline DataError & operator=(DataError &&) noexcept = default;
    inline ~DataError() override = default;
};


// the environment failed us; SQLSTATE classes 08, 53 through 58, and their neighbors
class pyre::postgres::OperationalError : public pyre::postgres::DatabaseError {
    // metamethods
public:
    explicit inline OperationalError(diagnostic_type diagnostic);
    inline OperationalError(const OperationalError &) = default;
    inline OperationalError(OperationalError &&) noexcept = default;
    inline OperationalError & operator=(const OperationalError &) = default;
    inline OperationalError & operator=(OperationalError &&) noexcept = default;
    inline ~OperationalError() override = default;
};


// the statement would have left the database inconsistent; SQLSTATE class 23
class pyre::postgres::IntegrityError : public pyre::postgres::DatabaseError {
    // metamethods
public:
    explicit inline IntegrityError(diagnostic_type diagnostic);
    inline IntegrityError(const IntegrityError &) = default;
    inline IntegrityError(IntegrityError &&) noexcept = default;
    inline IntegrityError & operator=(const IntegrityError &) = default;
    inline IntegrityError & operator=(IntegrityError &&) noexcept = default;
    inline ~IntegrityError() override = default;
};


// the back end found itself in a state it does not believe in; SQLSTATE classes XX, P0, and
// the ones that say a cursor or a transaction is not where the server left it
class pyre::postgres::InternalError : public pyre::postgres::DatabaseError {
    // metamethods
public:
    explicit inline InternalError(diagnostic_type diagnostic);
    inline InternalError(const InternalError &) = default;
    inline InternalError(InternalError &&) noexcept = default;
    inline InternalError & operator=(const InternalError &) = default;
    inline InternalError & operator=(InternalError &&) noexcept = default;
    inline ~InternalError() override = default;
};


// the statement was malformed; SQLSTATE class 42, and the ones that name a thing that is not
// there
class pyre::postgres::ProgrammingError : public pyre::postgres::DatabaseError {
    // metamethods
public:
    explicit inline ProgrammingError(diagnostic_type diagnostic);
    inline ProgrammingError(const ProgrammingError &) = default;
    inline ProgrammingError(ProgrammingError &&) noexcept = default;
    inline ProgrammingError & operator=(const ProgrammingError &) = default;
    inline ProgrammingError & operator=(ProgrammingError &&) noexcept = default;
    inline ~ProgrammingError() override = default;
};


// the statement asked for something this server cannot do; SQLSTATE class 0A
class pyre::postgres::NotSupportedError : public pyre::postgres::DatabaseError {
    // metamethods
public:
    explicit inline NotSupportedError(diagnostic_type diagnostic);
    inline NotSupportedError(const NotSupportedError &) = default;
    inline NotSupportedError(NotSupportedError &&) noexcept = default;
    inline NotSupportedError & operator=(const NotSupportedError &) = default;
    inline NotSupportedError & operator=(NotSupportedError &&) noexcept = default;
    inline ~NotSupportedError() override = default;
};


// get the inline definitions
#include "Error.icc"


// end of file
