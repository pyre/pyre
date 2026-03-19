// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

namespace pyre::gsl::py {

void
pdf(::py::module & m)
{
    // uniform distribution
    m.def(
        "uniform_sample",
        [](pyre::gsl::RNG & r, std::tuple<double, double> support) -> double {
            auto [a, b] = support;
            return gsl_ran_flat(r.ptr, a, b);
        },
        "rng"_a, "support"_a,
        "return a sample from the uniform distribution on [a, b)");

    m.def(
        "uniform_density",
        [](std::tuple<double, double> support, double x) -> double {
            auto [a, b] = support;
            return gsl_ran_flat_pdf(x, a, b);
        },
        "support"_a, "x"_a,
        "evaluate the uniform distribution pdf at x");

    m.def(
        "uniform_vector",
        [](pyre::gsl::Vector & v, pyre::gsl::RNG & r, std::tuple<double, double> support) {
            auto [a, b] = support;
            for (std::size_t i = 0; i < v.ptr->size; ++i) {
                gsl_vector_set(v.ptr, i, gsl_ran_flat(r.ptr, a, b));
            }
        },
        "vector"_a, "rng"_a, "support"_a,
        "fill a vector with samples from the uniform distribution on [a, b)");

    m.def(
        "uniform_matrix",
        [](pyre::gsl::Matrix & mat, pyre::gsl::RNG & r, std::tuple<double, double> support) {
            auto [a, b] = support;
            for (std::size_t i = 0; i < mat.ptr->size1; ++i) {
                for (std::size_t j = 0; j < mat.ptr->size2; ++j) {
                    gsl_matrix_set(mat.ptr, i, j, gsl_ran_flat(r.ptr, a, b));
                }
            }
        },
        "matrix"_a, "rng"_a, "support"_a,
        "fill a matrix with samples from the uniform distribution on [a, b)");

    // uniform_pos distribution
    m.def(
        "uniform_pos_sample",
        [](pyre::gsl::RNG & r, std::tuple<double, double> support) -> double {
            auto [a, b] = support;
            return gsl_ran_flat(r.ptr, a, b);
        },
        "rng"_a, "support"_a,
        "return a sample from the positive uniform distribution on [a, b)");

    m.def(
        "uniform_pos_vector",
        [](pyre::gsl::Vector & v, pyre::gsl::RNG & r, std::tuple<double, double> support) {
            auto [a, b] = support;
            for (std::size_t i = 0; i < v.ptr->size; ++i) {
                gsl_vector_set(v.ptr, i, gsl_ran_flat(r.ptr, a, b));
            }
        },
        "vector"_a, "rng"_a, "support"_a,
        "fill a vector with samples from the positive uniform distribution on [a, b)");

    m.def(
        "uniform_pos_matrix",
        [](pyre::gsl::Matrix & mat, pyre::gsl::RNG & r, std::tuple<double, double> support) {
            auto [a, b] = support;
            for (std::size_t i = 0; i < mat.ptr->size1; ++i) {
                for (std::size_t j = 0; j < mat.ptr->size2; ++j) {
                    gsl_matrix_set(mat.ptr, i, j, gsl_ran_flat(r.ptr, a, b));
                }
            }
        },
        "matrix"_a, "rng"_a, "support"_a,
        "fill a matrix with samples from the positive uniform distribution on [a, b)");

    // gaussian distribution
    m.def(
        "gaussian_sample",
        [](pyre::gsl::RNG & r, double mean, double sigma) -> double {
            return mean + gsl_ran_gaussian(r.ptr, sigma);
        },
        "rng"_a, "mean"_a, "sigma"_a,
        "return a sample from the gaussian distribution with the given mean and sigma");

    m.def(
        "gaussian_density",
        [](double mean, double sigma, double x) -> double {
            return gsl_ran_gaussian_pdf(x - mean, sigma);
        },
        "mean"_a, "sigma"_a, "x"_a,
        "evaluate the gaussian pdf at x for the given mean and sigma");

    m.def(
        "gaussian_vector",
        [](pyre::gsl::Vector & v, pyre::gsl::RNG & r, double mean, double sigma) {
            for (std::size_t i = 0; i < v.ptr->size; ++i) {
                gsl_vector_set(v.ptr, i, mean + gsl_ran_gaussian(r.ptr, sigma));
            }
        },
        "vector"_a, "rng"_a, "mean"_a, "sigma"_a,
        "fill a vector with gaussian samples with the given mean and sigma");

    m.def(
        "gaussian_matrix",
        [](pyre::gsl::Matrix & mat, pyre::gsl::RNG & r, double mean, double sigma) {
            for (std::size_t i = 0; i < mat.ptr->size1; ++i) {
                for (std::size_t j = 0; j < mat.ptr->size2; ++j) {
                    gsl_matrix_set(mat.ptr, i, j, mean + gsl_ran_gaussian(r.ptr, sigma));
                }
            }
        },
        "matrix"_a, "rng"_a, "mean"_a, "sigma"_a,
        "fill a matrix with gaussian samples with the given mean and sigma");

    // unit gaussian distribution
    m.def(
        "ugaussian_sample",
        [](pyre::gsl::RNG & r, double mean) -> double {
            return mean + gsl_ran_ugaussian(r.ptr);
        },
        "rng"_a, "mean"_a,
        "return a sample from the unit gaussian distribution with the given mean");

    m.def(
        "ugaussian_density",
        [](double mean, double x) -> double {
            return gsl_ran_ugaussian_pdf(x - mean);
        },
        "mean"_a, "x"_a,
        "evaluate the unit gaussian pdf at x for the given mean");

    m.def(
        "ugaussian_vector",
        [](pyre::gsl::Vector & v, pyre::gsl::RNG & r, double mean) {
            for (std::size_t i = 0; i < v.ptr->size; ++i) {
                gsl_vector_set(v.ptr, i, mean + gsl_ran_ugaussian(r.ptr));
            }
        },
        "vector"_a, "rng"_a, "mean"_a,
        "fill a vector with unit gaussian samples with the given mean");

    m.def(
        "ugaussian_matrix",
        [](pyre::gsl::Matrix & mat, pyre::gsl::RNG & r, double mean) {
            for (std::size_t i = 0; i < mat.ptr->size1; ++i) {
                for (std::size_t j = 0; j < mat.ptr->size2; ++j) {
                    gsl_matrix_set(mat.ptr, i, j, mean + gsl_ran_ugaussian(r.ptr));
                }
            }
        },
        "matrix"_a, "rng"_a, "mean"_a,
        "fill a matrix with unit gaussian samples with the given mean");

    // truncated gaussian distribution: support [a, b]
    // sampling via inverse-CDF; PDF normalised by (CDF(b) - CDF(a))
    m.def(
        "tgaussian_sample",
        [](pyre::gsl::RNG & r, double mean, double sigma, std::tuple<double, double> support) -> double {
            auto [a, b] = support;
            double pa = gsl_cdf_gaussian_P(a - mean, sigma);
            double pb = gsl_cdf_gaussian_P(b - mean, sigma);
            double u  = pa + gsl_rng_uniform(r.ptr) * (pb - pa);
            return mean + gsl_cdf_gaussian_Pinv(u, sigma);
        },
        "rng"_a, "mean"_a, "sigma"_a, "support"_a,
        "return a sample from the truncated gaussian on [a, b)");

    m.def(
        "tgaussian_density",
        [](double mean, double sigma, std::tuple<double, double> support, double x) -> double {
            auto [a, b] = support;
            if (x < a || x > b) return 0.0;
            double pa = gsl_cdf_gaussian_P(a - mean, sigma);
            double pb = gsl_cdf_gaussian_P(b - mean, sigma);
            return gsl_ran_gaussian_pdf(x - mean, sigma) / (pb - pa);
        },
        "mean"_a, "sigma"_a, "support"_a, "x"_a,
        "evaluate the truncated gaussian pdf at x");

    m.def(
        "tgaussian_vector",
        [](pyre::gsl::Vector & v, pyre::gsl::RNG & r, double mean, double sigma,
           std::tuple<double, double> support) {
            auto [a, b] = support;
            double pa = gsl_cdf_gaussian_P(a - mean, sigma);
            double pb = gsl_cdf_gaussian_P(b - mean, sigma);
            for (std::size_t i = 0; i < v.ptr->size; ++i) {
                double u = pa + gsl_rng_uniform(r.ptr) * (pb - pa);
                gsl_vector_set(v.ptr, i, mean + gsl_cdf_gaussian_Pinv(u, sigma));
            }
        },
        "vector"_a, "rng"_a, "mean"_a, "sigma"_a, "support"_a,
        "fill a vector with samples from the truncated gaussian on [a, b)");

    m.def(
        "tgaussian_matrix",
        [](pyre::gsl::Matrix & mat, pyre::gsl::RNG & r, double mean, double sigma,
           std::tuple<double, double> support) {
            auto [a, b] = support;
            double pa = gsl_cdf_gaussian_P(a - mean, sigma);
            double pb = gsl_cdf_gaussian_P(b - mean, sigma);
            for (std::size_t i = 0; i < mat.ptr->size1; ++i) {
                for (std::size_t j = 0; j < mat.ptr->size2; ++j) {
                    double u = pa + gsl_rng_uniform(r.ptr) * (pb - pa);
                    gsl_matrix_set(mat.ptr, i, j, mean + gsl_cdf_gaussian_Pinv(u, sigma));
                }
            }
        },
        "matrix"_a, "rng"_a, "mean"_a, "sigma"_a, "support"_a,
        "fill a matrix with samples from the truncated gaussian on [a, b)");

    // dirichlet distribution
    m.def(
        "dirichlet_sample",
        [](pyre::gsl::RNG & r, pyre::gsl::Vector & alpha, pyre::gsl::Vector & theta) {
            gsl_ran_dirichlet(r.ptr, alpha.ptr->size, alpha.ptr->data, theta.ptr->data);
        },
        "rng"_a, "alpha"_a, "theta"_a,
        "draw a dirichlet sample into theta given concentration parameters alpha");

    m.def(
        "dirichlet_density",
        [](pyre::gsl::Vector & alpha, pyre::gsl::Vector & theta) -> double {
            return gsl_ran_dirichlet_pdf(alpha.ptr->size, alpha.ptr->data, theta.ptr->data);
        },
        "alpha"_a, "theta"_a,
        "evaluate the dirichlet pdf for the given alpha and theta");

    m.def(
        "dirichlet_vector",
        [](pyre::gsl::Vector & theta, pyre::gsl::RNG & r, pyre::gsl::Vector & alpha) {
            gsl_ran_dirichlet(r.ptr, alpha.ptr->size, alpha.ptr->data, theta.ptr->data);
        },
        "theta"_a, "rng"_a, "alpha"_a,
        "draw a dirichlet sample into theta vector given concentration parameters alpha");

    m.def(
        "dirichlet_matrix",
        [](pyre::gsl::Matrix & mat, pyre::gsl::RNG & r, pyre::gsl::Vector & alpha) {
            std::size_t K = alpha.ptr->size;
            for (std::size_t i = 0; i < mat.ptr->size1; ++i) {
                gsl_vector_view row = gsl_matrix_row(mat.ptr, i);
                gsl_ran_dirichlet(r.ptr, K, alpha.ptr->data, row.vector.data);
            }
        },
        "matrix"_a, "rng"_a, "alpha"_a,
        "fill each row of matrix with a dirichlet sample given concentration parameters alpha");
}

} // namespace pyre::gsl::py

// end of file
