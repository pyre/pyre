// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Diagnostic_h)
#define pyre_journal_Diagnostic_h

// place Diagnostic in namespace pyre::journal
namespace pyre {
    namespace journal {
        template <typename> class Diagnostic;
    }
}

// the injection operator
template <typename Channel, typename item_t>
inline
pyre::journal::Diagnostic<Channel> &
operator << (pyre::journal::Diagnostic<Channel> &, item_t);


// declaration
template <typename Severity>
class pyre::journal::Diagnostic {
    // types: place typedefs here
public:
    typedef Severity severity_t;
    typedef std::string string_t;
    typedef string_t metakey_t;
    typedef string_t metavalue_t;

    typedef std::vector<string_t> page_t;
    typedef std::stringstream buffer_t;
    typedef std::map<metakey_t, metavalue_t> metadata_t;

    // interface
public:
    // complete an entry
    inline Diagnostic & record();
    // add a new line
    inline Diagnostic & newline();
    // decorate with (key,value) meta data
    inline Diagnostic & setattr(string_t, string_t);
    // inject an item into the message stream
    template <typename item_t>
    inline Diagnostic & inject(item_t datum);

    // meta methods
public:
    inline ~Diagnostic();
    inline Diagnostic();
    inline Diagnostic(const Diagnostic &);
    inline Diagnostic & operator=(const Diagnostic &);
    
    // data members
public:
    page_t _page;
    buffer_t _buffer;
    metadata_t _metadata;

};


// get the inline definitions
#define pyre_journal_Diagnostic_icc
#include "Diagnostic.icc"
#undef pyre_journal_Diagnostic_icc


# endif
// end of file
