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


    // bind the collectives that carry a cell of type {cellT} and name their operator explicitly
    template <typename cellT>
    inline auto bindCollectives(py::class_<Communicator> & cls) -> void
    {
        // combine the contributions of every process, delivering the answer to {root}
        cls.def(
            // the name
            "reduce",
            // the implementation
            [](const Communicator & self, cellT item, Op op, rank_t root) -> py::object {
                // room for the answer, and for my place in the communicator
                cellT answer;
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
            "item"_a, "op"_a, "root"_a = 0,
            // the docstring
            "combine the {item} of every process with {op}, delivering the answer to {root}");

        // the same, delivering the answer to everybody
        cls.def(
            // the name
            "allreduce",
            // the implementation
            [](const Communicator & self, cellT item, Op op) -> cellT {
                // combine, without holding the interpreter
                py::gil_scoped_release nogil;
                // and hand the answer to every process
                return self.allreduce(item, op);
            },
            // the signature
            "item"_a, "op"_a,
            // the docstring
            "combine the {item} of every process with {op}, delivering the answer to all");

        // the running combination over the processes that precede me
        cls.def(
            // the name
            "scan",
            // the implementation
            [](const Communicator & self, cellT item, Op op) -> cellT {
                // combine, without holding the interpreter
                py::gil_scoped_release nogil;
                // myself included
                return self.scan(item, op);
            },
            // the signature
            "item"_a, "op"_a,
            // the docstring
            "combine the {item} of every process that precedes me, myself included");

        cls.def(
            // the name
            "exscan",
            // the implementation
            [](const Communicator & self, cellT item, Op op) -> py::object {
                // room for the answer, and for my place in the communicator
                cellT answer;
                rank_t rank = 0;
                // combine, without holding the interpreter
                {
                    py::gil_scoped_release nogil;
                    answer = self.exscan(item, op);
                    rank = self.rank();
                }
                // the standard leaves the answer undefined at rank zero, where nothing precedes
                if (rank == 0) {
                    return py::none();
                }
                // everybody else has a real one
                return py::cast(answer);
            },
            // the signature
            "item"_a, "op"_a,
            // the docstring
            "combine the {item} of every process that strictly precedes me; {None} at rank zero, "
            "where the standard leaves the answer undefined");

        // collecting one cell from each process
        cls.def(
            // the name
            "gather",
            // the implementation
            [](const Communicator & self, cellT item, rank_t root) -> py::object {
                // room for the answer, and for my place in the communicator
                std::vector<cellT> answer;
                rank_t rank = 0;
                // collect, without holding the interpreter
                {
                    py::gil_scoped_release nogil;
                    answer = self.gather(item, root);
                    rank = self.rank();
                }
                // only {root} was handed anything
                if (rank != root) {
                    return py::none();
                }
                // so only {root} reports
                return py::cast(answer);
            },
            // the signature
            "item"_a, "root"_a = 0,
            // the docstring
            "collect the {item} of every process at {root}, in rank order");

        cls.def(
            // the name
            "allgather",
            // the implementation
            [](const Communicator & self, cellT item) -> std::vector<cellT> {
                // collect, without holding the interpreter
                py::gil_scoped_release nogil;
                // and hand the answer to every process
                return self.allgather(item);
            },
            // the signature
            "item"_a,
            // the docstring
            "collect the {item} of every process, in rank order, and deliver it to all");

        // handing one cell to each process
        cls.def(
            // the name
            "scatter",
            // the implementation
            [](const Communicator & self, const std::vector<cellT> & items, rank_t root) -> cellT {
                // hand them out, without holding the interpreter
                py::gil_scoped_release nogil;
                // each process receives the cell addressed to it
                return self.scatter(items, root);
            },
            // the signature
            "items"_a, "root"_a = 0,
            // the docstring
            "hand the nth cell of {items} to the nth process; only {root}'s {items} matters");

        cls.def(
            // the name
            "alltoall",
            // the implementation
            [](const Communicator & self, const std::vector<cellT> & items) -> std::vector<cellT> {
                // exchange, without holding the interpreter
                py::gil_scoped_release nogil;
                // every process hands one cell to every process
                return self.alltoall(items);
            },
            // the signature
            "items"_a,
            // the docstring
            "hand the nth cell of every process's {items} to the nth process");
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

    // the rest of the collective family, which names its operator rather than implying it; as
    // above, the integral overload of each goes first
    bindCollectives<integer_t>(cls);
    bindCollectives<real_t>(cls);

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

    cls.def(
        // the name
        "probe",
        // the implementation
        &Communicator::probe,
        // block without holding the interpreter, so that other threads may run
        py::call_guard<py::gil_scoped_release>(),
        // the signature
        "peer"_a = anySource, "tag"_a = anyTag,
        // the docstring
        "block until a matching message arrives, without receiving it, and report on it");

    cls.def(
        // the name
        "iprobe",
        // the implementation
        &Communicator::iprobe,
        // the signature
        "peer"_a = anySource, "tag"_a = anyTag,
        // the docstring
        "report on a matching message if one has already arrived, and hand back {None} if none "
        "has; this never blocks");

    // the nonblocking payload transfers. mpi reads and writes the buffer long after the call
    // that started the transfer has returned, so the buffer must outlive the receipt. the
    // {keep_alive} below says exactly that: python may not collect the buffer while the receipt
    // it handed back is still reachable
    cls.def(
        // the name
        "isendBytes",
        // the implementation
        [](const Communicator & self, const py::bytes & payload, rank_t peer,
           tag_t tag) -> Request {
            // point at the octets python is holding; a {bytes} object never moves them, and
            // never lets anybody change them
            char * data = nullptr;
            // and learn how many there are
            Py_ssize_t extent = 0;
            // ask python for both
            PyBytes_AsStringAndSize(payload.ptr(), &data, &extent);
            // start the transfer without holding the interpreter
            py::gil_scoped_release nogil;
            // and hand back the receipt
            return self.isendBytes(data, static_cast<size_type>(extent), peer, tag);
        },
        // the signature
        "payload"_a, "peer"_a, "tag"_a = 0,
        // tie the payload's life to the receipt's
        py::keep_alive<0, 2>(),
        // the docstring
        "start shipping a raw payload to {peer}, and hand back the receipt; the payload is kept "
        "alive for as long as the receipt is");

    cls.def(
        // the name
        "irecvBytes",
        // the implementation
        [](const Communicator & self, py::bytearray buffer, rank_t peer, tag_t tag) -> Request {
            // point at the octets python is holding
            char * data = PyByteArray_AsString(buffer.ptr());
            // and learn how many there are; the transfer fills exactly this many
            auto extent = PyByteArray_Size(buffer.ptr());
            // start the transfer without holding the interpreter
            py::gil_scoped_release nogil;
            // and hand back the receipt
            return self.irecvBytes(data, static_cast<size_type>(extent), peer, tag);
        },
        // the signature
        "buffer"_a, "peer"_a, "tag"_a = anyTag,
        // tie the buffer's life to the receipt's
        py::keep_alive<0, 2>(),
        // the docstring
        "start receiving a raw payload from {peer} into {buffer}, and hand back the receipt; the "
        "buffer is kept alive for as long as the receipt is, and must not be resized while the "
        "transfer is in flight");

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
