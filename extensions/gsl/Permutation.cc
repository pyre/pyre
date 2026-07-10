// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the permutation, and the capsule name the free functions that have not moved yet agree on
#include <gsl/gsl_permutation.h>
#include "capsules.h"


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

    // allocate a permutation of {shape} elements, or adopt the one that {data} carries
    //
    // the {data} path is what the free functions that have not moved to pybind11 yet still hand
    // back: a capsule holding a {gsl_permutation} they allocated. we take it over, and disarm the
    // capsule so that it does not release what is now ours. it goes away with the last of them
    cls.def(
        // the implementation
        py::init([](std::size_t shape, py::object data) -> permutation_ptr {
            // when nobody handed us storage
            if (data.is_none()) {
                // ask gsl for some, already initialized to the identity
                return permutation_ptr(gsl_permutation_calloc(shape));
            }
            // otherwise, {data} must be a permutation capsule
            PyObject * capsule = data.ptr();
            // and if it isn't
            if (!PyCapsule_IsValid(capsule, gsl::permutation::capsule_t)) {
                // say so
                throw py::type_error("expected a gsl permutation capsule");
            }
            // pull the permutation out
            auto * p = static_cast<gsl_permutation *>(
                PyCapsule_GetPointer(capsule, gsl::permutation::capsule_t));
            // and take ownership away from the capsule, so it releases nothing
            PyCapsule_SetDestructor(capsule, nullptr);
            // the permutation is ours now
            return permutation_ptr(p);
        }),
        // the signature
        "shape"_a, "data"_a = py::none(),
        // the docstring
        "allocate a permutation of {shape} elements, or adopt the one {data} carries");

    // how many elements i permute
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const gsl_permutation & self) -> std::size_t { return gsl_permutation_size(&self); },
        // the docstring
        "the number of elements i permute");

    // the transitional bridge to the free functions that have not moved to pybind11 yet
    //
    // they speak in capsules, so we hand them one that points at my {gsl_permutation} and
    // releases nothing, since the bound object owns it. it goes away with the last of them
    cls.def_property_readonly(
        // the name
        "data",
        // the implementation
        [](gsl_permutation & self) -> py::capsule {
            // a capsule that borrows, rather than owns
            return py::capsule(&self, gsl::permutation::capsule_t);
        },
        // the docstring
        "the underlying gsl permutation, for the free functions that have not moved yet");

    // all done
    return;
}


// end of file
