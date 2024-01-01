// -*- C++ -*-
//
// Lijun Zhu (ljzhu@gps.caltech.edu)
//
// (c) 1998-2024 all rights reserved
//

#if !defined(gsl_extension_numpy_h)
#define gsl_extension_numpy_h


// place everything in my private namespace
namespace gsl {
    namespace vector {
        // vector_asnumpy
        extern const char * const ndarray__name__;
        extern const char * const ndarray__doc__;
        PyObject * ndarray(PyObject *, PyObject *);
    } // namespace vector

    namespace matrix {
        // matrix_ndarray
        extern const char * const ndarray__name__;
        extern const char * const ndarray__doc__;
        PyObject * ndarray(PyObject *, PyObject *);
    } // namespace matrix
} // namespace gsl

#endif // gsl_extension_numpy_h

// end of file
