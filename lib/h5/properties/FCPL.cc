// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "FCPL.h"


// make a fresh file creation property list
pyre::h5::properties::FCPL::FCPL() : List(H5Pcreate(H5P_FILE_CREATE)) {}


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
    H5Pget_file_space_page_size(id(), &size);
    // and report
    return size;
}


// set the file space page size
auto
pyre::h5::properties::FCPL::pageSize(hsize_t size) -> void
{
    // hand it to the library
    H5Pset_file_space_page_size(id(), size);
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
    H5Pget_file_space_strategy(id(), &strategy, &persist, &threshold);
    // pack and ship
    return FilespaceStrategy(strategy, persist != 0, threshold);
}


// set the file space strategy
auto
pyre::h5::properties::FCPL::filespaceStrategy(const FilespaceStrategy & strategy) -> void
{
    // hand them to the library
    H5Pset_file_space_strategy(
        id(), strategy.strategy, static_cast<hbool_t>(strategy.persist), strategy.threshold);
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
    H5Pget_userblock(id(), &size);
    // and report
    return size;
}


// set the size of the user block
auto
pyre::h5::properties::FCPL::userblock(hsize_t size) -> void
{
    // hand it to the library
    H5Pset_userblock(id(), size);
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
    H5Pget_sizes(id(), &offsets, &lengths);
    // pack and ship
    return Sizes(offsets, lengths);
}


// set the widths used to record positions and lengths
auto
pyre::h5::properties::FCPL::sizes(const Sizes & sizes) -> void
{
    // hand them to the library
    H5Pset_sizes(id(), sizes.offsets, sizes.lengths);
    // all done
    return;
}


// end of file
