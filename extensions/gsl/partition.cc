// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the mpi c api, the pyre mpi communicator, and the gsl entities we shuffle
#include <mpi.h>
#include <pyre/mpi.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>


// the local helpers
namespace gsl::py {
    // the communicator every partitioning call takes as its first argument
    using communicator_t = pyre::mpi::Communicator;
} // namespace gsl::py


// add the bindings for the gsl mpi partitioning
void
gsl::py::partition(py::module & m)
{
    // vector operations
    // broadcast a vector from {source} to every process in the communicator
    //
    // only {source} has to supply a {vector}; it hands its own back, and every other process
    // receives a freshly allocated one carrying the same values
    m.def(
        // the name
        "bcastVector",
        // the implementation
        [](const communicator_t & comm, int source, py::object vector) -> py::object {
            // the source knows the shape; it announces it to everybody
            long dim = 0;
            if (comm.rank() == source) {
                dim = vector.cast<gsl_vector &>().size;
            }
            MPI_Bcast(&dim, 1, MPI_LONG, source, comm.handle());
            // the source broadcasts from its own storage; everybody else into fresh storage
            gsl_vector * v =
                (comm.rank() == source) ? &vector.cast<gsl_vector &>() : gsl_vector_alloc(dim);
            // move the payload
            int status = MPI_Bcast(v->data, dim, MPI_DOUBLE, source, comm.handle());
            // complain if it failed
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Bcast failed");
            }
            // the source hands its own vector back; everybody else adopts the fresh one
            if (comm.rank() == source) {
                return vector;
            }
            return py::cast(v, py::return_value_policy::take_ownership);
        },
        // the signature
        "communicator"_a, "source"_a, "vector"_a,
        // the docstring
        "broadcast {vector} from {source} to every process in {communicator}");

    // gather the vectors of every process into one big vector at {destination}
    m.def(
        // the name
        "gatherVector",
        // the implementation
        [](const communicator_t & comm, int destination, gsl_vector & vector) -> py::object {
            // the destination allocates room for every process's contribution
            gsl_vector * bertha = nullptr;
            double * data = nullptr;
            if (comm.rank() == destination) {
                bertha = gsl_vector_alloc(vector.size * comm.size());
                data = bertha->data;
            }
            // gather the contributions in rank order
            int status = MPI_Gather(
                vector.data, vector.size, MPI_DOUBLE, data, vector.size, MPI_DOUBLE, destination,
                comm.handle());
            // complain if it failed
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Gather failed");
            }
            // everybody but the destination has nothing to show for it
            if (comm.rank() != destination) {
                return py::none();
            }
            // the destination adopts the big vector
            return py::cast(bertha, py::return_value_policy::take_ownership);
        },
        // the signature
        "communicator"_a, "destination"_a, "vector"_a,
        // the docstring
        "gather the vectors of every process into one at {destination}");

    // scatter the vector held by {source} among all processes, filling each one's {destination}
    m.def(
        // the name
        "scatterVector",
        // the implementation
        [](const communicator_t & comm, int source, gsl_vector & destination,
           py::object vector) -> void {
            // only the source reads from a whole vector
            double * data = (comm.rank() == source) ? vector.cast<gsl_vector &>().data : nullptr;
            // hand each process its slice
            int status = MPI_Scatter(
                data, destination.size, MPI_DOUBLE, destination.data, destination.size, MPI_DOUBLE,
                source, comm.handle());
            // complain if it failed
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Scatter failed");
            }
        },
        // the signature
        "communicator"_a, "source"_a, "destination"_a, "vector"_a,
        // the docstring
        "scatter the vector held by {source} among all processes, filling each {destination}");

    // matrix operations
    // broadcast a matrix from {source} to every process in the communicator
    m.def(
        // the name
        "bcastMatrix",
        // the implementation
        [](const communicator_t & comm, int source, py::object matrix) -> py::object {
            // the source knows the shape; it announces both dimensions to everybody
            long dim[2] = { 0, 0 };
            if (comm.rank() == source) {
                gsl_matrix & mat = matrix.cast<gsl_matrix &>();
                dim[0] = mat.size1;
                dim[1] = mat.size2;
            }
            MPI_Bcast(dim, 2, MPI_LONG, source, comm.handle());
            // the source broadcasts from its own storage; everybody else into fresh storage
            gsl_matrix * mat = (comm.rank() == source) ? &matrix.cast<gsl_matrix &>()
                                                       : gsl_matrix_alloc(dim[0], dim[1]);
            // move the payload
            int status = MPI_Bcast(mat->data, dim[0] * dim[1], MPI_DOUBLE, source, comm.handle());
            // complain if it failed
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Bcast failed");
            }
            // the source hands its own matrix back; everybody else adopts the fresh one
            if (comm.rank() == source) {
                return matrix;
            }
            return py::cast(mat, py::return_value_policy::take_ownership);
        },
        // the signature
        "communicator"_a, "source"_a, "matrix"_a,
        // the docstring
        "broadcast {matrix} from {source} to every process in {communicator}");

    // gather the matrices of every process into one tall matrix at {destination}
    m.def(
        // the name
        "gatherMatrix",
        // the implementation
        [](const communicator_t & comm, int destination, gsl_matrix & matrix) -> py::object {
            // the destination allocates room for every process's contribution, stacked by row
            gsl_matrix * bertha = nullptr;
            double * data = nullptr;
            if (comm.rank() == destination) {
                bertha = gsl_matrix_alloc(matrix.size1 * comm.size(), matrix.size2);
                data = bertha->data;
            }
            // the count of cells each process contributes
            int cells = matrix.size1 * matrix.size2;
            // gather the contributions in rank order
            int status = MPI_Gather(
                matrix.data, cells, MPI_DOUBLE, data, cells, MPI_DOUBLE, destination,
                comm.handle());
            // complain if it failed
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Gather failed");
            }
            // everybody but the destination has nothing to show for it
            if (comm.rank() != destination) {
                return py::none();
            }
            // the destination adopts the tall matrix
            return py::cast(bertha, py::return_value_policy::take_ownership);
        },
        // the signature
        "communicator"_a, "destination"_a, "matrix"_a,
        // the docstring
        "gather the matrices of every process into one at {destination}");

    // scatter the matrix held by {source} among all processes, filling each one's {destination}
    m.def(
        // the name
        "scatterMatrix",
        // the implementation
        [](const communicator_t & comm, int source, gsl_matrix & destination,
           py::object matrix) -> void {
            // only the source reads from a whole matrix
            double * data = (comm.rank() == source) ? matrix.cast<gsl_matrix &>().data : nullptr;
            // the count of cells each process receives
            int cells = destination.size1 * destination.size2;
            // hand each process its block of rows
            int status = MPI_Scatter(
                data, cells, MPI_DOUBLE, destination.data, cells, MPI_DOUBLE, source,
                comm.handle());
            // complain if it failed
            if (status != MPI_SUCCESS) {
                throw std::runtime_error("MPI_Scatter failed");
            }
        },
        // the signature
        "communicator"_a, "source"_a, "destination"_a, "matrix"_a,
        // the docstring
        "scatter the matrix held by {source} among all processes, filling each {destination}");

    // all done
    return;
}


// end of file
