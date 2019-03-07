// -*- C++ -*-
//
// Lijun Zhu
// Caltech
// (c) 1998-2019 all rights reserved
//

#if !defined(gsl_extension_numpy_h)
#define gsl_extension_numpy_h


// place everything in my private namespace
namespace gsl {
    namespace vector {
        // vector_asnumpy
        extern const char * const asnumpy__name__;
        extern const char * const asnumpy__doc__;
        PyObject * asnumpy(PyObject *, PyObject *);
    } // of namespace vector

    namespace matrix {
        // matrix_asnumpy
        extern const char * const asnumpy__name__;
        extern const char * const asnumpy__doc__;
        PyObject * asnumpy(PyObject *, PyObject *);
    } // of namespace matrix
} // of namespace gsl

#endif //gsl_extension_numpy_h

// end of file
