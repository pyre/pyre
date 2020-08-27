// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2020 all rights reserved

#if !defined(pyre_journal_Tee_h)
#define pyre_journal_Tee_h

// behaves like POSIX tee(1)
// i.e. outputs to stdout, as well as any number of extra files
class pyre::journal::Tee : public Splitter
{
public:
    template<typename... Ts>
    Tee(const Ts&... args) :
        Splitter{{
            // log to console,
            std::make_shared<cout_t>(),
            // and any number of additional files
            std::make_shared<file_t>(args)...
        }}
    {}

    virtual ~Tee() = default;
};

#endif // pyre_journal_Tee_h

// end of file
