// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

namespace pyre::gsl::py {

void
stats(::py::module & m)
{
    // Pearson correlation coefficient
    m.def(
        "stats_correlation",
        [](pyre::gsl::Vector & v1, pyre::gsl::Vector & v2) -> double {
            return gsl_stats_correlation(v1.ptr->data, 1, v2.ptr->data, 1, v1.ptr->size);
        },
        "v1"_a, "v2"_a,
        "compute the Pearson correlation coefficient between the two datasets");

    // covariance
    m.def(
        "stats_covariance",
        [](pyre::gsl::Vector & v1, pyre::gsl::Vector & v2) -> double {
            return gsl_stats_covariance(v1.ptr->data, 1, v2.ptr->data, 1, v1.ptr->size);
        },
        "v1"_a, "v2"_a,
        "compute the covariance of two datasets");

    // matrix mean along an axis
    m.def(
        "stats_matrix_mean",
        [](pyre::gsl::Matrix & mat, int axis, pyre::gsl::Vector & meanVec) {
            std::size_t rows = mat.ptr->size1;
            std::size_t cols = mat.ptr->size2;
            std::size_t tda  = mat.ptr->tda;
            double * datap   = mat.ptr->data;

            switch (axis) {
                case 0: // mean along rows -> one mean per column
                    for (std::size_t i = 0; i < cols; ++i) {
                        gsl_vector_set(meanVec.ptr, i,
                                       gsl_stats_mean(datap + i, tda, rows));
                    }
                    break;
                case 1: // mean along columns -> one mean per row
                    for (std::size_t i = 0; i < rows; ++i) {
                        gsl_vector_set(meanVec.ptr, i,
                                       gsl_stats_mean(datap + i * tda, 1, cols));
                    }
                    break;
                default: // mean of all elements
                    gsl_vector_set(meanVec.ptr, 0,
                                   gsl_stats_mean(datap, 1, rows * cols));
                    break;
            }
        },
        "matrix"_a, "axis"_a, "mean"_a,
        "compute the mean of the matrix elements along the given axis, updating mean in-place");

    // matrix mean and sample standard deviation along an axis
    m.def(
        "stats_matrix_mean_sd",
        [](pyre::gsl::Matrix & mat, int axis, pyre::gsl::Vector & meanVec, pyre::gsl::Vector & sdVec) {
            std::size_t rows = mat.ptr->size1;
            std::size_t cols = mat.ptr->size2;
            std::size_t tda  = mat.ptr->tda;
            double * datap   = mat.ptr->data;

            switch (axis) {
                case 0: // along rows -> per-column statistics
                    for (std::size_t i = 0; i < cols; ++i) {
                        double * colp = datap + i;
                        double mean = gsl_stats_mean(colp, tda, rows);
                        gsl_vector_set(meanVec.ptr, i, mean);
                        gsl_vector_set(sdVec.ptr,   i, gsl_stats_sd_m(colp, tda, rows, mean));
                    }
                    break;
                case 1: // along columns -> per-row statistics
                    for (std::size_t i = 0; i < rows; ++i) {
                        double * rowp = datap + i * tda;
                        double mean = gsl_stats_mean(rowp, 1, cols);
                        gsl_vector_set(meanVec.ptr, i, mean);
                        gsl_vector_set(sdVec.ptr,   i, gsl_stats_sd_m(rowp, 1, cols, mean));
                    }
                    break;
                default: // all elements
                    {
                        double mean = gsl_stats_mean(datap, 1, rows * cols);
                        gsl_vector_set(meanVec.ptr, 0, mean);
                        gsl_vector_set(sdVec.ptr,   0,
                                       gsl_stats_sd_m(datap, 1, rows * cols, mean));
                    }
                    break;
            }
        },
        "matrix"_a, "axis"_a, "mean"_a, "sd"_a,
        "compute the mean and sample standard deviation of matrix elements along the given axis");

    // matrix mean and population standard deviation along an axis
    m.def(
        "stats_matrix_mean_std",
        [](pyre::gsl::Matrix & mat, int axis, pyre::gsl::Vector & meanVec, pyre::gsl::Vector & sdVec) {
            std::size_t rows = mat.ptr->size1;
            std::size_t cols = mat.ptr->size2;
            std::size_t tda  = mat.ptr->tda;
            double * datap   = mat.ptr->data;

            switch (axis) {
                case 0: // along rows -> per-column statistics
                    for (std::size_t i = 0; i < cols; ++i) {
                        double * colp = datap + i;
                        double mean = gsl_stats_mean(colp, tda, rows);
                        gsl_vector_set(meanVec.ptr, i, mean);
                        gsl_vector_set(sdVec.ptr,   i,
                                       gsl_stats_sd_with_fixed_mean(colp, tda, rows, mean));
                    }
                    break;
                case 1: // along columns -> per-row statistics
                    for (std::size_t i = 0; i < rows; ++i) {
                        double * rowp = datap + i * tda;
                        double mean = gsl_stats_mean(rowp, 1, cols);
                        gsl_vector_set(meanVec.ptr, i, mean);
                        gsl_vector_set(sdVec.ptr,   i,
                                       gsl_stats_sd_with_fixed_mean(rowp, 1, cols, mean));
                    }
                    break;
                default: // all elements
                    {
                        double mean = gsl_stats_mean(datap, 1, rows * cols);
                        gsl_vector_set(meanVec.ptr, 0, mean);
                        gsl_vector_set(sdVec.ptr,   0,
                                       gsl_stats_sd_with_fixed_mean(datap, 1, rows * cols, mean));
                    }
                    break;
            }
        },
        "matrix"_a, "axis"_a, "mean"_a, "sd"_a,
        "compute the mean and population standard deviation of matrix elements along the given axis");
}

} // namespace pyre::gsl::py

// end of file
