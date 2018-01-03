// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
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
class pyre::journal::Diagnostic : public pyre::journal::Chronicler {
    // types
public:
    typedef Severity severity_t;
    typedef std::string string_t;

    typedef std::vector<string_t> entry_t;
    typedef std::stringstream buffer_t;
    typedef std::map<string_t, string_t> metadata_t;

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
protected:
    inline ~Diagnostic();
    inline Diagnostic(string_t, string_t);
    // disallow
private:
    inline Diagnostic(const Diagnostic &);
    inline Diagnostic & operator=(const Diagnostic &);

    // data members
private:
    entry_t _entry;
    buffer_t _buffer;
    metadata_t _metadata;

    // implementation details
protected:
    inline void _startRecording();
    inline void _endRecording();
};


// get the inline definitions
#define pyre_journal_Diagnostic_icc
#include "Diagnostic.icc"
#undef pyre_journal_Diagnostic_icc


# endif
// end of file
