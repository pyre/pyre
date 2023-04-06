// -*- c++ -*-

// code guard
#if !defined(pyre_cuda_memory_DeviceMapped_h)
#define pyre_cuda_memory_DeviceMapped_h

// a block of cells on mapped memory
template <class T, bool isConst>
class pyre::cuda::memory::DeviceMapped {
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
    // set the device pointer to the host pointer
    inline DeviceMapped(pointer);

    // accessors
public:
    // access to the raw device data pointer
    inline auto device_data() const -> pointer;

    // implementation details: data
private:
    pointer _device_data;

    // default metamethods
public:
    // destructor
    ~DeviceMapped() = default;
    // constructors
    DeviceMapped(const DeviceMapped &) = default;
    DeviceMapped(DeviceMapped &&) = default;
    DeviceMapped & operator=(const DeviceMapped &) = default;
    DeviceMapped & operator=(DeviceMapped &&) = default;
};

// get the inline definitions
#define pyre_cuda_memory_DeviceMapped_icc
#include "DeviceMapped.icc"
#undef pyre_cuda_memory_DeviceMapped_icc

#endif

// end of file
