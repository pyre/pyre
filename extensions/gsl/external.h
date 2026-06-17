// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#if !defined(gsl_extension_external_h)
#define gsl_extension_external_h

// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

// STL
#include <map>
#include <memory>
#include <string>
#include <tuple>
#include <cstdio>
#include <sstream>

// GSL
#include <gsl/gsl_blas.h>
#include <gsl/gsl_cdf.h>
#include <gsl/gsl_eigen.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_histogram.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_permutation.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_sort_vector.h>
#include <gsl/gsl_statistics.h>
#include <gsl/gsl_vector.h>

// pyre
#include <pyre/journal.h>

// convenience
namespace py = pybind11;
using namespace pybind11::literals;


// thin C++ wrappers around GSL opaque types
namespace pyre::gsl {

    // vector
    struct Vector {
        gsl_vector * ptr = nullptr;
        bool owner;
        explicit Vector(size_t n) : ptr(gsl_vector_alloc(n)), owner(true) {}
        Vector(gsl_vector * v, bool own) : ptr(v), owner(own) {}
        ~Vector() { if (owner && ptr) { gsl_vector_free(ptr); ptr = nullptr; } }
        // non-copyable
        Vector(const Vector &) = delete;
        Vector & operator=(const Vector &) = delete;
        // movable
        Vector(Vector && o) noexcept : ptr(o.ptr), owner(o.owner) {
            o.ptr = nullptr; o.owner = false;
        }
    };

    // view wrapper that owns the gsl_vector_view struct
    struct VectorView {
        gsl_vector_view view;
        explicit VectorView(gsl_vector * v, size_t origin, size_t shape)
            : view(gsl_vector_subvector(v, origin, shape)) {}
        // non-copyable, non-movable (gsl_vector_view contains embedded gsl_vector)
        VectorView(const VectorView &) = delete;
        VectorView & operator=(const VectorView &) = delete;
    };

    // matrix
    struct Matrix {
        gsl_matrix * ptr = nullptr;
        bool owner;
        Matrix(size_t r, size_t c) : ptr(gsl_matrix_alloc(r, c)), owner(true) {}
        Matrix(gsl_matrix * m, bool own) : ptr(m), owner(own) {}
        ~Matrix() { if (owner && ptr) { gsl_matrix_free(ptr); ptr = nullptr; } }
        Matrix(const Matrix &) = delete;
        Matrix & operator=(const Matrix &) = delete;
        Matrix(Matrix && o) noexcept : ptr(o.ptr), owner(o.owner) {
            o.ptr = nullptr; o.owner = false;
        }
    };

    // matrix view wrapper
    struct MatrixView {
        gsl_matrix_view view;
        explicit MatrixView(gsl_matrix * m,
                            size_t r0, size_t c0, size_t r1, size_t c1)
            : view(gsl_matrix_submatrix(m, r0, c0, r1, c1)) {}
        MatrixView(const MatrixView &) = delete;
        MatrixView & operator=(const MatrixView &) = delete;
    };

    // random number generator
    struct RNG {
        gsl_rng * ptr = nullptr;
        explicit RNG(const gsl_rng_type * t) : ptr(gsl_rng_alloc(t)) {}
        ~RNG() { if (ptr) { gsl_rng_free(ptr); ptr = nullptr; } }
        RNG(const RNG &) = delete;
        RNG & operator=(const RNG &) = delete;
    };

    // permutation
    struct Permutation {
        gsl_permutation * ptr = nullptr;
        explicit Permutation(size_t n) : ptr(gsl_permutation_alloc(n)) {}
        Permutation(gsl_permutation * p, bool /*take ownership*/)
            : ptr(p) {}
        ~Permutation() { if (ptr) { gsl_permutation_free(ptr); ptr = nullptr; } }
        Permutation(const Permutation &) = delete;
        Permutation & operator=(const Permutation &) = delete;
    };

    // histogram
    struct Histogram {
        gsl_histogram * ptr = nullptr;
        explicit Histogram(size_t n) : ptr(gsl_histogram_alloc(n)) {}
        Histogram(gsl_histogram * h, bool /*take ownership*/) : ptr(h) {}
        ~Histogram() { if (ptr) { gsl_histogram_free(ptr); ptr = nullptr; } }
        Histogram(const Histogram &) = delete;
        Histogram & operator=(const Histogram &) = delete;
    };

} // namespace pyre::gsl


// public interop API
#include "api.h"

#endif

// end of file
