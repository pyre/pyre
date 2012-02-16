// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(gsl_extension_rng_h)
#define gsl_extension_rng_h


// place everything in my private namespace
namespace gsl {
    namespace rng {

        // initialization
        void initialize();

        // alloc
        extern const char * const alloc__name__;
        extern const char * const alloc__doc__;
        PyObject * alloc(PyObject *, PyObject *);

        // set
        extern const char * const set__name__;
        extern const char * const set__doc__;
        PyObject * set(PyObject *, PyObject *);

        // name
        extern const char * const name__name__;
        extern const char * const name__doc__;
        PyObject * name(PyObject *, PyObject *);

        // avail
        extern const char * const avail__name__;
        extern const char * const avail__doc__;
        PyObject * avail(PyObject *, PyObject *);

    } // of namespace rng
} // of namespace gsl

#endif

// end of file
