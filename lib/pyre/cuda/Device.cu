// -*- CUDA -*-
// -*- coding: utf-8 -*-
//

// my parts
#include "Device.h"
// local support
#include "ComputeCapability.h"

#include <pyre/journal.h>

pyre::cuda::Device::
Device(int id) :
    _id {id}
{
    const int count = getDeviceCount();
    if (id < 0 or id >= count) {
        // make an error channel
        pyre::journal::error_t error("cuda");
        // show me
        error
            << pyre::journal::at(__HERE__)
            << "invalid cuda device index " << id
            << pyre::journal::endl;

        // XXX throw an exception?
    }
}

static cudaDeviceProp
pyre::cuda::getDeviceProperties(int id)
{
    cudaDeviceProp props;
    const cudaError_t status = cudaGetDeviceProperties(&props, id);
    // if anything went wrong
    if (status != cudaSuccess) {
        // make an error channel
        pyre::journal::error_t error("cuda");
        // show me
        error
            << pyre::journal::at(__HERE__)
            << "while querying properties of device " << id << ": "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
    }
    return props;
}

std::string
pyre::cuda::Device::
name() const
{
    const auto props = pyre::cuda::getDeviceProperties(id());
    return props.name;
}

size_t
pyre::cuda::Device::
totalGlobalMem() const
{
    const auto props = pyre::cuda::getDeviceProperties(id());
    return props.totalGlobalMem;
}

pyre::cuda::ComputeCapability
pyre::cuda::Device::
computeCapability() const
{
    const auto props = pyre::cuda::getDeviceProperties(id());
    return {props.major, props.minor};
}

int
pyre::cuda::getDeviceCount()
{
    int count = -1;
    const cudaError_t status = cudaGetDeviceCount(&count);
    // if anything went wrong
    if (status != cudaSuccess) {
        // make an error channel
        pyre::journal::error_t error("cuda");
        // show me
        error
            << pyre::journal::at(__HERE__)
            << "failed to get cuda device count: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
    }
    return count;
}

pyre::cuda::Device
pyre::cuda::getDevice()
{
    int d = -1;
    const cudaError_t status = cudaGetDevice(&d);
    // if anything went wrong
    if (status != cudaSuccess) {
        // make an error channel
        pyre::journal::error_t error("cuda");
        // show me
        error
            << pyre::journal::at(__HERE__)
            << "failed to get current cuda device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
    }
    return d;
}

void
pyre::cuda::
setDevice(pyre::cuda::Device d)
{
    const cudaError_t status = cudaSetDevice(d.id());
    // if anything went wrong
    if (status != cudaSuccess) {
        // make an error channel
        pyre::journal::error_t error("cuda");
        // show me
        error
            << pyre::journal::at(__HERE__)
            << "failed to set cuda device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
    }
}

// end of file
