// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <complex>
#include <cstdint>
#include <utility>

// template expansion support
#include <pyre/typelists.h>
// the grid
#include <pyre/grid.h>


template <typename...>
struct expand_t;

template <template <typename...> class... strategiesT, typename... cellsT, int... dimsT>
struct expand_t<
    // the list of strategies
    pyre::typelists::templates_t<strategiesT...>,
    // the list of cells
    pyre::typelists::types_t<cellsT...>,
    // the list of dimensions
    std::integer_sequence<int, dimsT...>> {
    // expand the strategies
    using strategies = typename pyre::typelists::apply_t<
        // the templates
        pyre::typelists::templates_t<strategiesT...>,
        // their arguments
        pyre::typelists::types_t<pyre::typelists::types_t<cellsT>...>>::type;
    // compute the packings
    using packings = pyre::typelists::types_t<pyre::grid::canonical_t<dimsT>...>;
    // expand the grids
    using grids = typename pyre::typelists::apply_t<
        pyre::typelists::templates_t<pyre::grid::grid_t>,
        typename pyre::typelists::cartesian_t<packings, strategies>::type>::type;
    // collect
    using type = grids;
};


// the driver
int
main()
{
    // the grid dimensions
    using dims_t = std::integer_sequence<int, 1, 2, 3, 4>;
    // the list of cell types
    using cells_t = pyre::typelists::types_t<
        // signed integral types
        std::int8_t,
        // unsigned integral types
        std::uint8_t,
        // floats
        std::float_t, std::double_t,
        // complex
        std::complex<std::float_t>, std::complex<std::double_t>>;
    // the list of storage strategies
    using strategies_t = pyre::typelists::templates_t<
        // read/write
        pyre::memory::heap_t, pyre::memory::map_t, pyre::memory::view_t,
        // read-only
        pyre::memory::constheap_t, pyre::memory::constmap_t, pyre::memory::constview_t>;

    // strategies
    using strategyExpansions_t = typename expand_t<strategies_t, cells_t, dims_t>::strategies;
    // check
    static_assert(
        std::is_same_v<
            strategyExpansions_t,
            pyre::typelists::types_t<
                // read/write
                // heaps
                pyre::memory::heap_t<std::int8_t>, pyre::memory::heap_t<std::uint8_t>,
                pyre::memory::heap_t<std::float_t>, pyre::memory::heap_t<std::double_t>,
                pyre::memory::heap_t<std::complex<std::float_t>>,
                pyre::memory::heap_t<std::complex<std::double_t>>,
                // maps
                pyre::memory::map_t<std::int8_t>, pyre::memory::map_t<std::uint8_t>,
                pyre::memory::map_t<std::float_t>, pyre::memory::map_t<std::double_t>,
                pyre::memory::map_t<std::complex<std::float_t>>,
                pyre::memory::map_t<std::complex<std::double_t>>,
                // views
                pyre::memory::view_t<std::int8_t>, pyre::memory::view_t<std::uint8_t>,
                pyre::memory::view_t<std::float_t>, pyre::memory::view_t<std::double_t>,
                pyre::memory::view_t<std::complex<std::float_t>>,
                pyre::memory::view_t<std::complex<std::double_t>>,
                // read-only
                // heaps
                pyre::memory::constheap_t<std::int8_t>, pyre::memory::constheap_t<std::uint8_t>,
                pyre::memory::constheap_t<std::float_t>, pyre::memory::constheap_t<std::double_t>,
                pyre::memory::constheap_t<std::complex<std::float_t>>,
                pyre::memory::constheap_t<std::complex<std::double_t>>,
                // maps
                pyre::memory::constmap_t<std::int8_t>, pyre::memory::constmap_t<std::uint8_t>,
                pyre::memory::constmap_t<std::float_t>, pyre::memory::constmap_t<std::double_t>,
                pyre::memory::constmap_t<std::complex<std::float_t>>,
                pyre::memory::constmap_t<std::complex<std::double_t>>,
                // views
                pyre::memory::constview_t<std::int8_t>, pyre::memory::constview_t<std::uint8_t>,
                pyre::memory::constview_t<std::float_t>, pyre::memory::constview_t<std::double_t>,
                pyre::memory::constview_t<std::complex<std::float_t>>,
                pyre::memory::constview_t<std::complex<std::double_t>>>>,
        "mismatch in the strategy expansions");

    // packings
    using packingExpansions_t = typename expand_t<strategies_t, cells_t, dims_t>::packings;
    // check
    static_assert(
        std::is_same_v<
            packingExpansions_t, pyre::typelists::types_t<
                                     pyre::grid::canonical_t<1>, pyre::grid::canonical_t<2>,
                                     pyre::grid::canonical_t<3>, pyre::grid::canonical_t<4>>>,
        "mismatch in the packing expansions");

    // the list of grids
    using grids_t = typename expand_t<strategies_t, cells_t, dims_t>::type;
    // check
    static_assert(
        std::is_same_v<
            grids_t,
            pyre::typelists::types_t<
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::heap_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::heap_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::heap_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::heap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::heap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::heap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::map_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::map_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::map_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::map_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::map_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::map_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::view_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::view_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::view_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<1>, pyre::memory::view_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::view_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::view_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constheap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constheap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constheap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constheap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>,
                    pyre::memory::constheap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>,
                    pyre::memory::constheap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constmap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constmap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constmap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constmap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>,
                    pyre::memory::constmap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>,
                    pyre::memory::constmap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constview_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constview_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constview_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>, pyre::memory::constview_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>,
                    pyre::memory::constview_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<1>,
                    pyre::memory::constview_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::map_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::map_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::map_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::map_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::map_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::map_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::view_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::view_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::view_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::view_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::view_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::view_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constheap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constheap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constheap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constheap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>,
                    pyre::memory::constheap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>,
                    pyre::memory::constheap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constmap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constmap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constmap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constmap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>,
                    pyre::memory::constmap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>,
                    pyre::memory::constmap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constview_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constview_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constview_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>, pyre::memory::constview_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>,
                    pyre::memory::constview_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<2>,
                    pyre::memory::constview_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::heap_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::heap_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::heap_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::heap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::heap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::heap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::map_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::map_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::map_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::map_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::map_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::map_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::view_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::view_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::view_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<3>, pyre::memory::view_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::view_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::view_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constheap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constheap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constheap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constheap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>,
                    pyre::memory::constheap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>,
                    pyre::memory::constheap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constmap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constmap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constmap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constmap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>,
                    pyre::memory::constmap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>,
                    pyre::memory::constmap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constview_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constview_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constview_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>, pyre::memory::constview_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>,
                    pyre::memory::constview_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<3>,
                    pyre::memory::constview_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::heap_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::heap_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::heap_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::heap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::heap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::heap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::map_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::map_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::map_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::map_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::map_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::map_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::view_t<std::int8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::view_t<std::uint8_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::view_t<std::float_t>>,
                pyre::grid::grid_t<pyre::grid::canonical_t<4>, pyre::memory::view_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::view_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::view_t<std::complex<std::double_t>>>,

                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constheap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constheap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constheap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constheap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>,
                    pyre::memory::constheap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>,
                    pyre::memory::constheap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constmap_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constmap_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constmap_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constmap_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>,
                    pyre::memory::constmap_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>,
                    pyre::memory::constmap_t<std::complex<std::double_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constview_t<std::int8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constview_t<std::uint8_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constview_t<std::float_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>, pyre::memory::constview_t<std::double_t>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>,
                    pyre::memory::constview_t<std::complex<std::float_t>>>,
                pyre::grid::grid_t<
                    pyre::grid::canonical_t<4>,
                    pyre::memory::constview_t<std::complex<std::double_t>>>>>,
        "mismatch in grids_t");

    // all done
    return 0;
}


// end of file
