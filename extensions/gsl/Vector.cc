// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the capsule names the free functions that have not moved yet agree on
#include "capsules.h"
// the permutation that an indirect sort fills, and the sort itself
#include <gsl/gsl_permutation.h>
#include <gsl/gsl_sort_vector.h>


// the local helpers
namespace gsl::py {
    // hand a vector back to whoever gave it to us
    //
    // gsl marks the vectors it allocates as the owners of their data block, and those must go
    // back through {gsl_vector_free}. a view is a {gsl_vector} that borrows somebody else's
    // block, so it carries a clear {owner}; we build those ourselves, and only the struct is
    // ours to release
    struct vectorDeleter {
        void operator()(gsl_vector * v) const
        {
            // nothing to do for the empty handle
            if (!v) {
                return;
            }
            // a vector that owns its block came from {gsl_vector_alloc}
            if (v->owner) {
                // so it goes back the same way
                gsl_vector_free(v);
                // all done
                return;
            }
            // anything else is a view i built, and its data belongs to its parent
            delete v;
            // all done
            return;
        }
    };

    // the owning handle python holds
    using vector_ptr = std::unique_ptr<gsl_vector, vectorDeleter>;
} // namespace gsl::py


// add the bindings for the gsl vector
void
gsl::py::vector(py::module & m)
{
    // the class
    auto cls = py::class_<gsl_vector, vector_ptr>(
        // in scope
        m,
        // the name
        "Vector",
        // let numpy and anybody else who speaks the buffer protocol see my data
        py::buffer_protocol(),
        // the docstring
        "a vector of doubles, allocated and released by gsl");

    // allocate a vector of the given {shape}, or adopt the one that {data} carries
    //
    // the {data} path is what the free functions that have not moved to pybind11 yet still hand
    // back: a capsule holding a {gsl_vector} they allocated. we take it over, and disarm the
    // capsule so that it does not release what is now ours. it goes away with the last of them
    cls.def(
        // the implementation
        py::init([](std::size_t shape, py::object data) -> vector_ptr {
            // when nobody handed us storage
            if (data.is_none()) {
                // ask gsl for some
                return vector_ptr(gsl_vector_alloc(shape));
            }
            // otherwise, {data} must be a vector capsule
            PyObject * capsule = data.ptr();
            // and if it isn't
            if (!PyCapsule_IsValid(capsule, gsl::vector::capsule_t)) {
                // say so
                throw py::type_error("expected a gsl vector capsule");
            }
            // pull the vector out
            auto * v =
                static_cast<gsl_vector *>(PyCapsule_GetPointer(capsule, gsl::vector::capsule_t));
            // and take ownership away from the capsule, so it releases nothing
            PyCapsule_SetDestructor(capsule, nullptr);
            // the vector is ours now
            return vector_ptr(v);
        }),
        // the signature
        "shape"_a, "data"_a = py::none(),
        // the docstring
        "allocate a vector with {shape} cells, or adopt the one {data} carries");

    // build a view into the data of another vector
    //
    // the view is a {gsl_vector} that borrows the parent's block, so it must not outlive it;
    // {keep_alive} ties the parent to me for exactly as long as i am around
    cls.def(
        // the implementation
        py::init([](gsl_vector & parent, std::size_t start, std::size_t shape) -> vector_ptr {
            // ask gsl to describe the subvector
            auto view = gsl_vector_subvector(&parent, start, shape);
            // and take a copy of the descriptor it built; its {owner} is clear, so my deleter
            // releases the struct alone and leaves the parent's block untouched
            return vector_ptr(new gsl_vector(view.vector));
        }),
        // the signature
        "vector"_a, "start"_a, "shape"_a,
        // keep the parent alive for as long as the view is
        py::keep_alive<1, 2>(),
        // the docstring
        "build a view into {vector}, anchored at {start} and spanning {shape} cells");

    // how many cells i hold
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const gsl_vector & self) -> std::size_t { return self.size; },
        // the docstring
        "the number of cells i hold");

    // let numpy read my data without copying it
    cls.def_buffer([](gsl_vector & self) -> py::buffer_info {
        // describe the block: a one dimensional run of doubles, whose neighbours sit {stride}
        // cells apart, so that views over strided data describe themselves correctly
        return py::buffer_info(
            // the payload
            self.data,
            // the size of a cell, and how to spell it
            sizeof(double), py::format_descriptor<double>::format(),
            // the number of axes, and the extent of each
            1, { self.size },
            // the distance in octets between neighbours along the one axis
            { sizeof(double) * self.stride });
    });

    // fill {permutation} with the ordering that would sort me into ascending order, leaving me
    // untouched; the caller allocates {permutation} to my shape
    cls.def(
        // the name
        "sortIndex",
        // the implementation
        [](const gsl_vector & self, gsl_permutation & permutation) -> void {
            // gsl computes the sorting permutation without moving my elements
            gsl_sort_vector_index(&permutation, &self);
        },
        // the signature
        "permutation"_a,
        // the docstring
        "fill {permutation} with the ordering that would sort me into ascending order");

    // the transitional bridge to the free functions that have not moved to pybind11 yet
    //
    // they speak in capsules, so we hand them one that points at my {gsl_vector} and releases
    // nothing: the bound object is what owns the storage. it is safe for the {f(v.data)} call
    // pattern they are used through, and it goes away with the last of them
    cls.def_property_readonly(
        // the name
        "data",
        // the implementation
        [](gsl_vector & self) -> py::capsule {
            // a capsule that borrows, rather than owns
            return py::capsule(&self, gsl::vector::capsule_t);
        },
        // the docstring
        "the underlying gsl vector, for the free functions that have not moved yet");

    // all done
    return;
}


// end of file
