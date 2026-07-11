// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the distributions
#include <gsl/gsl_randist.h>
// the cumulative distributions and their inverses
#include <gsl/gsl_cdf.h>


// the local helpers
namespace gsl::py {
    // the support of the uniform distribution, as it crosses from python
    using support_t = std::pair<double, double>;

    // fill {v} by drawing from {draw}, a nullary callable that returns a double
    template <typename drawT>
    inline auto fillVector(gsl_vector & v, drawT draw) -> void
    {
        // one draw per cell
        for (std::size_t i = 0; i < v.size; ++i) {
            // deposit it, honouring the stride
            gsl_vector_set(&v, i, draw());
        }
    }

    // fill {m} by drawing from {draw}, a nullary callable that returns a double
    template <typename drawT>
    inline auto fillMatrix(gsl_matrix & m, drawT draw) -> void
    {
        // one draw per cell
        for (std::size_t i = 0; i < m.size1; ++i) {
            for (std::size_t j = 0; j < m.size2; ++j) {
                // deposit it, honouring the layout
                gsl_matrix_set(&m, i, j, draw());
            }
        }
    }

    // the cdf values that bracket a gaussian of {mean},{sigma} on {support}; these normalize the
    // truncated distribution and drive its inverse-cdf sampling
    inline auto truncation(double mean, double sigma, support_t support) -> support_t
    {
        // unpack the interval
        auto [a, b] = support;
        // a nonpositive width or an empty interval has no distribution
        if (sigma <= 0 || b <= a) {
            throw py::value_error(
                "the truncated gaussian needs sigma > 0 and a support (a, b) with a < b");
        }
        // the cdf at each endpoint, measured from the mean
        auto pa = gsl_cdf_gaussian_P(a - mean, sigma);
        auto pb = gsl_cdf_gaussian_P(b - mean, sigma);
        // guard the far-tail case where both endpoints round to the same probability
        if (pb <= pa) {
            throw py::value_error(
                "the truncated gaussian support lies too far in the tail to represent");
        }
        // hand back the bracketing probabilities
        return { pa, pb };
    }
} // namespace gsl::py


