// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Null_h)
#define pyre_journal_Null_h

// place Null in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Null;
    }
}


// the injection operator
template <typename item_t>
inline
pyre::journal::Null &
operator << (pyre::journal::Null &, item_t);


// declaration
class pyre::journal::Null
{
    // types
public:
    typedef std::string string_t;

    // interface
public:
    // accessors
    inline bool isActive() const;

    // mutators
    inline void activate() const;
    inline void deactivate() const;

    // meta methods
public:
    inline operator bool() const;

    inline ~Null();
    inline Null(const string_t &);
    // disallow
private:
    inline Null(const Null &);
    inline const Null & operator=(const Null &);
};


// get the inline definitions
#define pyre_journal_Null_icc
#include "Null.icc"
#undef pyre_journal_Null_icc


# endif
// end of file
