// -*- C++ -*-
//
// michael a.g. aivazis
// orthologue
// (c) 1998-2023 all rights reserved
//

#if !defined(pyre_mpi_Error_h)
#define pyre_mpi_Error_h


// forward declarations
namespace pyre::mpi {
    class Error;
} // namespace pyre::mpi


// a wrapper around MPI_Error
class pyre::mpi::Error : public std::exception {
    // interface
public:
    inline auto code() const -> int;

    // meta-methods
public:
    inline Error(int code);
    inline ~Error();

    // data
private:
    int _code; // the raw MPI error code
};

// get the inline definitions
#define pyre_mpi_Error_icc
#include "Error.icc"
#undef pyre_mpi_Error_icc

#endif

// end of file
