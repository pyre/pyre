// -*- C++ -*-
// -*- coding: utf-8 -*-
//

// code guard
#if !defined(pyre_cuda_Device_h)
#define pyre_cuda_Device_h

#include <string>

// A CUDA-enabled device
class pyre::cuda::Device {
public:
    // Construct a new Device object.
    //
    // Does not change the currently active CUDA device.
    Device(int id);

    // Return the (0-based) device index.
    inline int id() const noexcept;

    // Return a string identifying the device.
    std::string name() const;

    // Get the total global memory capacity in bytes.
    size_t totalGlobalMem() const;

    // Get the compute capability.
    pyre::cuda::ComputeCapability computeCapability() const;

private:
    int _id;
};

// Compare two Device objects.
inline bool
pyre::cuda::
operator==(pyre::cuda::Device, pyre::cuda::Device) noexcept;

// Compare two Device objects.
inline bool
pyre::cuda::
operator!=(pyre::cuda::Device, pyre::cuda::Device) noexcept;

// Return the number of available CUDA devices.
int
pyre::cuda::getDeviceCount();

// Get the current CUDA device for the active host thread.
pyre::cuda::Device
pyre::cuda::getDevice();

// Set the CUDA device for the active host thread.
void
pyre::cuda::setDevice(pyre::cuda::Device);

#endif

// end of file
