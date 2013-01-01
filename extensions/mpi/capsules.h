// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2013 all rights reserved
// 

#if !defined(pyre_extensions_mpi_capsules_h)
#define pyre_extensions_mpi_capsules_h

// capsules
namespace mpi {

    // communicator
    namespace communicator {
        const char * const capsule_t = "mpi.communicator"; 
        void free(PyObject *);
    }
    // group
    namespace group { 
        const char * const capsule_t = "mpi.group"; 
        void free(PyObject *);
    }

}
#endif

// end of file
