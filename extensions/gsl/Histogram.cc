// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the histogram
#include <gsl/gsl_histogram.h>


// the local helpers
namespace gsl::py {
    // gsl allocates every histogram through {gsl_histogram_alloc} and releases it through
    // {gsl_histogram_free}, so the handle python holds owns exactly one of them
    struct histogramDeleter {
        void operator()(gsl_histogram * h) const
        {
            // release the histogram, if there is one
            if (h) {
                gsl_histogram_free(h);
            }
        }
    };
    using histogram_ptr = std::unique_ptr<gsl_histogram, histogramDeleter>;
} // namespace gsl::py


// add the bindings for the gsl histogram
void
gsl::py::histogram(py::module & m)
{
    // the class
    auto cls = py::class_<gsl_histogram, histogram_ptr>(
        // in scope
        m,
        // the name
        "Histogram",
        // let numpy and anybody else who speaks the buffer protocol read my bin counts
        py::buffer_protocol(),
        // the docstring
        "a histogram of {bins} bins over a range of the reals, from gsl");

    // allocate a histogram of {bins} bins, with its counts zeroed
    cls.def(
        // the implementation
        py::init([](std::size_t bins) -> histogram_ptr {
            // ask gsl for storage, already zeroed
            return histogram_ptr(gsl_histogram_calloc(bins));
        }),
        // the signature
        "bins"_a,
        // the docstring
        "allocate a histogram of {bins} bins, with its counts zeroed");

    // structure
    // how many bins i hold
    cls.def_property_readonly(
        // the name
        "bins",
        // the implementation
        [](const gsl_histogram & self) -> std::size_t { return gsl_histogram_bins(&self); },
        // the docstring
        "the number of bins i hold");

    // the lower bound of the range i cover
    cls.def_property_readonly(
        // the name
        "lower",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_min(&self); },
        // the docstring
        "the lower bound of the range i cover");

    // the upper bound of the range i cover
    cls.def_property_readonly(
        // the name
        "upper",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_max(&self); },
        // the docstring
        "the upper bound of the range i cover");

    // statistics over the counts
    // the sum of all my bin counts
    cls.def_property_readonly(
        // the name
        "sum",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_sum(&self); },
        // the docstring
        "the sum of all my bin counts");

    // the mean of the histogrammed variable
    cls.def_property_readonly(
        // the name
        "mean",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_mean(&self); },
        // the docstring
        "the mean of the histogrammed variable, weighted by the counts");

    // the standard deviation of the histogrammed variable
    cls.def_property_readonly(
        // the name
        "sdev",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_sigma(&self); },
        // the docstring
        "the standard deviation of the histogrammed variable, weighted by the counts");

    // binning strategy
    // lay my bins out uniformly over [{lower}, {upper}), zeroing the counts
    cls.def(
        // the name
        "uniform",
        // the implementation
        [](py::object self, double lower, double upper) -> py::object {
            // spread the bins evenly across the range
            gsl_histogram_set_ranges_uniform(&self.cast<gsl_histogram &>(), lower, upper);
            // and hand myself back, so callers can chain
            return self;
        },
        // the signature
        "lower"_a, "upper"_a,
        // the docstring
        "lay my bins out uniformly over [{lower}, {upper}), and return me");

    // use the monotonically increasing {edges} as my bin boundaries; there must be one more
    // edge than i have bins, the last being the upper bound of the final bin
    cls.def(
        // the name
        "ranges",
        // the implementation
        [](py::object self, const std::vector<double> & edges) -> py::object {
            // hand gsl the boundaries
            gsl_histogram_set_ranges(&self.cast<gsl_histogram &>(), edges.data(), edges.size());
            // and hand myself back, so callers can chain
            return self;
        },
        // the signature
        "edges"_a,
        // the docstring
        "use the monotonic {edges} as my bin boundaries, and return me");

    // accumulation
    // set all my counts back to zero
    cls.def(
        // the name
        "reset",
        // the implementation
        [](py::object self) -> py::object {
            // clear the counts
            gsl_histogram_reset(&self.cast<gsl_histogram &>());
            // and hand myself back, so callers can chain
            return self;
        },
        // the docstring
        "set all my counts back to zero, and return me");

    // add one to the bin that contains {x}
    cls.def(
        // the name
        "increment",
        // the implementation
        [](py::object self, double x) -> py::object {
            // bump the bin that holds {x}
            gsl_histogram_increment(&self.cast<gsl_histogram &>(), x);
            // and hand myself back, so callers can chain
            return self;
        },
        // the signature
        "x"_a,
        // the docstring
        "add one to the bin that contains {x}, and return me");

    // add {weight} to the bin that contains {x}
    cls.def(
        // the name
        "accumulate",
        // the implementation
        [](py::object self, double x, double weight) -> py::object {
            // add the weight to the bin that holds {x}
            gsl_histogram_accumulate(&self.cast<gsl_histogram &>(), x, weight);
            // and hand myself back, so callers can chain
            return self;
        },
        // the signature
        "x"_a, "weight"_a,
        // the docstring
        "add {weight} to the bin that contains {x}, and return me");

    // queries
    // the index of the bin that contains {x}, or {None} when {x} lies outside my range
    cls.def(
        // the name
        "find",
        // the implementation
        [](const gsl_histogram & self, double x) -> py::object {
            // room for the answer
            std::size_t index = 0;
            // an {x} outside my range is a legitimate query with a {None} answer, not an error;
            // so silence gsl's handler for the duration, and put it back afterwards, rather than
            // let a miss reach the journal
            gsl_error_handler_t * handler = gsl_set_error_handler_off();
            // ask gsl, which reports whether {x} landed inside the range
            int status = gsl_histogram_find(&self, x, &index);
            // restore whatever handler was in place
            gsl_set_error_handler(handler);
            // outside the range, there is no bin to name
            if (status != GSL_SUCCESS) {
                return py::none();
            }
            // otherwise, hand back the bin
            return py::cast(index);
        },
        // the signature
        "x"_a,
        // the docstring
        "the index of the bin that contains {x}, or {None} if {x} is out of range");

    // the [lower, upper) range of the {i}th bin
    cls.def(
        // the name
        "range",
        // the implementation
        [](const gsl_histogram & self, std::size_t i) -> std::pair<double, double> {
            // bounds check, so an out of range bin raises rather than reading past the block
            if (i >= gsl_histogram_bins(&self)) {
                throw py::index_error("histogram bin index out of range");
            }
            // room for the answer
            double lower = 0, upper = 0;
            // ask gsl
            gsl_histogram_get_range(&self, i, &lower, &upper);
            // and hand back the pair
            return { lower, upper };
        },
        // the signature
        "i"_a,
        // the docstring
        "the [lower, upper) range of the {i}th bin, as a pair");

    // the largest count in any of my bins
    cls.def(
        // the name
        "max",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_max_val(&self); },
        // the docstring
        "the largest count in any of my bins");

    // the smallest count in any of my bins
    cls.def(
        // the name
        "min",
        // the implementation
        [](const gsl_histogram & self) -> double { return gsl_histogram_min_val(&self); },
        // the docstring
        "the smallest count in any of my bins");

    // the index of the bin holding the largest count
    cls.def(
        // the name
        "argmax",
        // the implementation
        [](const gsl_histogram & self) -> std::size_t { return gsl_histogram_max_bin(&self); },
        // the docstring
        "the index of the bin holding the largest count");

    // the index of the bin holding the smallest count
    cls.def(
        // the name
        "argmin",
        // the implementation
        [](const gsl_histogram & self) -> std::size_t { return gsl_histogram_min_bin(&self); },
        // the docstring
        "the index of the bin holding the smallest count");

    // copying
    // allocate an independent histogram with my bins and counts
    cls.def(
        // the name
        "clone",
        // the implementation
        [](const gsl_histogram & self) -> histogram_ptr {
            // gsl copies both the ranges and the counts into fresh storage
            return histogram_ptr(gsl_histogram_clone(&self));
        },
        // the docstring
        "allocate an independent histogram carrying my bins and counts");

    // make me an exact copy of {other}, which must have my shape
    cls.def(
        // the name
        "copy",
        // the implementation
        [](py::object self, const gsl_histogram & other) -> py::object {
            // gsl overwrites my ranges and counts with {other}'s
            gsl_histogram_memcpy(&self.cast<gsl_histogram &>(), &other);
            // and hand myself back, so callers can chain
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "make me an exact copy of {other}, which must have my shape, and return me");

    // elementwise combination, in place
    // add the counts of another histogram to mine, bin by bin
    cls.def(
        // the name
        "__iadd__",
        // the implementation
        [](py::object self, const gsl_histogram & other) -> py::object {
            // fold the other's counts into mine
            gsl_histogram_add(&self.cast<gsl_histogram &>(), &other);
            // and hand myself back
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "add the counts of {other} to mine, bin by bin");

    // shift every count by a constant
    cls.def(
        // the name
        "__iadd__",
        // the implementation
        [](py::object self, double offset) -> py::object {
            // raise every count by the offset
            gsl_histogram_shift(&self.cast<gsl_histogram &>(), offset);
            // and hand myself back
            return self;
        },
        // the signature
        "offset"_a,
        // the docstring
        "raise every one of my counts by {offset}");

    // subtract the counts of another histogram from mine, bin by bin
    cls.def(
        // the name
        "__isub__",
        // the implementation
        [](py::object self, const gsl_histogram & other) -> py::object {
            // take the other's counts out of mine
            gsl_histogram_sub(&self.cast<gsl_histogram &>(), &other);
            // and hand myself back
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "subtract the counts of {other} from mine, bin by bin");

    // lower every count by a constant
    cls.def(
        // the name
        "__isub__",
        // the implementation
        [](py::object self, double offset) -> py::object {
            // drop every count by the offset
            gsl_histogram_shift(&self.cast<gsl_histogram &>(), -offset);
            // and hand myself back
            return self;
        },
        // the signature
        "offset"_a,
        // the docstring
        "lower every one of my counts by {offset}");

    // multiply my counts by another histogram's, bin by bin
    cls.def(
        // the name
        "__imul__",
        // the implementation
        [](py::object self, const gsl_histogram & other) -> py::object {
            // scale my counts by the other's
            gsl_histogram_mul(&self.cast<gsl_histogram &>(), &other);
            // and hand myself back
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "multiply my counts by {other}'s, bin by bin");

    // scale every count by a constant
    cls.def(
        // the name
        "__imul__",
        // the implementation
        [](py::object self, double factor) -> py::object {
            // scale every count
            gsl_histogram_scale(&self.cast<gsl_histogram &>(), factor);
            // and hand myself back
            return self;
        },
        // the signature
        "factor"_a,
        // the docstring
        "scale every one of my counts by {factor}");

    // divide my counts by another histogram's, bin by bin
    cls.def(
        // the name
        "__itruediv__",
        // the implementation
        [](py::object self, const gsl_histogram & other) -> py::object {
            // divide my counts by the other's
            gsl_histogram_div(&self.cast<gsl_histogram &>(), &other);
            // and hand myself back
            return self;
        },
        // the signature
        "other"_a,
        // the docstring
        "divide my counts by {other}'s, bin by bin");

    // scale every count by the reciprocal of a constant
    cls.def(
        // the name
        "__itruediv__",
        // the implementation
        [](py::object self, double divisor) -> py::object {
            // scale every count by the reciprocal
            gsl_histogram_scale(&self.cast<gsl_histogram &>(), 1 / divisor);
            // and hand myself back
            return self;
        },
        // the signature
        "divisor"_a,
        // the docstring
        "divide every one of my counts by {divisor}");

    // container support
    // the number of bins, so that {len} works
    cls.def(
        // the name
        "__len__",
        // the implementation
        [](const gsl_histogram & self) -> std::size_t { return gsl_histogram_bins(&self); },
        // the docstring
        "the number of bins i hold");

    // the count in the {i}th bin
    cls.def(
        // the name
        "__getitem__",
        // the implementation
        [](const gsl_histogram & self, std::size_t i) -> double {
            // bounds check, so that out of range reads raise rather than read past the end
            if (i >= gsl_histogram_bins(&self)) {
                throw py::index_error("histogram bin index out of range");
            }
            // hand back the count
            return gsl_histogram_get(&self, i);
        },
        // the signature
        "i"_a,
        // the docstring
        "the count in the {i}th bin");

    // let numpy read my bin counts without copying them
    cls.def_buffer([](gsl_histogram & self) -> py::buffer_info {
        // describe the counts: a one dimensional, contiguous run of doubles, one per bin
        return py::buffer_info(
            // the payload
            self.bin,
            // the size of a cell, and how to spell it
            sizeof(double), py::format_descriptor<double>::format(),
            // the number of axes, and the extent of the one
            1, { self.n },
            // the distance in octets between neighbouring counts
            { sizeof(double) });
    });

    // all done
    return;
}


// end of file
