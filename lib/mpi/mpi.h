// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_mpi_h)
#define pyre_mpi_h

#include <mpi.h>

#include "mpi/Error.h"
#include "mpi/Group.h"
#include "mpi/Communicator.h"

namespace pyre {
    namespace mpi {
        typedef Error error_t;
        typedef Communicator communicator_t;
        typedef Group group_t;
    }
}

#endif


// end of file
