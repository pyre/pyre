// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#if !defined(pyre_memory_api_h)
#define pyre_memory_api_h


// user facing types
namespace pyre::memory {
    // normalized type access
    template <typename T, bool isConst>
    using cell_t = Cell<T, isConst>;

    // helper that generates a human readable name for each supported datatype
    template <typename T>
    using cellname_t = CellName<T>;

    // block on the stack
    template <int D, typename T>
    using stack_t = Stack<D, T, false>;
    // read-only version
    template <int D, typename T>
    using conststack_t = Stack<D, T, true>;

    // block on the heap
    template <typename T>
    using heap_t = Heap<T, false>;
    // read-only version
    template <typename T>
    using constheap_t = Heap<T, true>;

    // file-backed blocks of cells
    template <typename T>
    using map_t = Map<T, false>;
    // file-backed blocks of const cells
    template <typename T>
    using constmap_t = Map<T, true>;

    // view to someone else's data
    template <typename T>
    using view_t = View<T, false>;

    // const view to someone else's data
    template <typename T>
    using constview_t = View<T, true>;
} // namespace pyre::memory


// low level entities; you should probably stay away from them
namespace pyre::memory {
    // support for managing file-backed memory undifferentiated blocks
    // used by {map_t} and {constmap_t} above
    using filemap_t = FileMap;

    // expansion api
    // basic types
    template <typename... typeT>
    using types_t = Types<typeT...>;

    // datatypes
    using cellTypes_t = types_t<
        // signed integers
        int8_t, int16_t, int32_t, int64_t,
        // unsigned integers
        uint8_t, uint16_t, uint32_t, uint64_t,
        // floating point
        float32_t, float64_t,
        // complex
        complex64_t, complex128_t>;

    // storage strategies
    template <template <typename typeT> class... strategiesT>
    using storageStrategies_t = StorageStrategies<strategiesT...>;

    // the read-only storage strategies
    using constStorageStrategies_t = storageStrategies_t<
        // const heaps, maps, views
        constheap_t, constmap_t, constview_t>;

    // the read/write storage strategies
    using mutableStorageStrategies_t = storageStrategies_t<
        // writeable heaps, maps, view
        heap_t, map_t, view_t>;

    // all storage strategies
    using allStorageStrategies_t = Concat<constStorageStrategies_t, mutableStorageStrategies_t>;

    // type list concatenation
    template <typename... listT>
    using concat_t = Concat<listT...>;
} // namespace pyre::memory


#endif

// end of file
