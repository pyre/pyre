// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "FCPL.h"
// the reporting of library refusals
#include "../diagnostics.h"


// make a fresh file creation property list
pyre::h5::properties::FCPL::FCPL() : List(H5Pcreate(H5P_FILE_CREATE))
{
    // if the library refused to make it
    if (!valid()) {
        // complain
        complain("pyre.h5.fcpl", "creating a file creation property list");
    }
}


// adopt an existing raw handle
pyre::h5::properties::FCPL::FCPL(id_type id) : List(id) {}


// the shared default file creation property list
auto
pyre::h5::properties::FCPL::theDefault() -> const FCPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const FCPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the file space page size
auto
pyre::h5::properties::FCPL::pageSize() const -> hsize_t
{
    // make room for the answer
    hsize_t size = 0;
    // ask the library
    if (H5Pget_file_space_page_size(id(), &size) < 0) {
        // complain if it refused
        complain("pyre.h5.fcpl", "retrieving the file space page size");
        // and report nothing
        return 0;
    }
    // otherwise, report
    return size;
}


// set the file space page size
auto
pyre::h5::properties::FCPL::pageSize(hsize_t size) -> void
{
    // hand it to the library
    if (H5Pset_file_space_page_size(id(), size) < 0) {
        // and complain if it refused
        complain("pyre.h5.fcpl", "setting the file space page size");
    }
    // all done
    return;
}


// the file space strategy: (strategy, persist free space, threshold)
auto
pyre::h5::properties::FCPL::filespaceStrategy() const -> FilespaceStrategy
{
    // make room for the answer
    H5F_fspace_strategy_t strategy = H5F_FSPACE_STRATEGY_FSM_AGGR;
    hbool_t persist = 0;
    hsize_t threshold = 0;
    // ask the library
    if (H5Pget_file_space_strategy(id(), &strategy, &persist, &threshold) < 0) {
        // complain if it refused
        complain("pyre.h5.fcpl", "retrieving the file space strategy");
        // and report the library default
        return FilespaceStrategy(H5F_FSPACE_STRATEGY_FSM_AGGR, false, 0);
    }
    // otherwise, pack and ship
    return FilespaceStrategy(strategy, persist != 0, threshold);
}


// set the file space strategy
auto
pyre::h5::properties::FCPL::filespaceStrategy(const FilespaceStrategy & strategy) -> void
{
    // hand them to the library
    if (H5Pset_file_space_strategy(
            id(), strategy.strategy, static_cast<hbool_t>(strategy.persist), strategy.threshold)
        < 0) {
        // and complain if it refused
        complain("pyre.h5.fcpl", "setting the file space strategy");
    }
    // all done
    return;
}


// the size of the user block
auto
pyre::h5::properties::FCPL::userblock() const -> hsize_t
{
    // make room for the answer
    hsize_t size = 0;
    // ask the library
    if (H5Pget_userblock(id(), &size) < 0) {
        // complain if it refused
        complain("pyre.h5.fcpl", "retrieving the user block size");
        // and report nothing
        return 0;
    }
    // otherwise, report
    return size;
}


// set the size of the user block
auto
pyre::h5::properties::FCPL::userblock(hsize_t size) -> void
{
    // hand it to the library
    if (H5Pset_userblock(id(), size) < 0) {
        // and complain if it refused
        complain("pyre.h5.fcpl", "setting the user block size");
    }
    // all done
    return;
}


// the widths hdf5 uses to record positions and lengths
auto
pyre::h5::properties::FCPL::sizes() const -> Sizes
{
    // make room for the answer
    std::size_t offsets = 0;
    std::size_t lengths = 0;
    // ask the library
    if (H5Pget_sizes(id(), &offsets, &lengths) < 0) {
        // complain if it refused
        complain("pyre.h5.fcpl", "retrieving the offset and length widths");
        // and report empty widths
        return Sizes(0, 0);
    }
    // otherwise, pack and ship
    return Sizes(offsets, lengths);
}


// set the widths used to record positions and lengths
auto
pyre::h5::properties::FCPL::sizes(const Sizes & sizes) -> void
{
    // hand them to the library
    if (H5Pset_sizes(id(), sizes.offsets, sizes.lengths) < 0) {
        // and complain if it refused
        complain("pyre.h5.fcpl", "setting the offset and length widths");
    }
    // all done
    return;
}


// end of file
