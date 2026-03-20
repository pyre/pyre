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
group(::py::module & m)
{
    // register the Group type
    ::py::class_<pyre::mpi::Group>(m, "Group")
        // check whether the group is empty
        .def_property_readonly("isEmpty", &pyre::mpi::Group::isEmpty,
            "check whether this group is empty")
        // the number of processes in this group
        .def_property_readonly("size", &pyre::mpi::Group::size,
            "the number of processes in this group")
        // the rank of the calling process in this group
        .def_property_readonly("rank", &pyre::mpi::Group::rank,
            "the rank of this process in the group")

        // build a subgroup by including specific ranks
        .def("include", &pyre::mpi::Group::include, "ranks"_a,
            "build a subgroup by including specific ranks")

        // build a subgroup by excluding specific ranks
        .def("exclude", &pyre::mpi::Group::exclude, "ranks"_a,
            "build a subgroup by excluding specific ranks")

        // union of two groups
        .def(
            "__add__",
            [](const pyre::mpi::Group & self, const pyre::mpi::Group & other) {
                return pyre::mpi::groupUnion(self, other);
            },
            "build a group out of the union of two groups")

        // difference of two groups
        .def(
            "__sub__",
            [](const pyre::mpi::Group & self, const pyre::mpi::Group & other) {
                return pyre::mpi::groupDifference(self, other);
            },
            "build a group out of the difference of two groups")

        // intersection of two groups
        .def(
            "__and__",
            [](const pyre::mpi::Group & self, const pyre::mpi::Group & other) {
                return pyre::mpi::groupIntersection(self, other);
            },
            "build a group out of the intersection of two groups");
}

} // namespace pyre::mpi::py


// end of file
