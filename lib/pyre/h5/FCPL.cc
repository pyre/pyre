// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "FCPL.h"


// make a fresh file creation property list
pyre::h5::FCPL::FCPL() : PropList(H5Pcreate(H5P_FILE_CREATE)) {}


// adopt an existing raw handle
pyre::h5::FCPL::FCPL(id_type id) : PropList(id) {}


// the shared default file creation property list
auto
pyre::h5::FCPL::theDefault() -> const FCPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const FCPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the file space page size
auto
pyre::h5::FCPL::pageSize() const -> hsize_t
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
pyre::h5::FCPL::setPageSize(hsize_t size) -> void
{
    // hand it to the library
    H5Pset_file_space_page_size(id(), size);
    // all done
    return;
}


// the file space strategy: (strategy, persist free space, threshold)
auto
pyre::h5::FCPL::filespaceStrategy() const -> std::tuple<H5F_fspace_strategy_t, hbool_t, hsize_t>
{
    // make room for the answer
    H5F_fspace_strategy_t strategy = H5F_FSPACE_STRATEGY_FSM_AGGR;
    hbool_t persist = 0;
    hsize_t threshold = 0;
    // ask the library
    H5Pget_file_space_strategy(id(), &strategy, &persist, &threshold);
    // pack and ship
    return { strategy, persist, threshold };
}


// set the file space strategy
auto
pyre::h5::FCPL::setFilespaceStrategy(
    H5F_fspace_strategy_t strategy, hbool_t persist, hsize_t threshold) -> void
{
    // hand them to the library
    H5Pset_file_space_strategy(id(), strategy, persist, threshold);
    // all done
    return;
}


// end of file
