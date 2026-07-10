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


// the local helpers
namespace gsl::py {
    // hand a matrix back to whoever gave it to us
    //
    // gsl marks the matrices it allocates as the owners of their data block, and those go back
    // through {gsl_matrix_free}. a view is a {gsl_matrix} that borrows somebody else's block, so
    // it carries a clear {owner}; we build those ourselves, and only the struct is ours to free
    struct matrixDeleter {
        void operator()(gsl_matrix * m) const
        {
            // nothing to do for the empty handle
            if (!m) {
                return;
            }
            // a matrix that owns its block came from {gsl_matrix_alloc}
            if (m->owner) {
                // so it goes back the same way
                gsl_matrix_free(m);
                // all done
                return;
            }
            // anything else is a view i built, and its data belongs to its parent
            delete m;
            // all done
            return;
        }
    };

    // the owning handle python holds
    using matrix_ptr = std::unique_ptr<gsl_matrix, matrixDeleter>;

    // the shape of a matrix, and the anchor of a view, as they cross from python
    using shape_type = std::pair<std::size_t, std::size_t>;
} // namespace gsl::py


// add the bindings for the gsl matrix
void
gsl::py::matrix(py::module & m)
{
    // the class
    auto cls = py::class_<gsl_matrix, matrix_ptr>(
        // in scope
        m,
        // the name
        "Matrix",
        // let numpy and anybody else who speaks the buffer protocol see my data
        py::buffer_protocol(),
        // the docstring
        "a matrix of doubles, allocated and released by gsl");

    // allocate a matrix of the given {shape}, or adopt the one that {data} carries
    //
    // the {data} path is what the free functions that have not moved to pybind11 yet still hand
    // back: a capsule holding a {gsl_matrix} they allocated. we take it over, and disarm the
    // capsule so that it does not release what is now ours. it goes away with the last of them
    cls.def(
        // the implementation
        py::init([](shape_type shape, py::object data) -> matrix_ptr {
            // when nobody handed us storage
            if (data.is_none()) {
                // ask gsl for some
                return matrix_ptr(gsl_matrix_alloc(shape.first, shape.second));
            }
            // otherwise, {data} must be a matrix capsule
            PyObject * capsule = data.ptr();
            // and if it isn't
            if (!PyCapsule_IsValid(capsule, gsl::matrix::capsule_t)) {
                // say so
                throw py::type_error("expected a gsl matrix capsule");
            }
            // pull the matrix out
            auto * mat =
                static_cast<gsl_matrix *>(PyCapsule_GetPointer(capsule, gsl::matrix::capsule_t));
            // and take ownership away from the capsule, so it releases nothing
            PyCapsule_SetDestructor(capsule, nullptr);
            // the matrix is ours now
            return matrix_ptr(mat);
        }),
        // the signature
        "shape"_a, "data"_a = py::none(),
        // the docstring
        "allocate a matrix of the given {shape}, or adopt the one {data} carries");

    // build a view into the data of another matrix
    //
    // the view is a {gsl_matrix} that borrows the parent's block, so it must not outlive it;
    // {keep_alive} ties the parent to me for exactly as long as i am around
    cls.def(
        // the implementation
        py::init([](gsl_matrix & parent, shape_type start, shape_type shape) -> matrix_ptr {
            // ask gsl to describe the submatrix
            auto view = gsl_matrix_submatrix(
                &parent, start.first, start.second, shape.first, shape.second);
            // and take a copy of the descriptor it built; its {owner} is clear, so my deleter
            // releases the struct alone and leaves the parent's block untouched
            return matrix_ptr(new gsl_matrix(view.matrix));
        }),
        // the signature
        "matrix"_a, "start"_a, "shape"_a,
        // keep the parent alive for as long as the view is
        py::keep_alive<1, 2>(),
        // the docstring
        "build a view into {matrix}, anchored at {start} and spanning {shape}");

    // my shape, as a {rows, columns} pair
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const gsl_matrix & self) -> shape_type { return { self.size1, self.size2 }; },
        // the docstring
        "my shape, as a pair of the number of rows and the number of columns");

    // let numpy read my data without copying it
    cls.def_buffer([](gsl_matrix & self) -> py::buffer_info {
        // describe the block: a two dimensional grid of doubles. its rows are {tda} cells apart
        // rather than {size2}, so that submatrix views, which share the parent's wider rows,
        // still describe themselves correctly
        return py::buffer_info(
            // the payload
            self.data,
            // the size of a cell, and how to spell it
            sizeof(double), py::format_descriptor<double>::format(),
            // the number of axes, and the extent of each
            2, { self.size1, self.size2 },
            // the distance in octets between neighbours along each axis: a whole row apart down
            // the first, one cell apart across the second
            { sizeof(double) * self.tda, sizeof(double) });
    });

    // the transitional bridge to the free functions that have not moved to pybind11 yet
    //
    // they speak in capsules, so we hand them one that points at my {gsl_matrix} and releases
    // nothing: the bound object is what owns the storage. it is safe for the {f(m.data)} call
    // pattern they are used through, and it goes away with the last of them
    cls.def_property_readonly(
        // the name
        "data",
        // the implementation
        [](gsl_matrix & self) -> py::capsule {
            // a capsule that borrows, rather than owns
            return py::capsule(&self, gsl::matrix::capsule_t);
        },
        // the docstring
        "the underlying gsl matrix, for the free functions that have not moved yet");

    // all done
    return;
}


// end of file
