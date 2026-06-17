// -*- c++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2026 all rights reserved
//

// externals
#include "external.h"


namespace pyre::mpi::py {

void
communicator(::py::module & m)
{
    // register the Communicator type
    ::py::class_<pyre::mpi::Communicator>(m, "Communicator")
        // the number of processes in this communicator
        .def_property_readonly("size", &pyre::mpi::Communicator::size,
            "the number of processes in this communicator")
        // the rank of the calling process
        .def_property_readonly("rank", &pyre::mpi::Communicator::rank,
            "the rank of this process in the communicator")

        // barrier
        .def("barrier", &pyre::mpi::Communicator::barrier,
            "block until all members of this communicator reach this point")

        // broadcast a bytes object to all tasks
        .def(
            "bcast",
            [](pyre::mpi::Communicator & self, int root, ::py::bytes data) {
                int rank = self.rank();
                std::string buf = data.cast<std::string>();
                int size = static_cast<int>(buf.size());
                // broadcast the length
                MPI_Bcast(&size, 1, MPI_INT, root, self.handle());
                // non-root processes need a buffer of the right size
                if (rank != root) {
                    buf.resize(size);
                }
                // broadcast the data
                MPI_Bcast(buf.data(), size, MPI_BYTE, root, self.handle());
                return ::py::bytes(buf.data(), size);
            },
            "root"_a, "data"_a,
            "broadcast a python bytes object to all tasks")

        // sum reduction to root
        .def(
            "sum",
            [](pyre::mpi::Communicator & self, int root, double number) -> ::py::object {
                double total;
                MPI_Reduce(&number, &total, 1, MPI_DOUBLE, MPI_SUM, root, self.handle());
                if (self.rank() == root) return ::py::float_(total);
                return ::py::none();
            },
            "root"_a, "number"_a, "perform a sum reduction")

        // product reduction to root
        .def(
            "product",
            [](pyre::mpi::Communicator & self, int root, double number) -> ::py::object {
                double result = 0;
                MPI_Reduce(&number, &result, 1, MPI_DOUBLE, MPI_PROD, root, self.handle());
                if (self.rank() == root) return ::py::float_(result);
                return ::py::none();
            },
            "root"_a, "number"_a, "perform a product reduction")

        // max reduction to root
        .def(
            "max",
            [](pyre::mpi::Communicator & self, int root, double number) -> ::py::object {
                double result = 0;
                MPI_Reduce(&number, &result, 1, MPI_DOUBLE, MPI_MAX, root, self.handle());
                if (self.rank() == root) return ::py::float_(result);
                return ::py::none();
            },
            "root"_a, "number"_a, "perform a max reduction")

        // min reduction to root
        .def(
            "min",
            [](pyre::mpi::Communicator & self, int root, double number) -> ::py::object {
                double result = 0;
                MPI_Reduce(&number, &result, 1, MPI_DOUBLE, MPI_MIN, root, self.handle());
                if (self.rank() == root) return ::py::float_(result);
                return ::py::none();
            },
            "root"_a, "number"_a, "perform a min reduction")

        // sum allreduce
        .def(
            "sum_all",
            [](pyre::mpi::Communicator & self, double number) {
                double total;
                MPI_Allreduce(&number, &total, 1, MPI_DOUBLE, MPI_SUM, self.handle());
                return total;
            },
            "number"_a,
            "perform a sum reduction and distribute the result to all processes")

        // product allreduce
        .def(
            "product_all",
            [](pyre::mpi::Communicator & self, double number) {
                double result = 0;
                MPI_Allreduce(&number, &result, 1, MPI_DOUBLE, MPI_PROD, self.handle());
                return result;
            },
            "number"_a,
            "perform a product reduction and distribute the result to all processes")

        // max allreduce
        .def(
            "max_all",
            [](pyre::mpi::Communicator & self, double number) {
                double result = 0;
                MPI_Allreduce(&number, &result, 1, MPI_DOUBLE, MPI_MAX, self.handle());
                return result;
            },
            "number"_a,
            "perform a max reduction and distribute the result to all processes")

        // min allreduce
        .def(
            "min_all",
            [](pyre::mpi::Communicator & self, double number) {
                double result = 0;
                MPI_Allreduce(&number, &result, 1, MPI_DOUBLE, MPI_MIN, self.handle());
                return result;
            },
            "number"_a,
            "perform a min reduction and distribute the result to all processes")

        // create a new communicator from a group
        .def(
            "create",
            [](pyre::mpi::Communicator & self, pyre::mpi::Group & group) -> ::py::object {
                auto comm = self.communicator(group);
                if (comm.isNull()) return ::py::none();
                return ::py::cast(comm);
            },
            "group"_a, "create a new communicator from a group")

        // extract the group from this communicator
        .def("group", &pyre::mpi::Communicator::group,
            "extract the group from this communicator")

        // create a cartesian communicator
        .def("cartesian", &pyre::mpi::Communicator::cartesian,
            "procs"_a, "periods"_a, "reorder"_a,
            "create a Cartesian communicator")

        // retrieve cartesian coordinates of a process
        .def("coordinates", &pyre::mpi::Communicator::coordinates,
            "rank"_a, "retrieve the Cartesian coordinates of a process");

    // backward-compatible module-level aliases
    m.def("communicatorRank", &pyre::mpi::Communicator::rank,
        "comm"_a, "return the rank of this process in the given communicator");
    m.def("communicatorSize", &pyre::mpi::Communicator::size,
        "comm"_a, "return the number of processes in the given communicator");
}

} // namespace pyre::mpi::py


// end of file
