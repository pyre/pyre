// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Chronicler_h)
#define pyre_journal_Chronicler_h


// singleton that owns the journal default configuration
class pyre::journal::Chronicler {
    // types
public:
    // strings;
    using string_type = string_t;
    // detail level
    using detail_type = detail_t;
    // the margin type
    using margin_type = string_type;
    // global metadata
    using key_type = key_t;
    using value_type = value_t;
    using notes_type = notes_t;

    // device support
    using device_type = device_ptr;

    // channel names
    using name_type = name_t;
    using nameset_type = nameset_t;

    // command line parsing
    using cmdname_type = cmdname_t;
    using cmdvalue_type = cmdvalue_t;
    using cmd_type = cmd_t;

    // interface
public:
    // the initializer that parses the program command line
    static void init(int argc, char * argv[]);

    // suppress all output
    static void quiet();

    // decoration level filter
    static inline auto decor() -> detail_type;
    static inline auto decor(detail_type) -> detail_type;
    // detail level filter
    static inline auto detail() -> detail_type;
    static inline auto detail(detail_type) -> detail_type;

    // print margin control
    static inline auto margin() -> margin_type;
    static inline auto margin(margin_type) -> margin_type;

    // metadata
    static inline auto notes() -> notes_type &;
    // device support
    static inline auto device() -> device_type;
    static inline void device(device_type);

    template <class deviceT, class... Args>
    static inline void device(Args &&... args);

    // convert a string with a comma separated list of names into a set
    static inline auto nameset(string_type) -> nameset_type;

    // data members
private:
    static device_type _device;
    static notes_type _notes;
    static detail_type _decor;
    static detail_type _detail;
    static string_type _margin;

    // disallow
private:
    Chronicler() = delete;
    Chronicler(const Chronicler &) = delete;
    Chronicler(const Chronicler &&) = delete;
    const Chronicler & operator=(const Chronicler &) = delete;
    const Chronicler & operator=(const Chronicler &&) = delete;
};


// get the inline definitions
#define pyre_journal_Chronicler_icc
#include "Chronicler.icc"
#undef pyre_journal_Chronicler_icc


#endif

// end of file
