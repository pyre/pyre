// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>
// other packages
#include <cassert>
#include <numeric>
// grab the mpi objects
#include <pyre/mpi.h>


// exercise the collective family, each of which deduces its datatype from the cells it is
// handed
int
main()
{
    // bring mpi up
    pyre::mpi::initialize();

    // push down a scope so our handles die before mpi does
    {
        // the communicator that holds the whole job
        auto world = pyre::mpi::world();
        // its size
        auto size = world.size();
        // and my rank in it
        auto rank = world.rank();
        // the sum of every rank, which several of the checks below lean on
        auto total = size * (size - 1) / 2;

        // a reduction over whole numbers stays whole all the way through
        auto sum = world.reduce(rank, pyre::mpi::Op::sum, 0);
        // only the root receives the answer
        if (rank == 0) {
            assert(sum == total);
        }

        // the same reduction, delivered to everybody
        assert(world.allreduce(rank, pyre::mpi::Op::sum) == total);
        // and the extrema
        assert(world.allreduce(rank, pyre::mpi::Op::maximum) == size - 1);
        assert(world.allreduce(rank, pyre::mpi::Op::minimum) == 0);

        // the same for floating point cells, to prove the deduction really is generic
        assert(world.allreduce(1.0, pyre::mpi::Op::sum) == static_cast<double>(size));

        // an elementwise reduction over a block of cells
        std::vector<int> mine { rank, 2 * rank };
        // combine them
        auto combined = world.allreduce(mine, pyre::mpi::Op::sum);
        // one answer per cell
        assert(combined.size() == 2);
        // each summed independently
        assert(combined[0] == total);
        assert(combined[1] == 2 * total);

        // an inclusive scan hands me the sum over everybody who precedes me, myself included
        assert(world.scan(rank, pyre::mpi::Op::sum) == rank * (rank + 1) / 2);
        // the exclusive one leaves me out; every process must take part, but the standard
        // declares the answer undefined at rank zero, where there is nothing to combine, so
        // that is the one rank we may not check
        auto running = world.exscan(rank, pyre::mpi::Op::sum);
        // everywhere else it is the sum over my strict predecessors
        if (rank > 0) {
            assert(running == rank * (rank - 1) / 2);
        }

        // gather every rank at the root
        auto gathered = world.gather(rank, 0);
        // only the root gets anything
        if (rank == 0) {
            // one cell per process
            assert(gathered.size() == static_cast<std::size_t>(size));
            // in rank order
            for (int slot = 0; slot < size; ++slot) {
                assert(gathered[slot] == slot);
            }
        } else {
            // everybody else gets nothing at all
            assert(gathered.empty());
        }

        // the same, delivered to everybody
        auto everywhere = world.allgather(rank);
        // one cell per process
        assert(everywhere.size() == static_cast<std::size_t>(size));
        // and they sum to what we expect
        assert(std::accumulate(everywhere.begin(), everywhere.end(), 0) == total);

        // scatter one cell per process from the root; only the root's buffer matters
        std::vector<int> parcels(rank == 0 ? size : 0);
        // fill it with the doubled rank of the process each cell is bound for
        if (rank == 0) {
            for (int slot = 0; slot < size; ++slot) {
                parcels[slot] = 2 * slot;
            }
        }
        // hand them out; each process receives the cell addressed to it
        assert(world.scatter(parcels, 0) == 2 * rank);

        // every process hands one cell to every process; the cell i send to {peer} says who
        // sent it
        std::vector<int> outgoing(size, rank);
        // exchange
        auto incoming = world.alltoall(outgoing);
        // so i receive one cell from each process, each carrying that process's rank
        assert(incoming.size() == static_cast<std::size_t>(size));
        // in rank order
        for (int slot = 0; slot < size; ++slot) {
            assert(incoming[slot] == slot);
        }

        // a scatter whose root brought the wrong number of cells is refused before mpi ever
        // sees it, rather than reading past the end of the buffer
        if (rank == 0) {
            // plant a flag
            bool refused = false;
            // ask for the impossible
            try {
                // one cell too few
                std::vector<int> wrong(size - 1);
                // so this must fail
                world.scatter(wrong, 0);
            }
            // with a shape error
            catch (const pyre::mpi::ShapeError &) {
                refused = true;
            }
            // check that it did
            assert(refused);
        }

        // the ranks that did not raise must not wait for the one that did, so line everybody
        // up again before we tear mpi down
        world.barrier();
    }

    // take mpi down
    pyre::mpi::finalize();

    // all done
    return 0;
}


// end of file
