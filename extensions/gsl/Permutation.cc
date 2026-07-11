// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the permutation
#include <gsl/gsl_permutation.h>


// the local helpers
namespace gsl::py {
    // gsl allocates every permutation through {gsl_permutation_alloc} and releases it through
    // {gsl_permutation_free}, so the handle python holds owns exactly one of them
    struct permutationDeleter {
        void operator()(gsl_permutation * p) const
        {
            // release the permutation, if there is one
            if (p) {
                gsl_permutation_free(p);
            }
        }
    };
    using permutation_ptr = std::unique_ptr<gsl_permutation, permutationDeleter>;
} // namespace gsl::py


// add the bindings for the gsl permutation
void
gsl::py::permutation(py::module & m)
{
    // the class
    auto cls = py::class_<gsl_permutation, permutation_ptr>(
        // in scope
        m,
        // the name
        "Permutation",
        // the docstring
        "a permutation of the integers [0, n), from gsl");

    // allocate a permutation of {shape} elements, initialized to the identity
    cls.def(
        // the implementation
        py::init([](std::size_t shape) -> permutation_ptr {
            // gsl hands back the identity permutation, already initialized
            return permutation_ptr(gsl_permutation_calloc(shape));
        }),
        // the signature
        "shape"_a,
        // the docstring
        "allocate a permutation of {shape} elements, initialized to the identity");

    // how many elements i permute
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const gsl_permutation & self) -> std::size_t { return gsl_permutation_size(&self); },
        // the docstring
        "the number of elements i permute");

    // reset me to the identity
    cls.def(
        // the name
        "init",
        // the implementation
        [](py::object self) -> py::object {
            // gsl writes the identity
            gsl_permutation_init(&self.cast<gsl_permutation &>());
            // hand myself back, so callers can chain
            return self;
        },
        // the docstring
        "reset me to the identity permutation, and return me");

    // allocate an independent copy of me
    cls.def(
        // the name
        "clone",
        // the implementation
        [](const gsl_permutation & self) -> permutation_ptr {
            // fresh storage of my size
            auto * copy = gsl_permutation_alloc(gsl_permutation_size(&self));
            // filled with my values
            gsl_permutation_memcpy(copy, &self);
            // and handed over
            return permutation_ptr(copy);
        },
        // the docstring
        "allocate an independent permutation carrying my values");

    // overwrite me with the values of {other}, which must have my size
    cls.def(
        // the name
        "copy",
        // the implementation
        [](py::object self, const gsl_permutation & other) -> py::object {
            // gsl overwrites my values with the other's
            gsl_permutation_memcpy(&self.cast<gsl_permutation &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "overwrite me with the values of {other}, and return me");

    // the value at index {i}
    cls.def(
        // the name
        "get",
        // the implementation
        [](const gsl_permutation & self, std::size_t i) -> std::size_t {
            // straight from gsl
            return gsl_permutation_get(&self, i);
        },
        // the signature
        "i"_a,
        // the docstring
        "the value at index {i}");

    // exchange the values at indices {i} and {j}
    cls.def(
        // the name
        "swap",
        // the implementation
        [](py::object self, std::size_t i, std::size_t j) -> py::object {
            // gsl exchanges the two values
            gsl_permutation_swap(&self.cast<gsl_permutation &>(), i, j);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "i"_a, "j"_a,
        // the docstring
        "exchange the values at indices {i} and {j}, and return me");

    // reverse me, in place
    cls.def(
        // the name
        "reverse",
        // the implementation
        [](py::object self) -> py::object {
            // gsl reverses my order
            gsl_permutation_reverse(&self.cast<gsl_permutation &>());
            // hand myself back, so callers can chain
            return self;
        },
        // the docstring
        "reverse my order, in place, and return me");

    // allocate my inverse
    cls.def(
        // the name
        "inverse",
        // the implementation
        [](const gsl_permutation & self) -> permutation_ptr {
            // fresh storage of my size
            auto * inv = gsl_permutation_alloc(gsl_permutation_size(&self));
            // filled with my inverse
            gsl_permutation_inverse(inv, &self);
            // and handed over
            return permutation_ptr(inv);
        },
        // the docstring
        "allocate the permutation that inverts me");

    // advance me to the next permutation in lexicographic order
    cls.def(
        // the name
        "next",
        // the implementation
        [](gsl_permutation & self) -> bool {
            // gsl reports GSL_SUCCESS while there is a next one, and steps me to it
            return gsl_permutation_next(&self) == GSL_SUCCESS;
        },
        // the docstring
        "step me to the next permutation, returning whether there was one");

    // step me back to the previous permutation in lexicographic order
    cls.def(
        // the name
        "prev",
        // the implementation
        [](gsl_permutation & self) -> bool {
            // gsl reports GSL_SUCCESS while there is a previous one, and steps me to it
            return gsl_permutation_prev(&self) == GSL_SUCCESS;
        },
        // the docstring
        "step me to the previous permutation, returning whether there was one");

    // whether i am a valid permutation
    cls.def(
        // the name
        "__bool__",
        // the implementation
        [](const gsl_permutation & self) -> bool {
            // gsl checks that every index appears exactly once
            return gsl_permutation_valid(&self) == GSL_SUCCESS;
        },
        // the docstring
        "whether i am a valid permutation, with every index appearing exactly once");

    // the number of elements i permute, so that {len} works
    cls.def(
        // the name
        "__len__",
        // the implementation
        [](const gsl_permutation & self) -> std::size_t { return gsl_permutation_size(&self); },
        // the docstring
        "the number of elements i permute");

    // all done
    return;
}


// end of file
