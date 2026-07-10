// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test; nothing else is needed to use it, and in particular nothing python
#include <pyre/postgres.h>
// and the journal, so the test may say something when it goes wrong
#include <pyre/journal.h>


// verify that the package is there, that its header is self contained, and that the names it
// publishes are the ones its clients are told to expect
int
main()
{
    // the exception hierarchy
    static_assert(std::is_base_of_v<std::exception, pyre::postgres::exception_t>);
    static_assert(std::is_base_of_v<pyre::postgres::exception_t, pyre::postgres::error_t>);
    // a warning is not an error; the database api puts the two side by side, and a {catch} that
    // hunts for a failure must not sweep up a remark
    static_assert(!std::is_base_of_v<pyre::postgres::error_t, pyre::postgres::warning_t>);
    static_assert(std::is_base_of_v<pyre::postgres::exception_t, pyre::postgres::warning_t>);
    // and the five that a caller branches on
    static_assert(std::is_base_of_v<pyre::postgres::error_t, pyre::postgres::databaseError_t>);
    static_assert(
        std::is_base_of_v<pyre::postgres::databaseError_t, pyre::postgres::dataError_t>);
    static_assert(
        std::is_base_of_v<pyre::postgres::databaseError_t, pyre::postgres::integrityError_t>);
    static_assert(
        std::is_base_of_v<pyre::postgres::databaseError_t, pyre::postgres::operationalError_t>);
    static_assert(
        std::is_base_of_v<pyre::postgres::databaseError_t, pyre::postgres::programmingError_t>);

    // a connection is worth copying and worth moving, and a transaction is worth neither
    static_assert(std::is_copy_constructible_v<pyre::postgres::connection_t>);
    static_assert(std::is_move_constructible_v<pyre::postgres::connection_t>);
    static_assert(!std::is_copy_constructible_v<pyre::postgres::transaction_t>);
    static_assert(std::is_move_constructible_v<pyre::postgres::transaction_t>);

    // a result and the views into it are all cheap to copy
    static_assert(std::is_copy_constructible_v<pyre::postgres::result_t>);
    static_assert(std::is_copy_constructible_v<pyre::postgres::row_t>);
    static_assert(std::is_copy_constructible_v<pyre::postgres::field_t>);

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.postgres.sanity");
    // and say something
    channel << "the postgres bindings are there" << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
