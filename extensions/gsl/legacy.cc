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
#include "matrix.h"      // matrices
#include "rng.h"         // random numbers
#include "vector.h"      // vectors

// mpi support
#if defined(WITH_MPI)
#include "partition.h"
#endif

// the table of the entities the module still publishes as free functions over capsules
namespace gsl::legacy {
PyMethodDef methods[] = {
    // matrices
    { matrix::alloc__name__, matrix::alloc, METH_VARARGS, matrix::alloc__doc__ },
    { matrix::view_alloc__name__, matrix::view_alloc, METH_VARARGS, matrix::view_alloc__doc__ },
    { matrix::zero__name__, matrix::zero, METH_VARARGS, matrix::zero__doc__ },
    { matrix::fill__name__, matrix::fill, METH_VARARGS, matrix::fill__doc__ },
    { matrix::identity__name__, matrix::identity, METH_VARARGS, matrix::identity__doc__ },
    { matrix::copy__name__, matrix::copy, METH_VARARGS, matrix::copy__doc__ },
    { matrix::tuple__name__, matrix::tuple, METH_VARARGS, matrix::tuple__doc__ },
    { matrix::read__name__, matrix::read, METH_VARARGS, matrix::read__doc__ },
    { matrix::write__name__, matrix::write, METH_VARARGS, matrix::write__doc__ },
    { matrix::scanf__name__, matrix::scanf, METH_VARARGS, matrix::scanf__doc__ },
    { matrix::printf__name__, matrix::printf, METH_VARARGS, matrix::printf__doc__ },
    { matrix::transpose__name__, matrix::transpose, METH_VARARGS, matrix::transpose__doc__ },
    { matrix::get__name__, matrix::get, METH_VARARGS, matrix::get__doc__ },
    { matrix::set__name__, matrix::set, METH_VARARGS, matrix::set__doc__ },
    { matrix::get_col__name__, matrix::get_col, METH_VARARGS, matrix::get_col__doc__ },
    { matrix::get_row__name__, matrix::get_row, METH_VARARGS, matrix::get_row__doc__ },
    { matrix::set_col__name__, matrix::set_col, METH_VARARGS, matrix::set_col__doc__ },
    { matrix::set_row__name__, matrix::set_row, METH_VARARGS, matrix::set_row__doc__ },
    { matrix::contains__name__, matrix::contains, METH_VARARGS, matrix::contains__doc__ },
    { matrix::max__name__, matrix::max, METH_VARARGS, matrix::max__doc__ },
    { matrix::min__name__, matrix::min, METH_VARARGS, matrix::min__doc__ },
    { matrix::minmax__name__, matrix::minmax, METH_VARARGS, matrix::minmax__doc__ },
    { matrix::equal__name__, matrix::equal, METH_VARARGS, matrix::equal__doc__ },
    { matrix::add__name__, matrix::add, METH_VARARGS, matrix::add__doc__ },
    { matrix::sub__name__, matrix::sub, METH_VARARGS, matrix::sub__doc__ },
    { matrix::mul__name__, matrix::mul, METH_VARARGS, matrix::mul__doc__ },
    { matrix::div__name__, matrix::div, METH_VARARGS, matrix::div__doc__ },
    { matrix::shift__name__, matrix::shift, METH_VARARGS, matrix::shift__doc__ },
    { matrix::scale__name__, matrix::scale, METH_VARARGS, matrix::scale__doc__ },
    { matrix::eigen_symmetric__name__, matrix::eigen_symmetric, METH_VARARGS,
      matrix::eigen_symmetric__doc__ },

    // random numbers
    { rng::avail__name__, rng::avail, METH_VARARGS, rng::avail__doc__ },
    { rng::alloc__name__, rng::alloc, METH_VARARGS, rng::alloc__doc__ },
    { rng::get__name__, rng::get, METH_VARARGS, rng::get__doc__ },
    { rng::name__name__, rng::name, METH_VARARGS, rng::name__doc__ },
    { rng::range__name__, rng::range, METH_VARARGS, rng::range__doc__ },
    { rng::set__name__, rng::set, METH_VARARGS, rng::set__doc__ },
    { rng::uniform__name__, rng::uniform, METH_VARARGS, rng::uniform__doc__ },

    // vectors
    { vector::alloc__name__, vector::alloc, METH_VARARGS, vector::alloc__doc__ },
    { vector::view_alloc__name__, vector::view_alloc, METH_VARARGS, vector::view_alloc__doc__ },
    { vector::zero__name__, vector::zero, METH_VARARGS, vector::zero__doc__ },
    { vector::fill__name__, vector::fill, METH_VARARGS, vector::fill__doc__ },
    { vector::basis__name__, vector::basis, METH_VARARGS, vector::basis__doc__ },
    { vector::copy__name__, vector::copy, METH_VARARGS, vector::copy__doc__ },
    { vector::tuple__name__, vector::tuple, METH_VARARGS, vector::tuple__doc__ },
    { vector::read__name__, vector::read, METH_VARARGS, vector::read__doc__ },
    { vector::write__name__, vector::write, METH_VARARGS, vector::write__doc__ },
    { vector::scanf__name__, vector::scanf, METH_VARARGS, vector::scanf__doc__ },
    { vector::printf__name__, vector::printf, METH_VARARGS, vector::printf__doc__ },
    { vector::get__name__, vector::get, METH_VARARGS, vector::get__doc__ },
    { vector::set__name__, vector::set, METH_VARARGS, vector::set__doc__ },
    { vector::contains__name__, vector::contains, METH_VARARGS, vector::contains__doc__ },
    { vector::max__name__, vector::max, METH_VARARGS, vector::max__doc__ },
    { vector::min__name__, vector::min, METH_VARARGS, vector::min__doc__ },
    { vector::minmax__name__, vector::minmax, METH_VARARGS, vector::minmax__doc__ },
    { vector::equal__name__, vector::equal, METH_VARARGS, vector::equal__doc__ },
    { vector::add__name__, vector::add, METH_VARARGS, vector::add__doc__ },
    { vector::sub__name__, vector::sub, METH_VARARGS, vector::sub__doc__ },
    { vector::mul__name__, vector::mul, METH_VARARGS, vector::mul__doc__ },
    { vector::div__name__, vector::div, METH_VARARGS, vector::div__doc__ },
    { vector::shift__name__, vector::shift, METH_VARARGS, vector::shift__doc__ },
    { vector::scale__name__, vector::scale, METH_VARARGS, vector::scale__doc__ },
    // statistics
    { vector::sort__name__, vector::sort, METH_VARARGS, vector::sort__doc__ },
    { vector::mean__name__, vector::mean, METH_VARARGS, vector::mean__doc__ },
    { vector::median__name__, vector::median, METH_VARARGS, vector::median__doc__ },
    { vector::variance__name__, vector::variance, METH_VARARGS, vector::variance__doc__ },
    { vector::sdev__name__, vector::sdev, METH_VARARGS, vector::sdev__doc__ },

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
