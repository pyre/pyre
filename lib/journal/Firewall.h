// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Firewall_h)
#define pyre_journal_Firewall_h

// place Firewall in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Firewall;
    }
}


// declaration
class pyre::journal::Firewall :
    public pyre::journal::Diagnostic<Firewall>,
    public pyre::journal::Channel<Firewall, true>
{
    // befriend my superclass so it can invoke my recording hooks
    friend class Diagnostic<Firewall>;

    // types
public:
    typedef std::string string_t;
    typedef Diagnostic<Firewall> diagnostic_t;
    typedef Channel<Firewall, true> channel_t;

    // meta methods
public:
    inline ~Firewall();
    inline Firewall(string_t name);
    // disallow
private:
    inline Firewall(const Firewall &);
    inline const Firewall & operator=(const Firewall &);

    // implementation details
protected:
    inline void _endRecording(); // NYI: are firewalls fatal?
};


// get the inline definitions
#define pyre_journal_Firewall_icc
#include "Firewall.icc"
#undef pyre_journal_Firewall_icc


# endif
// end of file
