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
    CUresult status;

    // find out how many devices there are
    int count;
    status = cuDeviceGetCount(&count);
    // if anything went wrong
    if (status != CUDA_SUCCESS) {
        // build an error message
        std::stringstream msg;
        msg << "'cuDeviceGetCount' returned error " << status << std::endl;
        // decorate the exception
        PyErr_SetString(Error, msg.str().c_str());
        // and raise it
        return 0;
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

        // the name of the device
        char name[256];
        status = cuDeviceGetName(name, 256, index);
        // if anything went wrong
        if (status != CUDA_SUCCESS) {
            // build an error message
            std::stringstream msg;
            msg << "'cuDeviceGetName' returned error " << status << std::endl;
            // decorate the exception
            PyErr_SetString(Error, msg.str().c_str());
            // and raise it
            return 0;
        }
        // convert to a python string and attach
        PyObject_SetAttrString(sheet, "name", PyUnicode_FromString(name));

        // compute capability
        int major, minor;
        status = cuDeviceComputeCapability(&major, &minor, index);
        // if anything went wrong
        if (status != CUDA_SUCCESS) {
            // build an error message
            std::stringstream msg;
            msg << "'cuDeviceComputeCapability' returned error " << status << std::endl;
            // decorate the exception
            PyErr_SetString(Error, msg.str().c_str());
            // and raise it
            return 0;
        }
        // build a representation of the compute capability
        PyObject * capability = PyTuple_New(2);
        PyTuple_SET_ITEM(capability, 0, PyLong_FromLong(major));
        PyTuple_SET_ITEM(capability, 1, PyLong_FromLong(minor));
        // attach it
        PyObject_SetAttrString(sheet, "capability", capability);

        // get the driver version
        int driverVersion;
        status = cuDriverGetVersion(&driverVersion);
        // if anything went wrong
        if (status != CUDA_SUCCESS) {
            // build an error message
            std::stringstream msg;
            msg << "'cuDriverGetVersion' returned error " << status << std::endl;
            // decorate the exception
            PyErr_SetString(Error, msg.str().c_str());
            // and raise it
            return 0;
        }
        // build a rep for the driver version
        PyObject *version = PyTuple_New(2);
        PyTuple_SET_ITEM(version, 0, PyLong_FromLong(driverVersion/1000));
        PyTuple_SET_ITEM(version, 1, PyLong_FromLong((driverVersion%100)/10));
        // attach it
        PyObject_SetAttrString(sheet, "version", version);

        // memory
        size_t memory;
        // device total memory
        status = cuDeviceTotalMem(&memory, index);
        // if anything went wrong
        if (status != CUDA_SUCCESS) {
            // build an error message
            std::stringstream msg;
            msg << "'cuDeviceTotalMem' returned error " << status << std::endl;
            // decorate the exception
            PyErr_SetString(Error, msg.str().c_str());
            // and raise it
            return 0;
        }
        // attach it
        PyObject_SetAttrString(sheet, "globalMemory", PyLong_FromUnsignedLong(memory));
    }

    // return the device tuple
    return result;
}
    

// end of file
