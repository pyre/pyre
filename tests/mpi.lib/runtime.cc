// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>
// other packages
#include <cassert>
// grab the mpi objects
#include <pyre/mpi.h>


// exercise the runtime face: bringing mpi up and down, and the communicators it predefines
int
main()
{
    // before we do anything, mpi is down
    assert(!pyre::mpi::initialized());
    // and it has certainly not been taken down
    assert(!pyre::mpi::finalized());

    // bring it up, asking for the weakest thread guarantee, which every implementation grants
    auto granted = pyre::mpi::initialize(pyre::mpi::Thread::single);
    // mpi must grant at least what we asked for; my levels are ordered by increasing freedom,
    // so this comparison answers the question a caller actually has
    assert(granted >= pyre::mpi::Thread::single);
    // and now it is up
    assert(pyre::mpi::initialized());

    // asking again must be harmless, and must report the same level
    assert(pyre::mpi::initialize(pyre::mpi::Thread::single) == granted);

    // whatever level we were granted, it is one of the four the standard names
    assert(pyre::mpi::threadSupport(pyre::mpi::threadLevel(granted)) == granted);

    // push down a scope so our handles die before mpi does
    {
        // the communicator that holds the whole job
        auto world = pyre::mpi::world();
        // it names something
        assert(static_cast<bool>(world));
        // the communicator that holds me alone
        auto self = pyre::mpi::self();
        // has exactly one process
        assert(self.size() == 1);
        // in which i am the only rank
        assert(self.rank() == 0);

        // the communicator that holds nobody
        auto nothing = pyre::mpi::null();
        // names nothing
        assert(nothing.isNull());
        // and says so when asked in a boolean context
        assert(!nothing);

        // the clock runs forward
        double before = pyre::mpi::wtime();
        // and reports a positive resolution
        assert(pyre::mpi::wtick() > 0);
        // and never runs backwards
        assert(pyre::mpi::wtime() >= before);

        // every process knows where it lives
        assert(!pyre::mpi::processorName().empty());
    }

    // take mpi down
    pyre::mpi::finalize();
    // and now it is down
    assert(pyre::mpi::finalized());

    // taking it down twice must be harmless, since we decline rather than call into mpi
    pyre::mpi::finalize();

    // all done
    return 0;
}


// end of file
