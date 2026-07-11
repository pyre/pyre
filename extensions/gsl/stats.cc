// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the statistics
#include <gsl/gsl_statistics.h>
// an absent axis means "the whole matrix"
#include <optional>


// the local helpers
namespace gsl::py {
    // which spread, if any, to compute alongside the mean
    enum class spread_t {
        // just the mean
        none,
        // the sample standard deviation, dividing by N-1
        sample,
        // the population standard deviation, dividing by N about the fixed mean
        population
    };

    // compute the mean of a matrix, optionally with its spread, along {axis}
    //
    // {axis} 0 walks down each column, {axis} 1 across each row, and anything else folds the
    // whole matrix into a single number. the answers are written into {mean} and, when a spread
    // is asked for, {sd}, which the caller has sized to match
    inline auto matrixStats(
        const gsl_matrix & m, int axis, gsl_vector & mean, gsl_vector * sd, spread_t spread) -> void
    {
        // the shape of the matrix, and the stride between its rows
        const std::size_t rows = m.size1, cols = m.size2, tda = m.tda;
        // a running pointer into the payload
        const double * datap = m.data;

        // pick the recipe for the spread of a run of {n} cells, {stride} apart, about {mu}
        auto spreadOf =
            [spread](const double * p, std::size_t stride, std::size_t n, double mu) -> double {
            // the sample standard deviation divides by N-1
            if (spread == spread_t::sample) {
                return gsl_stats_sd_m(p, stride, n, mu);
            }
            // the population standard deviation divides by N about the fixed mean
            return gsl_stats_sd_with_fixed_mean(p, stride, n, mu);
        };

        // along the columns
        if (axis == 0) {
            // one answer per column
            for (std::size_t i = 0; i < cols; ++i, ++datap) {
                // the column is {rows} cells, one row-stride apart
                double mu = gsl_stats_mean(datap, tda, rows);
                // record it
                gsl_vector_set(&mean, i, mu);
                // and its spread, if asked for
                if (sd) {
                    gsl_vector_set(sd, i, spreadOf(datap, tda, rows, mu));
                }
            }
            // all done
            return;
        }

        // along the rows
        if (axis == 1) {
            // one answer per row
            for (std::size_t i = 0; i < rows; ++i, datap += tda) {
                // the row is {cols} contiguous cells
                double mu = gsl_stats_mean(datap, 1, cols);
                // record it
                gsl_vector_set(&mean, i, mu);
                // and its spread, if asked for
                if (sd) {
                    gsl_vector_set(sd, i, spreadOf(datap, 1, cols, mu));
                }
            }
            // all done
            return;
        }

        // otherwise, the whole matrix folds into one number, which reads its cells as a single
        // contiguous run and so needs the rows to be tightly packed
        if (tda != cols) {
            throw py::value_error("the whole-matrix mean requires a contiguous matrix");
        }
        // the lone mean over every cell
        double mu = gsl_stats_mean(datap, 1, rows * cols);
        // recorded in the first slot
        gsl_vector_set(&mean, 0, mu);
        // with its spread, if asked for
        if (sd) {
            gsl_vector_set(sd, 0, spreadOf(datap, 1, rows * cols, mu));
        }
        // all done
        return;
    }
} // namespace gsl::py


// add the bindings for the gsl statistics
void
gsl::py::stats(py::module & m)
{
    // the Pearson correlation coefficient of two datasets
    m.def(
        // the name
        "stats_correlation",
        // the implementation
        [](const gsl_vector & x, const gsl_vector & y) -> double {
            // gsl walks each dataset with unit stride
            return gsl_stats_correlation(x.data, 1, y.data, 1, x.size);
        },
        // the signature
        "x"_a, "y"_a,
        // the docstring
        "the Pearson correlation coefficient of {x} and {y}");

    // the covariance of two datasets
    m.def(
        // the name
        "stats_covariance",
        // the implementation
        [](const gsl_vector & x, const gsl_vector & y) -> double {
            // gsl walks each dataset with unit stride
            return gsl_stats_covariance(x.data, 1, y.data, 1, x.size);
        },
        // the signature
        "x"_a, "y"_a,
        // the docstring
        "the covariance of {x} and {y}");

    // the mean of a matrix along an axis
    m.def(
        // the name
        "stats_matrix_mean",
        // the implementation
        [](const gsl_matrix & source, std::optional<int> axis, gsl_vector & mean) -> void {
            // no spread, just the mean; an absent axis folds the whole matrix
            matrixStats(source, axis.value_or(-1), mean, nullptr, spread_t::none);
        },
        // the signature
        "matrix"_a, "axis"_a, "mean"_a,
        // the docstring
        "fill {mean} with the mean of {matrix} along {axis}");

    // the mean and sample standard deviation of a matrix along an axis
    m.def(
        // the name
        "stats_matrix_mean_sd",
        // the implementation
        [](const gsl_matrix & source, std::optional<int> axis, gsl_vector & mean,
           gsl_vector & sd) -> void {
            // the sample spread divides by N-1; an absent axis folds the whole matrix
            matrixStats(source, axis.value_or(-1), mean, &sd, spread_t::sample);
        },
        // the signature
        "matrix"_a, "axis"_a, "mean"_a, "sd"_a,
        // the docstring
        "fill {mean} and {sd} with the mean and sample standard deviation of {matrix} along "
        "{axis}");

    // the mean and population standard deviation of a matrix along an axis
    m.def(
        // the name
        "stats_matrix_mean_std",
        // the implementation
        [](const gsl_matrix & source, std::optional<int> axis, gsl_vector & mean,
           gsl_vector & sd) -> void {
            // the population spread divides by N; an absent axis folds the whole matrix
            matrixStats(source, axis.value_or(-1), mean, &sd, spread_t::population);
        },
        // the signature
        "matrix"_a, "axis"_a, "mean"_a, "sd"_a,
        // the docstring
        "fill {mean} and {sd} with the mean and population standard deviation of {matrix} along "
        "{axis}");

    // all done
    return;
}


// end of file