// add the bindings for the gsl probability distributions
void
gsl::py::pdf(py::module & m)
{
    // the uniform distribution over an interval
    // a single sample
    m.def(
        // the name
        "uniform_sample",
        // the implementation
        [](support_t support, gsl_rng & rng) -> double {
            // draw uniformly from the interval
            return gsl_ran_flat(&rng, support.first, support.second);
        },
        // the signature
        "support"_a, "rng"_a,
        // the docstring
        "draw a sample from the uniform distribution over {support}");

    // the density at a point
    m.def(
        // the name
        "uniform_density",
        // the implementation
        [](support_t support, double x) -> double {
            // the flat density
            return gsl_ran_flat_pdf(x, support.first, support.second);
        },
        // the signature
        "support"_a, "x"_a,
        // the docstring
        "the density of the uniform distribution over {support} at {x}");

    // fill a vector with samples
    m.def(
        // the name
        "uniform_vector",
        // the implementation
        [](support_t support, gsl_rng & rng, gsl_vector & v) -> void {
            // one uniform draw per cell
            fillVector(v, [&] { return gsl_ran_flat(&rng, support.first, support.second); });
        },
        // the signature
        "support"_a, "rng"_a, "vector"_a,
        // the docstring
        "fill {vector} with samples from the uniform distribution over {support}");

    // fill a matrix with samples
    m.def(
        // the name
        "uniform_matrix",
        // the implementation
        [](support_t support, gsl_rng & rng, gsl_matrix & mat) -> void {
            // one uniform draw per cell
            fillMatrix(mat, [&] { return gsl_ran_flat(&rng, support.first, support.second); });
        },
        // the signature
        "support"_a, "rng"_a, "matrix"_a,
        // the docstring
        "fill {matrix} with samples from the uniform distribution over {support}");

    // the uniform distribution over the open unit interval
    // a single sample
    m.def(
        // the name
        "uniform_pos_sample",
        // the implementation
        [](gsl_rng & rng) -> double { return gsl_rng_uniform_pos(&rng); },
        // the signature
        "rng"_a,
        // the docstring
        "draw a sample from the uniform distribution over (0, 1)");

    // fill a vector with samples
    m.def(
        // the name
        "uniform_pos_vector",
        // the implementation
        [](gsl_rng & rng, gsl_vector & v) -> void {
            // one positive uniform draw per cell
            fillVector(v, [&] { return gsl_rng_uniform_pos(&rng); });
        },
        // the signature
        "rng"_a, "vector"_a,
        // the docstring
        "fill {vector} with samples from the uniform distribution over (0, 1)");

    // fill a matrix with samples
    m.def(
        // the name
        "uniform_pos_matrix",
        // the implementation
        [](gsl_rng & rng, gsl_matrix & mat) -> void {
            // one positive uniform draw per cell
            fillMatrix(mat, [&] { return gsl_rng_uniform_pos(&rng); });
        },
        // the signature
        "rng"_a, "matrix"_a,
        // the docstring
        "fill {matrix} with samples from the uniform distribution over (0, 1)");

    // the gaussian distribution of a given mean and width
    // a single sample
    m.def(
        // the name
        "gaussian_sample",
        // the implementation
        [](double mean, double sigma, gsl_rng & rng) -> double {
            // a draw about zero, shifted to the mean
            return mean + gsl_ran_gaussian(&rng, sigma);
        },
        // the signature
        "mean"_a, "sigma"_a, "rng"_a,
        // the docstring
        "draw a sample from the gaussian of the given {mean} and {sigma}");

    // the density at a point
    m.def(
        // the name
        "gaussian_density",
        // the implementation
        [](double mean, double sigma, double x) -> double {
            // the gaussian density, measured from the mean
            return gsl_ran_gaussian_pdf(x - mean, sigma);
        },
        // the signature
        "mean"_a, "sigma"_a, "x"_a,
        // the docstring
        "the density of the gaussian of the given {mean} and {sigma} at {x}");

    // fill a vector with samples
    m.def(
        // the name
        "gaussian_vector",
        // the implementation
        [](double mean, double sigma, gsl_rng & rng, gsl_vector & v) -> void {
            // one gaussian draw per cell, shifted to the mean
            fillVector(v, [&] { return mean + gsl_ran_gaussian(&rng, sigma); });
        },
        // the signature
        "mean"_a, "sigma"_a, "rng"_a, "vector"_a,
        // the docstring
        "fill {vector} with samples from the gaussian of the given {mean} and {sigma}");

    // fill a matrix with samples
    m.def(
        // the name
        "gaussian_matrix",
        // the implementation
        [](double mean, double sigma, gsl_rng & rng, gsl_matrix & mat) -> void {
            // one gaussian draw per cell, shifted to the mean
            fillMatrix(mat, [&] { return mean + gsl_ran_gaussian(&rng, sigma); });
        },
        // the signature
        "mean"_a, "sigma"_a, "rng"_a, "matrix"_a,
        // the docstring
        "fill {matrix} with samples from the gaussian of the given {mean} and {sigma}");

    // the unit gaussian, of zero mean and unit width
    // a single sample
    m.def(
        // the name
        "ugaussian_sample",
        // the implementation
        [](gsl_rng & rng) -> double { return gsl_ran_ugaussian(&rng); },
        // the signature
        "rng"_a,
        // the docstring
        "draw a sample from the unit gaussian");

    // the density at a point
    m.def(
        // the name
        "ugaussian_density",
        // the implementation
        [](double x) -> double { return gsl_ran_ugaussian_pdf(x); },
        // the signature
        "x"_a,
        // the docstring
        "the density of the unit gaussian at {x}");

    // fill a vector with samples
    m.def(
        // the name
        "ugaussian_vector",
        // the implementation
        [](gsl_rng & rng, gsl_vector & v) -> void {
            // one unit gaussian draw per cell
            fillVector(v, [&] { return gsl_ran_ugaussian(&rng); });
        },
        // the signature
        "rng"_a, "vector"_a,
        // the docstring
        "fill {vector} with samples from the unit gaussian");

    // fill a matrix with samples
    m.def(
        // the name
        "ugaussian_matrix",
        // the implementation
        [](gsl_rng & rng, gsl_matrix & mat) -> void {
            // one unit gaussian draw per cell
            fillMatrix(mat, [&] { return gsl_ran_ugaussian(&rng); });
        },
        // the signature
        "rng"_a, "matrix"_a,
        // the docstring
        "fill {matrix} with samples from the unit gaussian");

    // the gaussian of a given mean and width, truncated to the interval {support}
    // a single sample, drawn by inverting the cdf between the bracketing probabilities
    m.def(
        // the name
        "tgaussian_sample",
        // the implementation
        [](double mean, double sigma, support_t support, gsl_rng & rng) -> double {
            // the probabilities that bracket the support
            auto [pa, pb] = truncation(mean, sigma, support);
            // draw uniformly between them
            auto u = pa + gsl_rng_uniform(&rng) * (pb - pa);
            // invert the cdf, shifting back to the mean
            return mean + gsl_cdf_gaussian_Pinv(u, sigma);
        },
        // the signature
        "mean"_a, "sigma"_a, "support"_a, "rng"_a,
        // the docstring
        "draw a sample from the gaussian of {mean} and {sigma}, truncated to {support}");

    // the density at a point
    m.def(
        // the name
        "tgaussian_density",
        // the implementation
        [](double mean, double sigma, support_t support, double x) -> double {
            // the probabilities that bracket the support; also validates the parameters
            auto [pa, pb] = truncation(mean, sigma, support);
            // no mass outside the support
            if (x < support.first || x > support.second) {
                return 0.0;
            }
            // the gaussian density renormalized by the mass the truncation retains
            return gsl_ran_gaussian_pdf(x - mean, sigma) / (pb - pa);
        },
        // the signature
        "mean"_a, "sigma"_a, "support"_a, "x"_a,
        // the docstring
        "the density at {x} of the gaussian of {mean} and {sigma}, truncated to {support}");

    // fill a vector with samples
    m.def(
        // the name
        "tgaussian_vector",
        // the implementation
        [](double mean, double sigma, support_t support, gsl_rng & rng, gsl_vector & v) -> void {
            // the probabilities that bracket the support, as plain locals the fill lambda captures
            auto brackets = truncation(mean, sigma, support);
            auto pa = brackets.first, pb = brackets.second;
            // one truncated draw per cell, by inverting the cdf between the brackets
            fillVector(v, [&] {
                auto u = pa + gsl_rng_uniform(&rng) * (pb - pa);
                return mean + gsl_cdf_gaussian_Pinv(u, sigma);
            });
        },
        // the signature
        "mean"_a, "sigma"_a, "support"_a, "rng"_a, "vector"_a,
        // the docstring
        "fill {vector} with samples from the gaussian of {mean} and {sigma}, truncated to {support}");

    // fill a matrix with samples
    m.def(
        // the name
        "tgaussian_matrix",
        // the implementation
        [](double mean, double sigma, support_t support, gsl_rng & rng, gsl_matrix & mat) -> void {
            // the probabilities that bracket the support, as plain locals the fill lambda captures
            auto brackets = truncation(mean, sigma, support);
            auto pa = brackets.first, pb = brackets.second;
            // one truncated draw per cell, by inverting the cdf between the brackets
            fillMatrix(mat, [&] {
                auto u = pa + gsl_rng_uniform(&rng) * (pb - pa);
                return mean + gsl_cdf_gaussian_Pinv(u, sigma);
            });
        },
        // the signature
        "mean"_a, "sigma"_a, "support"_a, "rng"_a, "matrix"_a,
        // the docstring
        "fill {matrix} with samples from the gaussian of {mean} and {sigma}, truncated to {support}");

    // the dirichlet distribution, parameterized by the concentration vector {alpha}
    // fill a vector with a single draw
    m.def(
        // the name
        "dirichlet_vector",
        // the implementation
        [](gsl_rng & rng, const gsl_vector & alpha, gsl_vector & v) -> void {
            // a dirichlet draw is a whole vector, one weight per concentration
            gsl_ran_dirichlet(&rng, alpha.size, alpha.data, v.data);
        },
        // the signature
        "rng"_a, "alpha"_a, "vector"_a,
        // the docstring
        "fill {vector} with a draw from the dirichlet distribution of concentration {alpha}");

    // fill each row of a matrix with a draw
    m.def(
        // the name
        "dirichlet_matrix",
        // the implementation
        [](gsl_rng & rng, const gsl_vector & alpha, gsl_matrix & mat) -> void {
            // the concentration sets the width of each draw
            std::size_t K = alpha.size;
            // one draw per row
            for (std::size_t i = 0; i < mat.size1; ++i) {
                // deposited across the row, honouring the layout
                gsl_ran_dirichlet(&rng, K, alpha.data, mat.data + i * mat.tda);
            }
        },
        // the signature
        "rng"_a, "alpha"_a, "matrix"_a,
        // the docstring
        "fill each row of {matrix} with a draw from the dirichlet distribution of {alpha}");

    // all done
    return;
}


// end of file
