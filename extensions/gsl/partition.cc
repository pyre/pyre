// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2026 all rights reserved


// pybind11 must be included before Python.h
#include "external.h"
// forward declarations
#include "forward.h"
// MPI and pyre mpi
#include <mpi.h>
#include <portinfo>
#include <pyre/mpi.h>


namespace pyre::gsl::py {

void
partition(::py::module & m)
{
    // --- matrix ---

    m.def(
        "bcastMatrix",
        [](pyre::mpi::Communicator & comm, int source, ::py::object mat_obj) -> ::py::object {
            long dim[2] = {0, 0};
            double * data_ptr = nullptr;
            ::py::object result_obj;
            // source fills dim and data_ptr from its matrix
            if (comm.rank() == source) {
                pyre::gsl::Matrix & src = mat_obj.cast<pyre::gsl::Matrix &>();
                dim[0] = src.ptr->size1;
                dim[1] = src.ptr->size2;
                data_ptr = src.ptr->data;
                result_obj = mat_obj;
            }
            // broadcast the shape to all ranks
            MPI_Bcast(dim, 2, MPI_LONG, source, comm.handle());
            // non-source ranks allocate a receive buffer
            if (comm.rank() != source) {
                auto mat = std::make_unique<pyre::gsl::Matrix>((size_t)dim[0], (size_t)dim[1]);
                data_ptr = mat->ptr->data;
                result_obj = ::py::cast(std::move(mat));
            }
            // single collective broadcast of the data
            MPI_Bcast(data_ptr, dim[0] * dim[1], MPI_DOUBLE, source, comm.handle());
            return ::py::make_tuple(result_obj, ::py::make_tuple((size_t)dim[0], (size_t)dim[1]));
        },
        "communicator"_a, "source"_a, "matrix"_a,
        "broadcast a matrix to all members of a communicator");

    m.def(
        "gatherMatrix",
        [](pyre::mpi::Communicator & comm, int destination, pyre::gsl::Matrix & mat)
            -> ::py::object {
            double * data = nullptr;
            gsl_matrix * bertha = nullptr;
            if (comm.rank() == destination) {
                size_t rows = mat.ptr->size1 * comm.size();
                size_t cols = mat.ptr->size2;
                bertha = gsl_matrix_alloc(rows, cols);
                data = bertha->data;
            }
            int size = mat.ptr->size1 * mat.ptr->size2;
            int status = MPI_Gather(
                mat.ptr->data, size, MPI_DOUBLE,
                data,          size, MPI_DOUBLE,
                destination, comm.handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Gather failed");
            }
            if (comm.rank() != destination) {
                return ::py::none();
            }
            auto shape = ::py::make_tuple(bertha->size1, bertha->size2);
            return ::py::make_tuple(
                ::py::cast(std::make_unique<pyre::gsl::Matrix>(bertha, true)), shape);
        },
        "communicator"_a, "destination"_a, "matrix"_a,
        "gather a matrix from the members of a communicator");

    m.def(
        "scatterMatrix",
        [](pyre::mpi::Communicator & comm, int source,
           pyre::gsl::Matrix & dst_mat, ::py::object src_obj) {
            double * data = nullptr;
            if (comm.rank() == source) {
                data = src_obj.cast<pyre::gsl::Matrix &>().ptr->data;
            }
            int size = dst_mat.ptr->size1 * dst_mat.ptr->size2;
            int status = MPI_Scatter(
                data,              size, MPI_DOUBLE, // send buffer
                dst_mat.ptr->data, size, MPI_DOUBLE, // receiver buffer
                source, comm.handle());              // rank of sender, communicator
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Scatter failed");
            }
        },
        "communicator"_a, "source"_a, "destination"_a, "matrix"_a,
        "scatter a matrix to the members of a communicator");

    // --- vector ---

    m.def(
        "bcastVector",
        [](pyre::mpi::Communicator & comm, int source, ::py::object vec_obj) -> ::py::object {
            long dim = 0;
            double * data_ptr = nullptr;
            ::py::object result_obj;
            // source fills dim and data_ptr from its vector
            if (comm.rank() == source) {
                pyre::gsl::Vector & src = vec_obj.cast<pyre::gsl::Vector &>();
                dim = src.ptr->size;
                data_ptr = src.ptr->data;
                result_obj = vec_obj;
            }
            // broadcast the size to all ranks
            MPI_Bcast(&dim, 1, MPI_LONG, source, comm.handle());
            // non-source ranks allocate a receive buffer
            if (comm.rank() != source) {
                auto vec = std::make_unique<pyre::gsl::Vector>((size_t)dim);
                data_ptr = vec->ptr->data;
                result_obj = ::py::cast(std::move(vec));
            }
            // single collective broadcast of the data
            MPI_Bcast(data_ptr, dim, MPI_DOUBLE, source, comm.handle());
            return ::py::make_tuple(result_obj, (size_t)dim);
        },
        "communicator"_a, "source"_a, "vector"_a,
        "broadcast a vector to all members of a communicator");

    m.def(
        "gatherVector",
        [](pyre::mpi::Communicator & comm, int destination, pyre::gsl::Vector & vec)
            -> ::py::object {
            double * data = nullptr;
            gsl_vector * bertha = nullptr;
            if (comm.rank() == destination) {
                bertha = gsl_vector_alloc(vec.ptr->size * comm.size());
                data = bertha->data;
            }
            int status = MPI_Gather(
                vec.ptr->data, vec.ptr->size, MPI_DOUBLE,
                data,          vec.ptr->size, MPI_DOUBLE,
                destination, comm.handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Gather failed");
            }
            if (comm.rank() != destination) {
                return ::py::none();
            }
            size_t sz = bertha->size;
            return ::py::make_tuple(
                ::py::cast(std::make_unique<pyre::gsl::Vector>(bertha, true)), sz);
        },
        "communicator"_a, "destination"_a, "vector"_a,
        "gather a vector from the members of a communicator");

    m.def(
        "scatterVector",
        [](pyre::mpi::Communicator & comm, int source,
           pyre::gsl::Vector & dst_vec, ::py::object src_obj) {
            double * data = nullptr;
            if (comm.rank() == source) {
                data = src_obj.cast<pyre::gsl::Vector &>().ptr->data;
            }
            int length = dst_vec.ptr->size;
            int status = MPI_Scatter(
                data,              length, MPI_DOUBLE,
                dst_vec.ptr->data, length, MPI_DOUBLE,
                source, comm.handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Scatter failed");
            }
        },
        "communicator"_a, "source"_a, "destination"_a, "vector"_a,
        "scatter a vector to the members of a communicator");
}

} // namespace pyre::gsl::py


// end of file
