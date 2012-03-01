// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(gsl_extension_linalg_h)
#define gsl_extension_linalg_h


// place everything in my private namespace
namespace gsl {
    namespace linalg {

        extern const char * const cholesky_decomp__name__;
        extern const char * const cholesky_decomp__doc__;
        PyObject * cholesky_decomp(PyObject *, PyObject *);

        extern const char * const LU_decomp__name__;
        extern const char * const LU_decomp__doc__;
        PyObject * LU_decomp(PyObject *, PyObject *);

        extern const char * const LU_invert__name__;
        extern const char * const LU_invert__doc__;
        PyObject * LU_invert(PyObject *, PyObject *);

        extern const char * const LU_det__name__;
        extern const char * const LU_det__doc__;
        PyObject * LU_det(PyObject *, PyObject *);

    } // of namespace linalg
} // of namespace gsl

#endif

// end of file
