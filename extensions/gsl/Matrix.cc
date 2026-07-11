// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the vectors my rows and columns cross into, and the symmetric eigenproblem
#include <gsl/gsl_vector.h>
#include <gsl/gsl_eigen.h>
// the file i/o
#include <cstdio>


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

    // allocate a matrix of the given {shape}
    cls.def(
        // the implementation
        py::init([](shape_type shape) -> matrix_ptr {
            // ask gsl for storage
            return matrix_ptr(gsl_matrix_alloc(shape.first, shape.second));
        }),
        // the signature
        "shape"_a,
        // the docstring
        "allocate a matrix of the given {shape}");

    // build a view into the data of another matrix
    //
    // the view is a {gsl_matrix} that borrows the parent's block, so it must not outlive it;
    // {keep_alive} ties the parent to me for exactly as long as i am around
    cls.def(
        // the implementation
        py::init([](gsl_matrix & parent, shape_type start, shape_type shape) -> matrix_ptr {
            // ask gsl to describe the submatrix
            auto view =
                gsl_matrix_submatrix(&parent, start.first, start.second, shape.first, shape.second);
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

    // initialization
    // set all my cells to zero
    cls.def(
        // the name
        "zero",
        // the implementation
        [](py::object self) -> py::object {
            // gsl zeroes the block
            gsl_matrix_set_zero(&self.cast<gsl_matrix &>());
            // hand myself back, so callers can chain
            return self;
        },
        // the docstring
        "set all my cells to zero, and return me");

    // set all my cells to {value}
    cls.def(
        // the name
        "fill",
        // the implementation
        [](py::object self, double value) -> py::object {
            // gsl writes the value everywhere
            gsl_matrix_set_all(&self.cast<gsl_matrix &>(), value);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "value"_a,
        // the docstring
        "set all my cells to {value}, and return me");

    // make me the identity: ones on the diagonal, zeros elsewhere
    cls.def(
        // the name
        "identity",
        // the implementation
        [](py::object self) -> py::object {
            // gsl lays down the identity
            gsl_matrix_set_identity(&self.cast<gsl_matrix &>());
            // hand myself back, so callers can chain
            return self;
        },
        // the docstring
        "make me the identity matrix, and return me");

    // overwrite my cells with those of {other}, which must have my shape
    cls.def(
        // the name
        "copy",
        // the implementation
        [](py::object self, const gsl_matrix & other) -> py::object {
            // gsl copies the cells across
            gsl_matrix_memcpy(&self.cast<gsl_matrix &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "overwrite my cells with those of {other}, and return me");

    // access; the index is a {row, column} pair, and either may be negative to count from the end
    // the value at {index}
    cls.def(
        // the name
        "get",
        // the implementation
        [](const gsl_matrix & self, std::pair<long, long> index) -> double {
            // reflect negative coordinates about the ends
            long i = index.first < 0 ? index.first + (long) self.size1 : index.first;
            long j = index.second < 0 ? index.second + (long) self.size2 : index.second;
            // bounds check, so out of range reads raise rather than read past the block
            if (i < 0 || (std::size_t) i >= self.size1 || j < 0 || (std::size_t) j >= self.size2) {
                throw py::index_error("matrix index out of range");
            }
            // hand back the cell
            return gsl_matrix_get(&self, i, j);
        },
        // the signature
        "index"_a,
        // the docstring
        "the value at the {row, column} {index}");

    // set the cell at {index} to {value}
    cls.def(
        // the name
        "set",
        // the implementation
        [](gsl_matrix & self, std::pair<long, long> index, double value) -> void {
            // reflect negative coordinates about the ends
            long i = index.first < 0 ? index.first + (long) self.size1 : index.first;
            long j = index.second < 0 ? index.second + (long) self.size2 : index.second;
            // bounds check
            if (i < 0 || (std::size_t) i >= self.size1 || j < 0 || (std::size_t) j >= self.size2) {
                throw py::index_error("matrix index out of range");
            }
            // write the cell
            gsl_matrix_set(&self, i, j, value);
        },
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "set the cell at the {row, column} {index} to {value}");

    // my cells as a tuple of rows, each itself a tuple
    cls.def(
        // the name
        "tuple",
        // the implementation
        [](const gsl_matrix & self) -> py::tuple {
            // one entry per row
            py::tuple rows(self.size1);
            // fill each
            for (std::size_t i = 0; i < self.size1; ++i) {
                // with a tuple of that row's cells
                py::tuple row(self.size2);
                for (std::size_t j = 0; j < self.size2; ++j) {
                    row[j] = gsl_matrix_get(&self, i, j);
                }
                rows[i] = row;
            }
            // and hand the whole back
            return rows;
        },
        // the docstring
        "my cells as a tuple of rows, each a tuple of doubles");

    // whether any of my cells equals {value}
    cls.def(
        // the name
        "contains",
        // the implementation
        [](const gsl_matrix & self, double value) -> bool {
            // scan my cells
            for (std::size_t i = 0; i < self.size1; ++i) {
                for (std::size_t j = 0; j < self.size2; ++j) {
                    // and report the first match
                    if (gsl_matrix_get(&self, i, j) == value) {
                        return true;
                    }
                }
            }
            // otherwise, no match
            return false;
        },
        // the signature
        "value"_a,
        // the docstring
        "whether any of my cells equals {value}");

    // whether {other} has my shape and my values
    cls.def(
        // the name
        "equal",
        // the implementation
        [](const gsl_matrix & self, const gsl_matrix & other) -> bool {
            // gsl compares shape and cells
            return gsl_matrix_equal(&self, &other) == 1;
        },
        // the signature
        "other"_a,
        // the docstring
        "whether {other} has my shape and my values");

    // extrema
    // my largest cell
    cls.def(
        // the name
        "max",
        // the implementation
        [](const gsl_matrix & self) -> double { return gsl_matrix_max(&self); },
        // the docstring
        "my largest cell");

    // my smallest cell
    cls.def(
        // the name
        "min",
        // the implementation
        [](const gsl_matrix & self) -> double { return gsl_matrix_min(&self); },
        // the docstring
        "my smallest cell");

    // my smallest and largest cells, as a pair
    cls.def(
        // the name
        "minmax",
        // the implementation
        [](const gsl_matrix & self) -> std::pair<double, double> {
            // room for the answer
            double small = 0, large = 0;
            // gsl finds both in one pass
            gsl_matrix_minmax(&self, &small, &large);
            // and we hand them back in order
            return { small, large };
        },
        // the docstring
        "my smallest and largest cells, as a pair");

    // elementwise arithmetic, in place
    // add the cells of {other} to mine
    cls.def(
        // the name
        "add",
        // the implementation
        [](py::object self, const gsl_matrix & other) -> py::object {
            // gsl adds cell by cell
            gsl_matrix_add(&self.cast<gsl_matrix &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "add the cells of {other} to mine, and return me");

    // subtract the cells of {other} from mine
    cls.def(
        // the name
        "sub",
        // the implementation
        [](py::object self, const gsl_matrix & other) -> py::object {
            // gsl subtracts cell by cell
            gsl_matrix_sub(&self.cast<gsl_matrix &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "subtract the cells of {other} from mine, and return me");

    // multiply my cells by those of {other}
    cls.def(
        // the name
        "mul",
        // the implementation
        [](py::object self, const gsl_matrix & other) -> py::object {
            // gsl multiplies cell by cell
            gsl_matrix_mul_elements(&self.cast<gsl_matrix &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "multiply my cells by those of {other}, and return me");

    // divide my cells by those of {other}
    cls.def(
        // the name
        "div",
        // the implementation
        [](py::object self, const gsl_matrix & other) -> py::object {
            // gsl divides cell by cell
            gsl_matrix_div_elements(&self.cast<gsl_matrix &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "divide my cells by those of {other}, and return me");

    // raise every cell by the constant {offset}
    cls.def(
        // the name
        "shift",
        // the implementation
        [](py::object self, double offset) -> py::object {
            // gsl adds the constant everywhere
            gsl_matrix_add_constant(&self.cast<gsl_matrix &>(), offset);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "offset"_a,
        // the docstring
        "raise every cell by the constant {offset}, and return me");

    // scale every cell by the constant {factor}
    cls.def(
        // the name
        "scale",
        // the implementation
        [](py::object self, double factor) -> py::object {
            // gsl multiplies every cell by the constant
            gsl_matrix_scale(&self.cast<gsl_matrix &>(), factor);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "factor"_a,
        // the docstring
        "scale every cell by the constant {factor}, and return me");

    // transpose; with no {destination} the transpose happens in place and needs me square, and
    // with one my transpose is written there and i am left untouched
    cls.def(
        // the name
        "transpose",
        // the implementation
        [](py::object self, gsl_matrix * destination) -> py::object {
            // in place, when nobody supplied a destination
            if (!destination) {
                gsl_matrix_transpose(&self.cast<gsl_matrix &>());
                // hand myself back
                return self;
            }
            // otherwise, gsl writes my transpose into the destination
            gsl_matrix_transpose_memcpy(destination, &self.cast<gsl_matrix &>());
            // and that is the answer
            return py::cast(destination);
        },
        // the signature
        "destination"_a = nullptr,
        // the docstring
        "transpose me in place, or into {destination} when one is given");

    // rows and columns; the caller allocates the vector each of these fills or reads
    // copy my {index}th row into {vector}
    cls.def(
        // the name
        "getRow",
        // the implementation
        [](const gsl_matrix & self, std::size_t index, gsl_vector & vector) -> void {
            // gsl copies the row out
            gsl_matrix_get_row(&vector, &self, index);
        },
        // the signature
        "index"_a, "vector"_a,
        // the docstring
        "copy my {index}th row into {vector}");

    // copy my {index}th column into {vector}
    cls.def(
        // the name
        "getColumn",
        // the implementation
        [](const gsl_matrix & self, std::size_t index, gsl_vector & vector) -> void {
            // gsl copies the column out
            gsl_matrix_get_col(&vector, &self, index);
        },
        // the signature
        "index"_a, "vector"_a,
        // the docstring
        "copy my {index}th column into {vector}");

    // set my {index}th row from the cells of {vector}
    cls.def(
        // the name
        "setRow",
        // the implementation
        [](py::object self, std::size_t index, const gsl_vector & vector) -> py::object {
            // gsl writes the row
            gsl_matrix_set_row(&self.cast<gsl_matrix &>(), index, &vector);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "index"_a, "vector"_a,
        // the docstring
        "set my {index}th row from the cells of {vector}, and return me");

    // set my {index}th column from the cells of {vector}
    cls.def(
        // the name
        "setColumn",
        // the implementation
        [](py::object self, std::size_t index, const gsl_vector & vector) -> py::object {
            // gsl writes the column
            gsl_matrix_set_col(&self.cast<gsl_matrix &>(), index, &vector);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "index"_a, "vector"_a,
        // the docstring
        "set my {index}th column from the cells of {vector}, and return me");

    // the symmetric eigenproblem; the caller allocates {eigenvalues} to my order and
    // {eigenvectors} to my shape, and we fill both, ordering them by {order}
    cls.def(
        // the name
        "eigenSymmetric",
        // the implementation
        [](const gsl_matrix & self, gsl_eigen_sort_t order, gsl_vector & eigenvalues,
           gsl_matrix & eigenvectors) -> void {
            // gsl destroys the matrix it works on, so it gets a private copy of me
            gsl_matrix * work = gsl_matrix_alloc(self.size1, self.size2);
            gsl_matrix_memcpy(work, &self);
            // the solver needs scratch space of my order
            gsl_eigen_symmv_workspace * space = gsl_eigen_symmv_alloc(self.size1);
            // solve, filling the caller's storage
            gsl_eigen_symmv(work, &eigenvalues, &eigenvectors, space);
            // put the answer in the requested order
            gsl_eigen_symmv_sort(&eigenvalues, &eigenvectors, order);
            // and release the scratch space and the working copy
            gsl_eigen_symmv_free(space);
            gsl_matrix_free(work);
        },
        // the signature
        "order"_a, "eigenvalues"_a, "eigenvectors"_a,
        // the docstring
        "fill {eigenvalues} and {eigenvectors} with my symmetric eigenproblem, ordered by "
        "{order}");

    // file i/o; the caller has already turned its path into a string
    // read my cells from the binary file {filename}
    cls.def(
        // the name
        "fread",
        // the implementation
        [](py::object self, const std::string & filename) -> py::object {
            // open the file for binary reading
            std::FILE * stream = std::fopen(filename.data(), "rb");
            // complain if it would not open
            if (!stream) {
                throw py::value_error("could not open '" + filename + "' for reading");
            }
            // pull my cells in, and close up
            gsl_matrix_fread(stream, &self.cast<gsl_matrix &>());
            std::fclose(stream);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "filename"_a,
        // the docstring
        "read my cells from the binary file {filename}, and return me");

    // write my cells to the binary file {filename}
    cls.def(
        // the name
        "fwrite",
        // the implementation
        [](py::object self, const std::string & filename) -> py::object {
            // open the file for binary writing
            std::FILE * stream = std::fopen(filename.data(), "wb");
            // complain if it would not open
            if (!stream) {
                throw py::value_error("could not open '" + filename + "' for writing");
            }
            // push my cells out, and close up
            gsl_matrix_fwrite(stream, &self.cast<gsl_matrix &>());
            std::fclose(stream);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "filename"_a,
        // the docstring
        "write my cells to the binary file {filename}, and return me");

    // read my cells from the text file {filename}
    cls.def(
        // the name
        "fscanf",
        // the implementation
        [](py::object self, const std::string & filename) -> py::object {
            // open the file for reading
            std::FILE * stream = std::fopen(filename.data(), "r");
            // complain if it would not open
            if (!stream) {
                throw py::value_error("could not open '" + filename + "' for reading");
            }
            // scan my cells in, and close up
            gsl_matrix_fscanf(stream, &self.cast<gsl_matrix &>());
            std::fclose(stream);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "filename"_a,
        // the docstring
        "read my cells from the text file {filename}, and return me");

    // write my cells to the text file {filename}, in the given {format}
    cls.def(
        // the name
        "fprintf",
        // the implementation
        [](py::object self, const std::string & filename,
           const std::string & format) -> py::object {
            // open the file for writing
            std::FILE * stream = std::fopen(filename.data(), "w");
            // complain if it would not open
            if (!stream) {
                throw py::value_error("could not open '" + filename + "' for writing");
            }
            // print my cells out, and close up
            gsl_matrix_fprintf(stream, &self.cast<gsl_matrix &>(), format.data());
            std::fclose(stream);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "filename"_a, "format"_a,
        // the docstring
        "write my cells to the text file {filename} in the given {format}, and return me");

    // all done
    return;
}


// end of file
