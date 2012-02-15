// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(gsl_extension_vector_h)
#define gsl_extension_vector_h


// place everything in my private namespace
namespace gsl {
    namespace vector {

        // allocate
        extern const char * const allocate__name__;
        extern const char * const allocate__doc__;
        PyObject * allocate(PyObject *, PyObject *);

        // set_zero
        extern const char * const set_zero__name__;
        extern const char * const set_zero__doc__;
        PyObject * set_zero(PyObject *, PyObject *);

    } // of namespace vector
} // of namespace gsl

#endif

// end of file
