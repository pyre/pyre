// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages and the type aliases that shape the {pyre::h5} namespace
#include "../external.h"


// the pyre-owned hdf5 property lists
namespace pyre::h5::properties {
    // the generic base
    class List;
    // dataset access, creation, and transfer
    class DAPL;
    class DCPL;
    class DXPL;
    // file access and creation
    class FAPL;
    class FCPL;
    // link access and creation
    class LAPL;
    class LCPL;
} // namespace pyre::h5::properties


// end of file
