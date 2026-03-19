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
// MPI communicator capsule tag — must match the definition in the mpi extension
static constexpr const char * mpi_communicator_capsule = "mpi.communicator";


// helpers
static pyre::mpi::communicator_t *
get_communicator(::py::object comm_obj)
{
    PyObject * cap = comm_obj.ptr();
    if (!PyCapsule_IsValid(cap, mpi_communicator_capsule)) {
        throw std::invalid_argument("expected an mpi communicator capsule");
    }
    return static_cast<pyre::mpi::communicator_t *>(
        PyCapsule_GetPointer(cap, mpi_communicator_capsule));
}


namespace pyre::gsl::py {

void
partition(::py::module & m)
{
    // --- matrix ---

    m.def(
        "bcastMatrix",
        [](::py::object comm_obj, int source, pyre::gsl::Matrix & mat) {
            auto * comm = get_communicator(comm_obj);
            long dim[2];
            if (comm->rank() == source) {
                dim[0] = mat.ptr->size1;
                dim[1] = mat.ptr->size2;
            }
            MPI_Bcast(dim, 2, MPI_LONG, source, comm->handle());
            if (comm->rank() != source) {
                // reallocate to the broadcast shape if needed
                if (mat.ptr->size1 != (size_t)dim[0] || mat.ptr->size2 != (size_t)dim[1]) {
                    gsl_matrix_free(mat.ptr);
                    mat.ptr = gsl_matrix_alloc(dim[0], dim[1]);
                }
            }
            MPI_Bcast(mat.ptr->data, dim[0] * dim[1], MPI_DOUBLE, source, comm->handle());
        },
        "communicator"_a, "source"_a, "matrix"_a,
        "broadcast a matrix to all members of a communicator");

    m.def(
        "gatherMatrix",
        [](::py::object comm_obj, int destination, pyre::gsl::Matrix & mat)
            -> ::py::object {
            auto * comm = get_communicator(comm_obj);
            double * data = nullptr;
            gsl_matrix * bertha = nullptr;
            if (comm->rank() == destination) {
                size_t rows = mat.ptr->size1 * comm->size();
                size_t cols = mat.ptr->size2;
                bertha = gsl_matrix_alloc(rows, cols);
                data = bertha->data;
            }
            int size = mat.ptr->size1 * mat.ptr->size2;
            int status = MPI_Gather(
                mat.ptr->data, size, MPI_DOUBLE,
                data,          size, MPI_DOUBLE,
                destination, comm->handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Gather failed");
            }
            if (comm->rank() != destination) {
                return ::py::none();
            }
            return ::py::cast(std::make_unique<pyre::gsl::Matrix>(bertha, true));
        },
        "communicator"_a, "destination"_a, "matrix"_a,
        "gather a matrix from the members of a communicator");

    m.def(
        "scatterMatrix",
        [](::py::object comm_obj, int source,
           pyre::gsl::Matrix & src_mat, pyre::gsl::Matrix & dst_mat) {
            auto * comm = get_communicator(comm_obj);
            double * data = nullptr;
            if (comm->rank() == source) {
                data = src_mat.ptr->data;
            }
            int size = dst_mat.ptr->size1 * dst_mat.ptr->size2;
            int status = MPI_Scatter(
                data,             size, MPI_DOUBLE,
                dst_mat.ptr->data, size, MPI_DOUBLE,
                source, comm->handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Scatter failed");
            }
        },
        "communicator"_a, "source"_a, "matrix"_a, "destination"_a,
        "scatter a matrix to the members of a communicator");

    // --- vector ---

    m.def(
        "bcastVector",
        [](::py::object comm_obj, int source, pyre::gsl::Vector & vec) {
            auto * comm = get_communicator(comm_obj);
            long dim;
            if (comm->rank() == source) {
                dim = vec.ptr->size;
            }
            MPI_Bcast(&dim, 1, MPI_LONG, source, comm->handle());
            if (comm->rank() != source) {
                if (vec.ptr->size != (size_t)dim) {
                    gsl_vector_free(vec.ptr);
                    vec.ptr = gsl_vector_alloc(dim);
                }
            }
            MPI_Bcast(vec.ptr->data, dim, MPI_DOUBLE, source, comm->handle());
        },
        "communicator"_a, "source"_a, "vector"_a,
        "broadcast a vector to all members of a communicator");

    m.def(
        "gatherVector",
        [](::py::object comm_obj, int destination, pyre::gsl::Vector & vec)
            -> ::py::object {
            auto * comm = get_communicator(comm_obj);
            double * data = nullptr;
            gsl_vector * bertha = nullptr;
            if (comm->rank() == destination) {
                bertha = gsl_vector_alloc(vec.ptr->size * comm->size());
                data = bertha->data;
            }
            int status = MPI_Gather(
                vec.ptr->data, vec.ptr->size, MPI_DOUBLE,
                data,          vec.ptr->size, MPI_DOUBLE,
                destination, comm->handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Gather failed");
            }
            if (comm->rank() != destination) {
                return ::py::none();
            }
            return ::py::cast(std::make_unique<pyre::gsl::Vector>(bertha, true));
        },
        "communicator"_a, "destination"_a, "vector"_a,
        "gather a vector from the members of a communicator");

    m.def(
        "scatterVector",
        [](::py::object comm_obj, int source,
           pyre::gsl::Vector & src_vec, pyre::gsl::Vector & dst_vec) {
            auto * comm = get_communicator(comm_obj);
            double * data = nullptr;
            if (comm->rank() == source) {
                data = src_vec.ptr->data;
            }
            int length = dst_vec.ptr->size;
            int status = MPI_Scatter(
                data,             length, MPI_DOUBLE,
                dst_vec.ptr->data, length, MPI_DOUBLE,
                source, comm->handle());
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Scatter failed");
            }
        },
        "communicator"_a, "source"_a, "vector"_a, "destination"_a,
        "scatter a vector to the members of a communicator");
}

} // namespace pyre::gsl::py


// end of file
