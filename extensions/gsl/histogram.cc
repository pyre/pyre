// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

namespace pyre::gsl::py {

void
histogram(::py::module & m)
{
    // register the Histogram type
    ::py::class_<pyre::gsl::Histogram>(m, "Histogram");

    // allocation
    m.def(
        "histogram_alloc",
        [](std::size_t n) {
            return std::make_unique<pyre::gsl::Histogram>(n);
        },
        "n"_a,
        "allocate a histogram with n bins");

    // uniform range initialization
    m.def(
        "histogram_uniform",
        [](pyre::gsl::Histogram & h, double lower, double upper) {
            gsl_histogram_set_ranges_uniform(h.ptr, lower, upper);
        },
        "h"_a, "lower"_a, "upper"_a,
        "set histogram bins with uniform coverage of a given range");

    // explicit range list initialization
    m.def(
        "histogram_ranges",
        [](pyre::gsl::Histogram & h, std::vector<double> ranges_list) {
            gsl_histogram_set_ranges(h.ptr, ranges_list.data(), ranges_list.size());
        },
        "h"_a, "ranges"_a,
        "set the histogram bin edges from a list of doubles");

    // reset
    m.def(
        "histogram_reset",
        [](pyre::gsl::Histogram & h) {
            gsl_histogram_reset(h.ptr);
        },
        "h"_a,
        "reset all histogram bin counts to zero");

    // increment
    m.def(
        "histogram_increment",
        [](pyre::gsl::Histogram & h, double x) {
            gsl_histogram_increment(h.ptr, x);
        },
        "h"_a, "x"_a,
        "increment by one the bin that contains the given value");

    // accumulate
    m.def(
        "histogram_accumulate",
        [](pyre::gsl::Histogram & h, double x, double weight) {
            gsl_histogram_accumulate(h.ptr, x, weight);
        },
        "h"_a, "x"_a, "weight"_a,
        "add the given weight to the bin that contains the given value");

    // fill: copy histogram data from src into dst
    m.def(
        "histogram_fill",
        [](pyre::gsl::Histogram & src, pyre::gsl::Histogram & dst) {
            gsl_histogram_memcpy(dst.ptr, src.ptr);
        },
        "src"_a, "dst"_a,
        "copy histogram data from src into dst");

    // clone
    m.def(
        "histogram_clone",
        [](pyre::gsl::Histogram & h) {
            gsl_histogram * clone = gsl_histogram_clone(h.ptr);
            return std::make_unique<pyre::gsl::Histogram>(clone, true);
        },
        "h"_a,
        "return an independent clone of the histogram");

    // copy
    m.def(
        "histogram_copy",
        [](pyre::gsl::Histogram & dst, pyre::gsl::Histogram & src) {
            gsl_histogram_memcpy(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "copy histogram data from src into dst");

    // vector: extract bin counts into a new pyre::gsl::Vector
    m.def(
        "histogram_vector",
        [](pyre::gsl::Histogram & h) {
            gsl_vector * v = gsl_vector_alloc(h.ptr->n);
            for (std::size_t i = 0; i < h.ptr->n; ++i) {
                gsl_vector_set(v, i, gsl_histogram_get(h.ptr, i));
            }
            return std::make_unique<pyre::gsl::Vector>(v, true);
        },
        "h"_a,
        "return a vector containing the histogram bin counts");

    // find
    m.def(
        "histogram_find",
        [](pyre::gsl::Histogram & h, double x) -> std::size_t {
            std::size_t bin = 0;
            gsl_histogram_find(h.ptr, x, &bin);
            return bin;
        },
        "h"_a, "x"_a,
        "return the index of the bin that contains x");

    // max upper range bound
    m.def(
        "histogram_max",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_max(h.ptr);
        },
        "h"_a,
        "return the maximum upper range of the histogram");

    // min lower range bound
    m.def(
        "histogram_min",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_min(h.ptr);
        },
        "h"_a,
        "return the minimum lower range of the histogram");

    // value of bin i
    m.def(
        "histogram_range",
        [](pyre::gsl::Histogram & h, std::size_t i) -> double {
            return gsl_histogram_get(h.ptr, i);
        },
        "h"_a, "i"_a,
        "return the value of bin i");

    // index of the bin with the maximum count
    m.def(
        "histogram_max_bin",
        [](pyre::gsl::Histogram & h) -> std::size_t {
            return gsl_histogram_max_bin(h.ptr);
        },
        "h"_a,
        "return the index of the bin with the maximum count");

    // index of the bin with the minimum count
    m.def(
        "histogram_min_bin",
        [](pyre::gsl::Histogram & h) -> std::size_t {
            return gsl_histogram_min_bin(h.ptr);
        },
        "h"_a,
        "return the index of the bin with the minimum count");

    // maximum bin count value
    m.def(
        "histogram_max_val",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_max_val(h.ptr);
        },
        "h"_a,
        "return the maximum bin count value");

    // minimum bin count value
    m.def(
        "histogram_min_val",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_min_val(h.ptr);
        },
        "h"_a,
        "return the minimum bin count value");

    // mean
    m.def(
        "histogram_mean",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_mean(h.ptr);
        },
        "h"_a,
        "compute the mean value of the histogram");

    // standard deviation
    m.def(
        "histogram_sdev",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_sigma(h.ptr);
        },
        "h"_a,
        "compute the standard deviation of the histogram");

    // sum
    m.def(
        "histogram_sum",
        [](pyre::gsl::Histogram & h) -> double {
            return gsl_histogram_sum(h.ptr);
        },
        "h"_a,
        "compute the sum of all bin counts");

    // get a single bin value
    m.def(
        "histogram_get",
        [](pyre::gsl::Histogram & h, std::size_t i) -> double {
            return gsl_histogram_get(h.ptr, i);
        },
        "h"_a, "i"_a,
        "return the count in bin i");

    // in-place arithmetic
    m.def(
        "histogram_add",
        [](pyre::gsl::Histogram & dst, pyre::gsl::Histogram & src) {
            gsl_histogram_add(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "in-place addition of two histograms");

    m.def(
        "histogram_sub",
        [](pyre::gsl::Histogram & dst, pyre::gsl::Histogram & src) {
            gsl_histogram_sub(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "in-place subtraction of two histograms");

    m.def(
        "histogram_mul",
        [](pyre::gsl::Histogram & dst, pyre::gsl::Histogram & src) {
            gsl_histogram_mul(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "in-place element-wise multiplication of two histograms");

    m.def(
        "histogram_div",
        [](pyre::gsl::Histogram & dst, pyre::gsl::Histogram & src) {
            gsl_histogram_div(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "in-place element-wise division of two histograms");

    m.def(
        "histogram_shift",
        [](pyre::gsl::Histogram & h, double offset) {
            gsl_histogram_shift(h.ptr, offset);
        },
        "h"_a, "offset"_a,
        "add a constant offset to all histogram bin counts");

    m.def(
        "histogram_scale",
        [](pyre::gsl::Histogram & h, double scale) {
            gsl_histogram_scale(h.ptr, scale);
        },
        "h"_a, "scale"_a,
        "multiply all histogram bin counts by a constant scale factor");
}

} // namespace pyre::gsl::py

// end of file
