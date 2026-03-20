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
ports(::py::module & m)
{
    // send bytes to a peer
    m.def(
        "sendBytes",
        [](pyre::mpi::Communicator & comm, int peer, int tag, ::py::bytes data) {
            std::string buf = data.cast<std::string>();
            pyre::journal::debug_t info("mpi.ports");
            info << pyre::journal::at(__HERE__)
                 << "peer={" << peer << "}, tag={" << tag << "}, bytes={"
                 << buf.size() << "}" << pyre::journal::endl;
            MPI_Send(buf.data(), static_cast<int>(buf.size()), MPI_BYTE,
                     peer, tag, comm.handle());
        },
        "comm"_a, "peer"_a, "tag"_a, "data"_a,
        "send bytes to a peer");

    // receive bytes from a peer
    m.def(
        "recvBytes",
        [](pyre::mpi::Communicator & comm, int peer, int tag) {
            MPI_Status status;
            MPI_Probe(peer, tag, comm.handle(), &status);
            int len;
            MPI_Get_count(&status, MPI_BYTE, &len);
            std::vector<char> buf(len);
            MPI_Recv(buf.data(), len, MPI_BYTE, peer, tag, comm.handle(), &status);
            pyre::journal::debug_t info("mpi.ports");
            info << pyre::journal::at(__HERE__)
                 << "peer={" << peer << "}, tag={" << tag << "}, bytes={"
                 << len << "}" << pyre::journal::endl;
            return ::py::bytes(buf.data(), len);
        },
        "comm"_a, "peer"_a, "tag"_a,
        "receive bytes from a peer");

    // send a string to a peer (including null terminator)
    m.def(
        "sendString",
        [](pyre::mpi::Communicator & comm, int peer, int tag, const std::string & str) {
            pyre::journal::debug_t info("mpi.ports");
            info << pyre::journal::at(__HERE__)
                 << "peer={" << peer << "}, tag={" << tag << "}, string={"
                 << str << "}" << pyre::journal::endl;
            MPI_Send(str.c_str(), static_cast<int>(str.size()) + 1,
                     MPI_CHAR, peer, tag, comm.handle());
        },
        "comm"_a, "peer"_a, "tag"_a, "str"_a,
        "send a string to a peer");

    // receive a string from a peer
    m.def(
        "recvString",
        [](pyre::mpi::Communicator & comm, int peer, int tag) {
            MPI_Status status;
            MPI_Probe(peer, tag, comm.handle(), &status);
            int len;
            MPI_Get_count(&status, MPI_CHAR, &len);
            std::vector<char> buf(len);
            MPI_Recv(buf.data(), len, MPI_CHAR, peer, tag, comm.handle(), &status);
            pyre::journal::debug_t info("mpi.ports");
            info << pyre::journal::at(__HERE__)
                 << "peer={" << peer << "}, tag={" << tag << "}, string={"
                 << buf.data() << "}" << pyre::journal::endl;
            return std::string(buf.data());
        },
        "comm"_a, "peer"_a, "tag"_a,
        "receive a string from a peer");
}

} // namespace pyre::mpi::py


// end of file
