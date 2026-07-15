// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the base of everything {pyre::mpi} throws
class pyre::mpi::Error : public std::exception {
    // types
public:
    // me
    using self_type = Error;
    // my superclass
    using super_type = std::exception;
    using string_type = string_t;

    // metamethods
public:
    // build an error that carries the given human readable {description}
    explicit inline Error(string_type description);
    // the full set, so the copy and move behavior is never left to inference
    inline Error(const Error &) = default;
    inline Error(Error &&) noexcept = default;
    inline Error & operator=(const Error &) = default;
    inline Error & operator=(Error &&) noexcept = default;
    inline ~Error() override = default;

    // interface
public:
    // what went wrong, as a sentence
    inline auto description() const -> const string_type &;
    // the same explanation, through the {std::exception} face
    inline auto what() const noexcept -> const char * override;

    // data
private:
    // the explanation i hand to whoever catches me
    string_type _description;
};


// an mpi call that returned something other than {MPI_SUCCESS}
class pyre::mpi::MPIError : public pyre::mpi::Error {
    // types
public:
    // mpi reports failures as opaque integers
    using code_type = int;

    // metamethods
public:
    // adopt the status code returned by a failed mpi call
    explicit inline MPIError(code_type code);
    // the full set
    inline MPIError(const MPIError &) = default;
    inline MPIError(MPIError &&) noexcept = default;
    inline MPIError & operator=(const MPIError &) = default;
    inline MPIError & operator=(MPIError &&) noexcept = default;
    inline ~MPIError() override = default;

    // interface
public:
    // the raw status code
    inline auto code() const -> code_type;
    // the error class it belongs to, which is portable across mpi implementations
    inline auto category() const -> code_type;

    // implementation details
private:
    // ask mpi to render {code} as text, taking care not to call into a runtime that is down
    static inline auto _describe(code_type code) -> string_type;
    // ask mpi which error class {code} belongs to
    static inline auto _classify(code_type code) -> code_type;

    // data
private:
    // the status code the failed call returned
    code_type _code;
    // the portable error class it belongs to
    code_type _category;
};


// an argument whose shape does not match what the call requires
class pyre::mpi::ShapeError : public pyre::mpi::Error {
    // metamethods
public:
    // explain which shape rule was violated
    explicit inline ShapeError(string_type description);
    // the full set
    inline ShapeError(const ShapeError &) = default;
    inline ShapeError(ShapeError &&) noexcept = default;
    inline ShapeError & operator=(const ShapeError &) = default;
    inline ShapeError & operator=(ShapeError &&) noexcept = default;
    inline ~ShapeError() override = default;
};


// get the inline definitions
#include "Error.icc"


// end of file
