// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(gsl_extension_capsules_h)
#define gsl_extension_capsules_h

// capsules
namespace gsl {

    // vectors
    namespace vector { 
        const char * const capsule_t = "gsl.vector";
        void free(PyObject *);
    }
    // matrix
    namespace matrix { 
        const char * const capsule_t = "gsl.matrix"; 
        void free(PyObject *);
    }
    // rng
    namespace rng {
        const char * const capsule_t = "gsl.rng"; 
        void free(PyObject *);
    }
}
// local

#endif

// end of file
