// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// my declarations
#include "legacy.h"

// the declarations of the entities that have not moved to pybind11 yet
#include "rng.h" // random numbers

// mpi support
#if defined(WITH_MPI)
#include "partition.h"
#endif


// the table of the entities the module still publishes as free functions over capsules
namespace gsl::legacy {
PyMethodDef methods[] = {
    // random numbers
    { rng::avail__name__, rng::avail, METH_VARARGS, rng::avail__doc__ },
    { rng::alloc__name__, rng::alloc, METH_VARARGS, rng::alloc__doc__ },
    { rng::get__name__, rng::get, METH_VARARGS, rng::get__doc__ },
    { rng::name__name__, rng::name, METH_VARARGS, rng::name__doc__ },
    { rng::range__name__, rng::range, METH_VARARGS, rng::range__doc__ },
    { rng::set__name__, rng::set, METH_VARARGS, rng::set__doc__ },
    { rng::uniform__name__, rng::uniform, METH_VARARGS, rng::uniform__doc__ },

// mpi support
#if defined(WITH_MPI)
    // matrix partitioning
    { mpi::bcastMatrix__name__, mpi::bcastMatrix, METH_VARARGS, mpi::bcastMatrix__doc__ },
    { mpi::gatherMatrix__name__, mpi::gatherMatrix, METH_VARARGS, mpi::gatherMatrix__doc__ },
    { mpi::scatterMatrix__name__, mpi::scatterMatrix, METH_VARARGS, mpi::scatterMatrix__doc__ },
    // vector partitioning
    { mpi::bcastVector__name__, mpi::bcastVector, METH_VARARGS, mpi::bcastVector__doc__ },
    { mpi::gatherVector__name__, mpi::gatherVector, METH_VARARGS, mpi::gatherVector__doc__ },
    { mpi::scatterVector__name__, mpi::scatterVector, METH_VARARGS, mpi::scatterVector__doc__ },
#endif

    // sentinel
    { 0, 0, 0, 0 }
};
} // namespace gsl::legacy


// end of file
