// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the bridge between python payloads and the buffers mpi moves
#include "utilities.h"


// the helpers that bind the reduction family
namespace pyre::mpi::py {
    // bind one reduction under {name}, for cells of type {cellT}
    //
    // a reduction that names a {destination} delivers its answer to that rank alone and hands
    // everybody else {None}; one that names none delivers to all
    template <typename cellT>
    inline auto bindReduction(
        py::class_<Communicator> & cls, classname_t name, Op op, docstring_t doc) -> void
    {
        // add the binding
        cls.def(
            // the name
            name,
            // the implementation
            [op](const Communicator & self, cellT item,
                 std::optional<rank_t> destination) -> py::object {
                // when nobody is named, everybody gets the answer
                if (!destination) {
                    // room for it
                    cellT answer;
                    // combine, without holding the interpreter
                    {
                        py::gil_scoped_release nogil;
                        answer = self.allreduce(item, op);
                    }
                    // and hand it to this process
                    return py::cast(answer);
                }

                // otherwise, exactly one rank collects
                auto root = *destination;
                // room for the answer
                cellT answer;
                // and for my place in the communicator
                rank_t rank = 0;
                // combine, without holding the interpreter
                {
                    py::gil_scoped_release nogil;
                    answer = self.reduce(item, op, root);
                    rank = self.rank();
                }
                // everybody but {root} was handed a value that means nothing
                if (rank != root) {
                    return py::none();
                }
                // so only {root} reports one
                return py::cast(answer);
            },
            // the signature
            "item"_a, "destination"_a = py::none(),
            // the docstring
            doc);
    }
} // namespace pyre::mpi::py


