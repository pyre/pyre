// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2013 all rights reserved
// 

#if !defined(gsl_extension_partition_h)
#define gsl_extension_partition_h


// place everything in my private namespace
namespace gsl {
    namespace mpi {

        // gather
        extern const char * const gather__name__;
        extern const char * const gather__doc__;
        PyObject * gather(PyObject *, PyObject *);

        // scatter
        extern const char * const scatter__name__;
        extern const char * const scatter__doc__;
        PyObject * scatter(PyObject *, PyObject *);

    } // of namespace mpi
} // of namespace gsl

#endif

// end of file
