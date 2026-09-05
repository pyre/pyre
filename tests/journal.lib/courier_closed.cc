// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <unistd.h>


// alias the types
using courier_t = pyre::journal::courier_t;
using chronicler_t = pyre::journal::chronicler_t;
using info_t = pyre::journal::info_t;


// a far end that goes away silences the courier without taking the process down
int
main()
{
    // make a pipe
    int pipes[2];
    assert(::pipe(pipes) == 0);
    // make a courier on its write end and install it
    auto courier = std::make_shared<courier_t>(pipes[1]);
    chronicler_t::device(courier);

    // with the far end present, an entry goes out
    info_t channel("test.courier.closed");
    channel << "present" << pyre::journal::endl;
    assert(courier->shipped() == 1);
    assert(!courier->dead());

    // take the far end away
    ::close(pipes[0]);
    // logging must not raise a signal or throw
    channel << "absent" << pyre::journal::endl;
    // the courier noticed
    assert(courier->dead());
    // the entry was stamped but not shipped
    assert(courier->seq() == 2);
    assert(courier->shipped() == 1);
    // and from now on nothing is even stamped
    channel << "silence" << pyre::journal::endl;
    assert(courier->seq() == 2);

    // closing a dead courier is harmless
    courier->close();
    // and so is closing it again
    courier->close();

    // all done
    return 0;
}


// end of file
