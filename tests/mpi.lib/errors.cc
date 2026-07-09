// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>
// other packages
#include <cassert>
#include <string>
// grab the mpi objects
#include <pyre/mpi.h>


// exercise the exception hierarchy: an mpi status code must arrive carrying the description
// mpi itself supplies, and the whole hierarchy must be catchable through its bases
int
main()
{
    // bring mpi up, so that mpi is able to describe its own error codes
    pyre::mpi::initialize();

    // push down a scope so our handles die before mpi does
    {
        // a successful status raises nothing at all
        pyre::mpi::check(MPI_SUCCESS);

        // any other status raises
        bool raised = false;
        // so hand {check} a code that names a real failure
        try {
            // this must throw
            pyre::mpi::check(MPI_ERR_COMM);
        }
        // catch the most derived type
        catch (const pyre::mpi::MPIError & error) {
            // note that we got here
            raised = true;
            // the error carries the code we handed it
            assert(error.code() == MPI_ERR_COMM);
            // it belongs to the error class mpi assigns that code
            assert(error.category() == MPI_ERR_COMM);
            // and it explains itself, rather than leaving the caller with a bare number
            assert(!error.description().empty());
            // through the {std::exception} face as well
            assert(std::string(error.what()) == error.description());
        }
        // check that it threw
        assert(raised);

        // the same error is catchable as the package's base error
        raised = false;
        // so throw it again
        try {
            pyre::mpi::check(MPI_ERR_RANK);
        }
        // and catch the base
        catch (const pyre::mpi::Error & error) {
            raised = true;
            // which still explains itself
            assert(!error.description().empty());
        }
        // check that it threw
        assert(raised);

        // and as a plain {std::exception}, which is what lets the bindings above us translate
        // every failure into a python exception rather than calling {std::terminate}
        raised = false;
        // so throw it once more
        try {
            pyre::mpi::check(MPI_ERR_TAG);
        }
        // and catch the standard base
        catch (const std::exception & error) {
            raised = true;
            // which still explains itself
            assert(std::string(error.what()).size() > 0);
        }
        // check that it threw
        assert(raised);

        // a shape error is a package error, but not an mpi one
        raised = false;
        // so provoke one
        try {
            // by asking for a grid whose axes do not all say whether they wrap
            pyre::mpi::world().cartesian({ 2, 2 }, { 0 }, 0);
        }
        // it is not an {MPIError}
        catch (const pyre::mpi::MPIError &) {
            // so getting here would be wrong
            assert(false);
        }
        // but it is an {Error}
        catch (const pyre::mpi::Error & error) {
            raised = true;
            // that explains which rule was broken
            assert(!error.description().empty());
        }
        // check that it threw
        assert(raised);
    }

    // take mpi down
    pyre::mpi::finalize();

    // once mpi is down, an error can no longer ask it for a description, and must say so
    // rather than call into a runtime that is not there
    auto orphan = pyre::mpi::MPIError(MPI_ERR_COMM);
    // it still knows the code it was handed
    assert(orphan.code() == MPI_ERR_COMM);
    // and it still explains itself, in the only terms left to it
    assert(!orphan.description().empty());

    // all done
    return 0;
}


// end of file
