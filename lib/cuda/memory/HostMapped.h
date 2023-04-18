// -*- c++ -*-

// code guard
#if !defined(pyre_cuda_memory_HostMapped_h)
#define pyre_cuda_memory_HostMapped_h

// a block of cells on mapped memory
template <class T, bool isConst>
class pyre::cuda::memory::HostMapped {
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
    // allocate a new block of memory
    inline HostMapped(cell_count_type);
    // i can make one from a block and a count
    inline HostMapped(handle_type, cell_count_type);

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
    // set the device pointer to the host pointer
    inline auto device() const -> pointer;

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
    handle_type _data;
    pointer _device_data;
    const cell_count_type _cells;

    // default metamethods
public:
    // destructor
    ~HostMapped() = default;
    // constructors
    HostMapped(const HostMapped &) = default;
    HostMapped(HostMapped &&) = default;
    HostMapped & operator=(const HostMapped &) = default;
    HostMapped & operator=(HostMapped &&) = default;
};

// get the inline definitions
#define pyre_cuda_memory_HostMapped_icc
#include "HostMapped.icc"
#undef pyre_cuda_memory_HostMapped_icc

#endif

// end of file
