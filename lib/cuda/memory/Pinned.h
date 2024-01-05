// -*- c++ -*-
//
// sebastiaan van paasen
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_cuda_memory_Pinned_h)
#define pyre_cuda_memory_Pinned_h

// a block of cells on pinned memory
template <class T, bool isConst>
class pyre::cuda::memory::Pinned {
    // types
public:
    // my cell
    using cell_type = pyre::memory::cell_t<T, isConst>;
    // pull the type aliases
    using value_type = typename cell_type::value_type;
    // derived types
    using pointer = typename cell_type::pointer;
    using const_pointer = typename cell_type::const_pointer;
    using reference = typename cell_type::reference;
    using const_reference = typename cell_type::const_reference;
    // distances
    using difference_type = typename cell_type::difference_type;
    // sizes of things
    using size_type = typename cell_type::size_type;
    using cell_count_type = typename cell_type::cell_count_type;
    // my handle
    using handle_type = std::shared_ptr<value_type>;

    // metamethods
public:
    // allocate a new block of host memory
    inline Pinned(cell_count_type);
    // i can make one from a block and a count
    inline Pinned(handle_type, cell_count_type);

    // accessors
public:
    // the number of cells
    inline auto cells() const -> cell_count_type;
    // the memory footprint of the block
    inline auto bytes() const -> size_type;
    // access to the raw data pointer
    inline auto data() const -> pointer;
    // the shared pointer
    inline auto handle() const -> handle_type;
    // access to the device data pointer
    inline auto device() const -> pointer;

    // cpu gpu synchronization
public:
    // synchronize all memory from cpu to gpu
    inline auto synchronizeHostToDevice();
    // synchronize part off the memory from cpu to gpu
    inline auto synchronizeHostToDevice(difference_type, cell_count_type);
    // synchronize all memory from gpu to cpu
    inline auto synchronizeDeviceToHost();
    // synchronize part off the memory from gpu to cpu
    inline auto synchronizeDeviceToHost(difference_type, cell_count_type);

    // iterator support
public:
    inline auto begin() const -> pointer;
    inline auto end() const -> pointer;

    // data access
public:
    // with bounds checking
    inline auto at(size_type) const -> reference;
    // without bounds checking
    inline auto operator[](size_type) const -> reference;

    // implementation details: data
private:
    handle_type _host_data;
    pointer _device_data;
    const cell_count_type _cells;

    // default metamethods
public:
    // destructor
    ~Pinned();
    // constructors
    Pinned(const Pinned &) = default;
    Pinned(Pinned &&) = default;
    Pinned & operator=(const Pinned &) = default;
    Pinned & operator=(Pinned &&) = default;
};

// get the inline definitions
#define pyre_cuda_memory_Pinned_icc
#include "Pinned.icc"
#undef pyre_cuda_memory_Pinned_icc

#endif

// end of file
