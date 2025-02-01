// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <cstdint>
#include <utility>

// the storage strategies
#include <pyre/memory.h>

// declarations
#include <pyre/typelists/apply.h>


// driver
int
main()
{
    // make a pile with a single cell type
    using byte_t = pyre::typelists::types_t<std::uint8_t>;
    // make a pile with a single template
    using heap_t = pyre::typelists::templates_t<pyre::memory::heap_t>;

    // expand a single templlate against a single type
    using oxo_t = pyre::typelists::apply_t<heap_t, byte_t>::type;
    // verify
    static_assert(
        std::is_same_v<oxo_t, pyre::typelists::types_t<pyre::memory::heap_t<std::uint8_t>>>,
        "mismatch in oxo_t");

    // make a collection with a few cell types
    using cells_t = pyre::typelists::types_t<
        pyre::typelists::types_t<std::uint8_t>, pyre::typelists::types_t<std::uint16_t>,
        pyre::typelists::types_t<std::uint32_t>>;
    // expand a single template against all the cell types
    using oxc_t = pyre::typelists::apply_t<heap_t, cells_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            oxc_t, pyre::typelists::types_t<
                       pyre::memory::heap_t<std::uint8_t>, pyre::memory::heap_t<std::uint16_t>,
                       pyre::memory::heap_t<std::uint32_t>>>,
        "mismatch in oxc_t");

    // make a pile with multiple storage strategies
    using strategies_t = pyre::typelists::templates_t<
        pyre::memory::heap_t, pyre::memory::map_t, pyre::memory::view_t>;
    // expand
    using sxc_t = pyre::typelists::apply_t<strategies_t, cells_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            sxc_t, pyre::typelists::types_t<
                       // heaps
                       pyre::memory::heap_t<std::uint8_t>, pyre::memory::heap_t<std::uint16_t>,
                       pyre::memory::heap_t<std::uint32_t>,
                       // maps
                       pyre::memory::map_t<std::uint8_t>, pyre::memory::map_t<std::uint16_t>,
                       pyre::memory::map_t<std::uint32_t>,
                       // views
                       pyre::memory::view_t<std::uint8_t>, pyre::memory::view_t<std::uint16_t>,
                       pyre::memory::view_t<std::uint32_t>>>,
        "mismatch in sxc_t");

    // all done
    return 0;
}


// end of file
