// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the permutation that an indirect sort fills, and the sort itself
#include <gsl/gsl_permutation.h>
#include <gsl/gsl_sort_vector.h>
// the statistics over my elements
#include <gsl/gsl_statistics.h>
// the file i/o
#include <cstdio>


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

    // turn a user index into a valid cell, or raise
    //
    // a negative index counts from the end, python style; anything that still falls outside
    // [0, size) is out of range. we check here rather than lean on gsl's own range check, which
    // is a compile-time option and, even when on, quietly returns zero and logs rather than
    // raising
    inline auto cell(std::size_t size, long i) -> std::size_t
    {
        // reflect a negative index about the end
        long index = i < 0 ? i + (long) size : i;
        // and complain if it still lands outside the vector
        if (index < 0 || (std::size_t) index >= size) {
            throw py::index_error("vector index out of range");
        }
        // the index is good
        return index;
    }
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

    // allocate a vector of the given {shape}
    cls.def(
        // the implementation
        py::init([](std::size_t shape) -> vector_ptr {
            // ask gsl for storage
            return vector_ptr(gsl_vector_alloc(shape));
        }),
        // the signature
        "shape"_a,
        // the docstring
        "allocate a vector with {shape} cells");

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

    // initialization
    // set all my cells to zero
    cls.def(
        // the name
        "zero",
        // the implementation
        [](py::object self) -> py::object {
            // gsl zeroes the block
            gsl_vector_set_zero(&self.cast<gsl_vector &>());
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
            gsl_vector_set_all(&self.cast<gsl_vector &>(), value);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "value"_a,
        // the docstring
        "set all my cells to {value}, and return me");

    // make me the {i}th basis vector: all zero but for a one at {i}
    cls.def(
        // the name
        "basis",
        // the implementation
        [](py::object self, long i) -> py::object {
            // the vector behind {self}
            auto & v = self.cast<gsl_vector &>();
            // gsl zeroes me and sets the one cell the checked index names
            gsl_vector_set_basis(&v, cell(v.size, i));
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "i"_a,
        // the docstring
        "make me the {i}th basis vector, and return me");

    // overwrite my cells with those of {other}, which must have my shape
    cls.def(
        // the name
        "copy",
        // the implementation
        [](py::object self, const gsl_vector & other) -> py::object {
            // gsl copies the cells across
            gsl_vector_memcpy(&self.cast<gsl_vector &>(), &other);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "overwrite my cells with those of {other}, and return me");

    // access
    // the value of my {i}th cell
    cls.def(
        // the name
        "get",
        // the implementation
        [](const gsl_vector & self, long i) -> double {
            // read the cell the checked index names
            return gsl_vector_get(&self, cell(self.size, i));
        },
        // the signature
        "i"_a,
        // the docstring
        "the value of my {i}th cell");

    // set my {i}th cell to {value}
    cls.def(
        // the name
        "set",
        // the implementation
        [](gsl_vector & self, long i, double value) -> void {
            // write the cell the checked index names
            gsl_vector_set(&self, cell(self.size, i), value);
        },
        // the signature
        "i"_a, "value"_a,
        // the docstring
        "set my {i}th cell to {value}");

    // my cells as a tuple
    cls.def(
        // the name
        "tuple",
        // the implementation
        [](const gsl_vector & self) -> py::tuple {
            // room for one entry per cell
            py::tuple result(self.size);
            // fill it, cell by cell
            for (std::size_t i = 0; i < self.size; ++i) {
                result[i] = gsl_vector_get(&self, i);
            }
            // and hand it back
            return result;
        },
        // the docstring
        "my cells as a tuple");

    // whether any of my cells equals {value}
    cls.def(
        // the name
        "contains",
        // the implementation
        [](const gsl_vector & self, double value) -> bool {
            // scan my cells
            for (std::size_t i = 0; i < self.size; ++i) {
                // and report the first match
                if (gsl_vector_get(&self, i) == value) {
                    return true;
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
        [](const gsl_vector & self, const gsl_vector & other) -> bool {
            // gsl compares shape and cells
            return gsl_vector_equal(&self, &other) == 1;
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
        [](const gsl_vector & self) -> double { return gsl_vector_max(&self); },
        // the docstring
        "my largest cell");

    // my smallest cell
    cls.def(
        // the name
        "min",
        // the implementation
        [](const gsl_vector & self) -> double { return gsl_vector_min(&self); },
        // the docstring
        "my smallest cell");

    // my smallest and largest cells, as a pair
    cls.def(
        // the name
        "minmax",
        // the implementation
        [](const gsl_vector & self) -> std::pair<double, double> {
            // room for the answer
            double small = 0, large = 0;
            // gsl finds both in one pass
            gsl_vector_minmax(&self, &small, &large);
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
        [](py::object self, const gsl_vector & other) -> py::object {
            // gsl adds cell by cell
            gsl_vector_add(&self.cast<gsl_vector &>(), &other);
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
        [](py::object self, const gsl_vector & other) -> py::object {
            // gsl subtracts cell by cell
            gsl_vector_sub(&self.cast<gsl_vector &>(), &other);
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
        [](py::object self, const gsl_vector & other) -> py::object {
            // gsl multiplies cell by cell
            gsl_vector_mul(&self.cast<gsl_vector &>(), &other);
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
        [](py::object self, const gsl_vector & other) -> py::object {
            // gsl divides cell by cell
            gsl_vector_div(&self.cast<gsl_vector &>(), &other);
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
            gsl_vector_add_constant(&self.cast<gsl_vector &>(), offset);
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
            gsl_vector_scale(&self.cast<gsl_vector &>(), factor);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "factor"_a,
        // the docstring
        "scale every cell by the constant {factor}, and return me");

    // statistics
    // sort my cells into ascending order, in place
    cls.def(
        // the name
        "sort",
        // the implementation
        [](py::object self) -> py::object {
            // gsl sorts the block
            gsl_sort_vector(&self.cast<gsl_vector &>());
            // hand myself back, so callers can chain
            return self;
        },
        // the docstring
        "sort my cells into ascending order, and return me");

    // the mean of my cells, optionally weighted by the cells of {weights}
    cls.def(
        // the name
        "mean",
        // the implementation
        [](const gsl_vector & self, const gsl_vector * weights) -> double {
            // an unweighted mean when nobody supplied weights
            if (!weights) {
                return gsl_stats_mean(self.data, self.stride, self.size);
            }
            // otherwise, the weighted mean
            return gsl_stats_wmean(
                weights->data, weights->stride, self.data, self.stride, self.size);
        },
        // the signature
        "weights"_a = nullptr,
        // the docstring
        "the mean of my cells, optionally weighted by {weights}");

    // the median of my cells, which must already be sorted
    cls.def(
        // the name
        "median",
        // the implementation
        [](const gsl_vector & self) -> double {
            // gsl reads the middle of the sorted run
            return gsl_stats_median_from_sorted_data(self.data, self.stride, self.size);
        },
        // the docstring
        "the median of my cells, which i assume are already sorted");

    // the variance of my cells, about {mean} when given, or about their own mean otherwise
    cls.def(
        // the name
        "variance",
        // the implementation
        [](const gsl_vector & self, std::optional<double> mean) -> double {
            // about the given mean, when there is one
            if (mean) {
                return gsl_stats_variance_m(self.data, self.stride, self.size, *mean);
            }
            // otherwise, about the mean computed on the fly
            return gsl_stats_variance(self.data, self.stride, self.size);
        },
        // the signature
        "mean"_a = py::none(),
        // the docstring
        "the variance of my cells, about {mean} if given, else about their own mean");

    // the standard deviation of my cells, about {mean} when given
    cls.def(
        // the name
        "sdev",
        // the implementation
        [](const gsl_vector & self, std::optional<double> mean) -> double {
            // about the given mean, when there is one
            if (mean) {
                return gsl_stats_sd_m(self.data, self.stride, self.size, *mean);
            }
            // otherwise, about the mean computed on the fly
            return gsl_stats_sd(self.data, self.stride, self.size);
        },
        // the signature
        "mean"_a = py::none(),
        // the docstring
        "the standard deviation of my cells, about {mean} if given, else about their own mean");

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
            gsl_vector_fread(stream, &self.cast<gsl_vector &>());
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
            gsl_vector_fwrite(stream, &self.cast<gsl_vector &>());
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
            gsl_vector_fscanf(stream, &self.cast<gsl_vector &>());
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
            gsl_vector_fprintf(stream, &self.cast<gsl_vector &>(), format.data());
            std::fclose(stream);
            // hand myself back, so callers can chain
            return self;
        },
        // the signature
        "filename"_a, "format"_a,
        // the docstring
        "write my cells to the text file {filename} in the given {format}, and return me");

    // the number of cells i hold, so that {len} works
    cls.def(
        // the name
        "__len__",
        // the implementation
        [](const gsl_vector & self) -> std::size_t { return self.size; },
        // the docstring
        "the number of cells i hold");

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

    // all done
    return;
}


// end of file
