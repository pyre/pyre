// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Informational.h"


// the one definition of the channel index; the declaration in the header explains why it lives
// in the library rather than in every translation unit that touches the channel; it is built
// the way the generic definition builds it, by asking the channel to initialize it
template <>
pyre::journal::Index pyre::journal::Channel<
    pyre::journal::Informational<pyre::journal::InventoryProxy>,
    pyre::journal::InventoryProxy>::_index =
    pyre::journal::Channel<
        pyre::journal::Informational<pyre::journal::InventoryProxy>,
        pyre::journal::InventoryProxy>::_initializeIndex();


// end of file
