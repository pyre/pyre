// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2013 all rights reserved
// 

#include <portinfo>
#include <Python.h>
#include <pyre/journal.h>

// my declarations
#include "discover.h"
// local support
#include "exceptions.h"
// so I can build reasonable error messages
#include <sstream>

// access to the CUDA runtime
#include <cuda.h>
#include <cuda_runtime.h>


// device discovery
PyObject * 
pyre::extensions::cuda::
discover(PyObject *, PyObject *args)
{
    // the device property class; it's supposed to be a class, so it's an instance of {type}
    PyObject *sheetFactory;
    // my journal channel; for debugging
    journal::info_t info("cuda");

    // if I were not passed the expected arguments
    if (!PyArg_ParseTuple(args, "O!:discover", &PyType_Type, &sheetFactory)) {
        // raise an exception
        return 0;
    }
    
    // the cuda flag
    cudaError_t status;

    // find out how many devices there are
    int count;
    status = cudaGetDeviceCount(&count);
    // if anything went wrong
    if (status != cudaSuccess) {
        // pretend there are no CUDA capable devices
        return PyTuple_New(0);
    }
    // show me
    // info << "CUDA devices: " << count << journal::endl;
    
    // build the device tuple
    PyObject * result = PyTuple_New(count);

    // if there are no devices attached
    if (!count) {
        // why are we here?
        return result;
    }

    // loop over the available devices
    for (int index=0; index<count; ++index) {
        // make a device property sheet
        PyObject *sheet = PyObject_CallObject(sheetFactory, 0);
        // add it to our pile
        PyTuple_SET_ITEM(result, index, sheet);

        // start decorating: first the device id
        PyObject_SetAttrString(sheet, "id", PyLong_FromLong(index));

        // storage for the device properties
        cudaDeviceProp prop;
        // set the current device
        cudaSetDevice(index);
        // get its properties
        cudaGetDeviceProperties(&prop, index);

        // get the name of the device
        PyObject_SetAttrString(sheet, "name", PyUnicode_FromString(prop.name));

        // build a representation of the compute capability
        PyObject * capability = PyTuple_New(2);
        PyTuple_SET_ITEM(capability, 0, PyLong_FromLong(prop.major));
        PyTuple_SET_ITEM(capability, 1, PyLong_FromLong(prop.minor));
        // attach it
        PyObject_SetAttrString(sheet, "capability", capability);

        // version info
        int version;
        PyObject *vtuple;
        // get the driver version
        cudaDriverGetVersion(&version);
        // build a rep for the driver version
        vtuple = PyTuple_New(2);
        PyTuple_SET_ITEM(vtuple, 0, PyLong_FromLong(version/1000));
        PyTuple_SET_ITEM(vtuple, 1, PyLong_FromLong((version%100)/10));
        // attach it
        PyObject_SetAttrString(sheet, "driverVersion", vtuple);

        // get the runtime version
        cudaRuntimeGetVersion(&version);
        // build a rep for the runtime version
        vtuple = PyTuple_New(2);
        PyTuple_SET_ITEM(vtuple, 0, PyLong_FromLong(version/1000));
        PyTuple_SET_ITEM(vtuple, 1, PyLong_FromLong((version%100)/10));
        // attach it
        PyObject_SetAttrString(sheet, "runtimeVersion", vtuple);

        // device total memory
        PyObject_SetAttrString(sheet, "globalMemory", PyLong_FromUnsignedLong(prop.totalGlobalMem));
    }

    // return the device tuple
    return result;
}
    

// end of file
