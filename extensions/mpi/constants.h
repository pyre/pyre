// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(pyre_extensions_postgres_constants_h)
#define pyre_extensions_postgres_constants_h

// local additions to the namespace
namespace pyre {
    namespace extensions {
        namespace mpi {

            // capsule names
            const char * const groupCapsuleName = "mpi.group";
            const char * const communicatorCapsuleName = "mpi.communicator";

            // types
            typedef pyre::mpi::group_t group_t;
            typedef pyre::mpi::communicator_t communicator_t;

        } // of namespace mpi
    } // of namespace extensions
} // of namespace pyre


# endif

// end of file
