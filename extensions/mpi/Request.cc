// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the helpers that let the collective waits reach the receipts a python list holds
namespace pyre::mpi::py {
    // move the receipts out of {requests} and into a vector the c++ layer can work on
    //
    // a receipt is not copyable, since exactly one owner is entitled to complete it. so the
    // python objects surrender theirs for the duration of the wait, and take them back when it
    // is over, whereupon the ones that completed are empty and the ones still in flight are not
    inline auto claim(const py::list & requests) -> std::vector<Request *>
    {
        // room for the answers
        std::vector<Request *> owners;
        // make room
        owners.reserve(requests.size());
        // reach into each element
        for (auto handle : requests) {
            // and remember where its receipt lives
            owners.push_back(handle.cast<Request *>());
        }
        // hand them off
        return owners;
    }
} // namespace pyre::mpi::py


// add the bindings for the receipt of a transfer that is still in flight
void
pyre::mpi::py::request(py::module & m)
{
    // the class; a receipt cannot be built from python, since only a transfer makes one
    auto cls = py::class_<Request>(
        // in scope
        m,
        // the name
        "Request",
        // the docstring
        "the receipt of a message transfer that is still in flight");

    // whether the transfer is still pending
    cls.def_property_readonly(
        // the name
        "active",
        // the implementation
        &Request::active,
        // the docstring
        "whether i still name a transfer that has not completed");

    cls.def(
        // the name
        "__bool__",
        // the implementation
        [](const Request & self) -> bool { return static_cast<bool>(self); },
        // the docstring
        "check whether i name a transfer");

    // completing it
    cls.def(
        // the name
        "wait",
        // the implementation
        &Request::wait,
        // block without holding the interpreter, so that other threads may run
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "block until my transfer completes, and report on it");

    cls.def(
        // the name
        "test",
        // the implementation
        &Request::test,
        // the docstring
        "check whether my transfer has completed, without blocking; hand back its report if it "
        "has, and {None} if it has not");

    cls.def(
        // the name
        "cancel",
        // the implementation
        &Request::cancel,
        // the docstring
        "ask mpi to abandon my transfer; it must still be completed, since mpi only promises "
        "that a cancelled transfer finishes one way or the other");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Request & self) -> string_t {
            return self.active() ? "<mpi.Request: in flight>" : "<mpi.Request: complete>";
        },
        // the docstring
        "a human readable summary of this receipt");

    // waiting on many transfers at once
    m.def(
        // the name
        "waitAll",
        // the implementation
        [](const py::list & requests) -> std::vector<Status> {
            // find the receipts
            auto owners = claim(requests);
            // and take them
            std::vector<Request> pending;
            // make room
            pending.reserve(owners.size());
            // one by one
            for (auto owner : owners) {
                pending.push_back(std::move(*owner));
            }

            // room for the reports
            std::vector<Status> reports;
            // block, without holding the interpreter
            {
                py::gil_scoped_release nogil;
                reports = pyre::mpi::waitAll(pending);
            }

            // give the receipts back, now that they are all spent
            for (decltype(owners.size()) slot = 0; slot < owners.size(); ++slot) {
                *owners[slot] = std::move(pending[slot]);
            }

            // hand off the reports
            return reports;
        },
        // the signature
        "requests"_a,
        // the docstring
        "block until every one of {requests} completes, and report on each");

    m.def(
        // the name
        "waitAny",
        // the implementation
        [](const py::list & requests) -> std::pair<int, Status> {
            // find the receipts
            auto owners = claim(requests);
            // and take them
            std::vector<Request> pending;
            // make room
            pending.reserve(owners.size());
            // one by one
            for (auto owner : owners) {
                pending.push_back(std::move(*owner));
            }

            // room for the answer
            std::pair<int, Status> outcome;
            // block, without holding the interpreter
            {
                py::gil_scoped_release nogil;
                outcome = pyre::mpi::waitAny(pending);
            }

            // give the receipts back; the one that completed is now empty, and the rest are
            // still in flight
            for (decltype(owners.size()) slot = 0; slot < owners.size(); ++slot) {
                *owners[slot] = std::move(pending[slot]);
            }

            // hand off which one finished, and how
            return outcome;
        },
        // the signature
        "requests"_a,
        // the docstring
        "block until one of {requests} completes, and report which, along with its outcome; the "
        "others are left in flight, and the index is {undefined} when none was");

    // all done
    return;
}


// end of file
