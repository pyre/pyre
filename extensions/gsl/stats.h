// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

#if !defined(gsl_extension_stats_h)
#define gsl_extension_stats_h


// place everything in my private namespace
namespace gsl {
    namespace stats {

        // gsl_stats_correlation
        extern const char * const correlation__name__;
        extern const char * const correlation__doc__;
        PyObject * correlation(PyObject *, PyObject *);
        
        // gsl_stats_covariance
        extern const char * const covariance__name__;
        extern const char * const covariance__doc__;
        PyObject * covariance(PyObject *, PyObject *);

    } // of namespace stats
} // of namespace gsl

#endif

// end of file
