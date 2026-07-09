// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the process group
void
pyre::mpi::py::group(py::module & m)
{
    // the class
    auto cls = py::class_<Group>(
        // in scope
        m,
        // the name
        "Group",
        // the docstring
        "a set of processes, ordered so that each one has a rank within the set");

    // the structure
    cls.def_property_readonly(
        // the name
        "rank",
        // the implementation
        &Group::rank,
        // the docstring
        "the rank of this process within me, or {undefined} when it is not a member");

    cls.def_property_readonly(
        // the name
        "size",
        // the implementation
        &Group::size,
        // the docstring
        "the number of processes i hold");

    // whether i hold anybody
    cls.def(
        // the name
        "isEmpty",
        // the implementation
        &Group::isEmpty,
        // the docstring
        "check whether i have no members; note that this asks about membership, not about the "
        "identity of my handle");

    // whether i name a group at all
    cls.def(
        // the name
        "isNull",
        // the implementation
        &Group::isNull,
        // the docstring
        "check whether i name no group at all, as opposed to a group with no members");

    // the truth of a group is whether it names one
    cls.def(
        // the name
        "__bool__",
        // the implementation
        [](const Group & self) -> bool { return static_cast<bool>(self); },
        // the docstring
        "check whether i name a group");

    // building groups out of explicit rank lists
    cls.def(
        // the name
        "include",
        // the implementation
        &Group::include,
        // the signature
        "ranks"_a,
        // the docstring
        "build the group that holds exactly the processes named in {ranks}, in that order");

    cls.def(
        // the name
        "exclude",
        // the implementation
        &Group::exclude,
        // the signature
        "ranks"_a,
        // the docstring
        "build the group that holds all my members except those named in {ranks}");

    // the set operations, which the c++ layer expresses as free functions because neither
    // argument is privileged; python prefers to spell them as methods
    cls.def(
        // the name
        "union",
        // the implementation
        [](const Group & self, const Group & other) -> Group {
            return groupUnion(self, other);
        },
        // the signature
        "other"_a,
        // the docstring
        "build the group whose processes belong to either me or {other}");

    cls.def(
        // the name
        "intersection",
        // the implementation
        [](const Group & self, const Group & other) -> Group {
            return groupIntersection(self, other);
        },
        // the signature
        "other"_a,
        // the docstring
        "build the group whose processes belong to both me and {other}");

    cls.def(
        // the name
        "difference",
        // the implementation
        [](const Group & self, const Group & other) -> Group {
            return groupDifference(self, other);
        },
        // the signature
        "other"_a,
        // the docstring
        "build the group whose processes belong to me but not to {other}");

    // how my membership relates to another's
    cls.def(
        // the name
        "compare",
        // the implementation
        &Group::compare,
        // the signature
        "other"_a,
        // the docstring
        "describe how my membership relates to {other}'s");

    // where my members sit in another group
    cls.def(
        // the name
        "translateRanks",
        // the implementation
        &Group::translateRanks,
        // the signature
        "ranks"_a, "other"_a,
        // the docstring
        "the ranks that my members {ranks} carry in {other}; members that {other} does not hold "
        "come back as {undefined}");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Group & self) -> string_t {
            // a null group cannot answer questions about its membership
            if (self.isNull()) {
                return "<mpi.Group: null>";
            }
            // everybody else can
            return "<mpi.Group: rank " + std::to_string(self.rank()) + " of "
                 + std::to_string(self.size()) + ">";
        },
        // the docstring
        "a human readable summary of this group");

    // all done
    return;
}


// end of file