// add the bindings for the communicator
void
pyre::mpi::py::communicator(py::module & m)
{
    // the class
    auto cls = py::class_<Communicator>(
        // in scope
        m,
        // the name
        "Communicator",
        // the docstring
        "a group of processes, together with the context that isolates their messages");

    // the structure
    cls.def_property_readonly(
        // the name
        "rank",
        // the implementation
        &Communicator::rank,
        // the docstring
        "the rank of this process within me");

    cls.def_property_readonly(
        // the name
        "size",
        // the implementation
        &Communicator::size,
        // the docstring
        "the number of processes i hold");

    cls.def(
        // the name
        "isNull",
        // the implementation
        &Communicator::isNull,
        // the docstring
        "check whether i name no communicator at all");

    cls.def(
        // the name
        "__bool__",
        // the implementation
        [](const Communicator & self) -> bool { return static_cast<bool>(self); },
        // the docstring
        "check whether i name a communicator");

    cls.def(
        // the name
        "group",
        // the implementation
        &Communicator::group,
        // the docstring
        "the set of processes i hold");

    cls.def(
        // the name
        "compare",
        // the implementation
        &Communicator::compare,
        // the signature
        "other"_a,
        // the docstring
        "describe how my membership and context relate to {other}'s");

    // communicator factories
    cls.def(
        // the name
        "restrict",
        // the implementation
        [](const Communicator & self, const Group & group) -> py::object {
            // build it; this is collective over me, so every one of my processes must call
            auto restricted = self.communicator(group);
            // the processes that {group} left out have nothing to work with
            if (restricted.isNull()) {
                // so tell them so
                return py::none();
            }
            // everybody else gets a real communicator
            return py::cast(restricted);
        },
        // the signature
        "group"_a,
        // the docstring
        "build the communicator that holds exactly the processes of {group}; collective over "
        "me, and {None} for the processes that {group} leaves out");

    cls.def(
        // the name
        "include",
        // the implementation
        [](const Communicator & self, const ranks_t & ranks) -> py::object {
            // carve the group out of mine, then build its communicator
            auto restricted = self.communicator(self.group().include(ranks));
            // the processes left out have nothing to work with
            if (restricted.isNull()) {
                return py::none();
            }
            // everybody else gets a real communicator
            return py::cast(restricted);
        },
        // the signature
        "ranks"_a,
        // the docstring
        "build the communicator that holds exactly the processes named in {ranks}");

    cls.def(
        // the name
        "exclude",
        // the implementation
        [](const Communicator & self, const ranks_t & ranks) -> py::object {
            // carve the group out of mine, then build its communicator
            auto restricted = self.communicator(self.group().exclude(ranks));
            // the processes left out have nothing to work with
            if (restricted.isNull()) {
                return py::none();
            }
            // everybody else gets a real communicator
            return py::cast(restricted);
        },
        // the signature
        "ranks"_a,
        // the docstring
        "build the communicator that holds all my processes except those named in {ranks}");

    cls.def(
        // the name
        "split",
        // the implementation
        [](const Communicator & self, int color, int key) -> py::object {
            // split; this is collective over me
            auto piece = self.split(color, key);
            // a process that offered {undefined} as its color asked to be left out
            if (piece.isNull()) {
                return py::none();
            }
            // everybody else lands in the communicator of its color
            return py::cast(piece);
        },
        // the signature
        "color"_a, "key"_a = 0,
        // the docstring
        "split me into one communicator per distinct {color}, ranking each by {key}; a process "
        "that offers {undefined} as its color is left out, and gets {None}");

    cls.def(
        // the name
        "duplicate",
        // the implementation
        &Communicator::duplicate,
        // the docstring
        "build a communicator with my membership but a fresh context");

    cls.def(
        // the name
        "cartesian",
        // the implementation
        [](const Communicator & self, const shape_t & axes, const shape_t & periods,
           int reorder) -> Cartesian {
            // lay my processes out on the grid; this is collective over me
            return self.cartesian(axes, periods, reorder);
        },
        // the signature
        "axes"_a, "periods"_a, "reorder"_a = 1,
        // the docstring
        "arrange my processes on a grid of the given shape, wrapping the axes flagged in "
        "{periods}, and letting mpi renumber them when {reorder} is set");

    // the conduit factory
    cls.def(
        // the name
        "port",
        // the implementation
        &Communicator::port,
        // the signature
        "peer"_a, "tag"_a = 0,
        // the docstring
        "establish a point to point conduit with {peer}; every message that goes through it "
        "carries {tag}");

    // collective operations
    cls.def(
        // the name
        "barrier",
        // the implementation
        &Communicator::barrier,
        // block without holding the interpreter, so that other threads may run
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "block until every one of my processes arrives here");

    cls.def(
        // the name
        "bcast",
        // the implementation
        [](const Communicator & self, const py::object & item, rank_t source) -> py::object {
            // room for the payload
            bytes_t payload;
            // only the source has anything to say, so only it does the flattening
            if (self.rank() == source) {
                payload = pickle(item);
            }
            // move the payload, without holding the interpreter; this overload carries the
            // extent along with the octets, so the other ranks need not know it beforehand
            {
                py::gil_scoped_release nogil;
                self.bcast(payload, source);
            }
            // and everybody rebuilds what the source flattened
            return unpickle(payload);
        },
        // the signature
        "item"_a = py::none(), "source"_a = 0,
        // the docstring
        "broadcast {item} from {source} to every one of my processes; only {source} has to "
        "supply an {item}");

    // the reductions; the integral overload of each is registered first, so that a reduction
    // of whole numbers hands back a whole number
    bindReduction<integer_t>(cls, "sum", Op::sum, "perform a sum reduction");
    bindReduction<real_t>(cls, "sum", Op::sum, "perform a sum reduction");
    bindReduction<integer_t>(cls, "product", Op::product, "perform a product reduction");
    bindReduction<real_t>(cls, "product", Op::product, "perform a product reduction");
    bindReduction<integer_t>(cls, "max", Op::maximum, "perform a max reduction");
    bindReduction<real_t>(cls, "max", Op::maximum, "perform a max reduction");
    bindReduction<integer_t>(cls, "min", Op::minimum, "perform a min reduction");
    bindReduction<real_t>(cls, "min", Op::minimum, "perform a min reduction");

    // point to point operations, in their raw form; the conduit above is the pleasant face
    cls.def(
        // the name
        "sendBytes",
        // the implementation
        [](const Communicator & self, const py::bytes & payload, rank_t peer, tag_t tag) -> void {
            // reinterpret the octets while we still hold the interpreter
            auto buffer = asBytes(payload);
            // and ship them without holding it
            py::gil_scoped_release nogil;
            // hand them to {peer}
            self.sendBytes(buffer, peer, tag);
            // all done
            return;
        },
        // the signature
        "payload"_a, "peer"_a, "tag"_a = 0,
        // the docstring
        "ship a raw payload to {peer}");

    cls.def(
        // the name
        "recvBytes",
        // the implementation
        [](const Communicator & self, rank_t peer, tag_t tag) -> py::bytes {
            // room for what arrives
            bytes_t payload;
            // take the message without holding the interpreter, since this blocks
            {
                py::gil_scoped_release nogil;
                payload = self.recvBytes(peer, tag);
            }
            // and hand the octets to python
            return asPython(payload);
        },
        // the signature
        "peer"_a, "tag"_a = anyTag,
        // the docstring
        "block until a raw payload arrives from {peer}, and hand back exactly what came");

    // process control
    cls.def(
        // the name
        "abort",
        // the implementation
        &Communicator::abort,
        // the signature
        "code"_a = 1,
        // the docstring
        "bring down every process i hold, handing {code} to the environment");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Communicator & self) -> string_t {
            // a null communicator cannot answer questions about its membership
            if (self.isNull()) {
                return "<mpi.Communicator: null>";
            }
            // everybody else can
            return "<mpi.Communicator: rank " + std::to_string(self.rank()) + " of "
                 + std::to_string(self.size()) + ">";
        },
        // the docstring
        "a human readable summary of this communicator");

    // all done
    return;
}


// end of file
