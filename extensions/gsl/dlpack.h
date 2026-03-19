// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved
//
// Minimal DLPack v0.8 definitions (https://github.com/dmlc/dlpack).
// Reproduced here to avoid a compile-time dependency on an external dlpack package;
// the ABI is stable and versioned via DLPACK_VERSION.

#if !defined(gsl_extension_dlpack_h)
#define gsl_extension_dlpack_h

#include <cstdint>

#define DLPACK_VERSION 80
#define DLPACK_ABI_VERSION 1

// device types
typedef enum {
    kDLCPU = 1,
    kDLCUDA = 2,
} DLDeviceType;

typedef struct {
    DLDeviceType device_type;
    int32_t device_id;
} DLDevice;

// data type codes
typedef enum {
    kDLInt = 0,
    kDLUInt = 1,
    kDLFloat = 2,
    kDLBfloat = 4,
    kDLComplex = 5,
} DLDataTypeCode;

typedef struct {
    uint8_t code;    // DLDataTypeCode
    uint8_t bits;    // 32 or 64
    uint16_t lanes;  // 1 for scalar
} DLDataType;

typedef struct DLTensor {
    void * data;
    DLDevice device;
    int32_t ndim;
    DLDataType dtype;
    int64_t * shape;
    int64_t * strides;   // nullptr means compact row-major
    uint64_t byte_offset;
} DLTensor;

typedef struct DLManagedTensor {
    DLTensor dl_tensor;
    void * manager_ctx;
    void (*deleter)(struct DLManagedTensor *);
} DLManagedTensor;

// float64 dtype constant
static constexpr DLDataType kFloat64 = { kDLFloat, 64, 1 };
// CPU device constant
static constexpr DLDevice kCPU = { kDLCPU, 0 };

#endif

// end of file
