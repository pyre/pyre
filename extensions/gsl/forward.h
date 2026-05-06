// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#if !defined(gsl_extension_forward_h)
#define gsl_extension_forward_h

// forward declarations of the wrapper types
namespace pyre::gsl {
    struct Vector;
    struct VectorView;
    struct Matrix;
    struct MatrixView;
    struct RNG;
    struct Permutation;
    struct Histogram;
} // namespace pyre::gsl

// forward declarations of the per-subsystem binding functions
namespace pyre::gsl::py {
    // rng initialization (called once at module load)
    void rng_initialize();
    // subsystem binders
    void blas(::py::module &);
    void histogram(::py::module &);
    void linalg(::py::module &);
    void matrix(::py::module &);
    void pdf(::py::module &);
    void permutation(::py::module &);
    void rng(::py::module &);
    void stats(::py::module &);
    void vector(::py::module &);
#if defined(WITH_MPI)
    void partition(::py::module &);
#endif
} // namespace pyre::gsl::py

#endif

// end of file
