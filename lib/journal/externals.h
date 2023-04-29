// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_externals_h)
#define pyre_journal_externals_h


// externals
#include <cstdlib>
#include <type_traits>
#include <stdexcept>
#include <utility>
#include <memory>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <fstream>
#include <sstream>
#include <iomanip>


// aliases for fundamental types that define implementation choices
namespace pyre::journal {
    // sizes of things
    using size_t = std::size_t;
    // strings
    using string_t = std::string;
    // output streams; careful here: we already have a {stream_t} that's an alias for a device
    // {Stream} device
    using outputstream_t = std::ostream;
    // file streams; careful here: we already have a {file_t} that's an alias to the file device
    using filestream_t = std::ofstream;
    // and their mode bit masks
    using filemode_t = std::ios_base::openmode;
    // paths
    using path_t = std::string;

    // generic names
    using name_t = string_t;
    // set of names
    using nameset_t = std::set<name_t>;

    // command line parsing
    using cmdname_t = string_t;
    using cmdvalue_t = string_t;
    using cmd_t = std::map<cmdname_t, cmdvalue_t>;

    // the channel level of detail
    using detail_t = int;
    // the channel dent level
    using dent_t = int;

    // the type of line
    using line_t = string_t;
    // line buffer: the accumulator of partially constructed messages
    using linebuf_t = std::stringstream;
    // a page is the payload of a journal entry
    using page_t = std::vector<line_t>;
    // metadata associated with a journal entry
    using key_t = string_t;
    using value_t = string_t;
    using notes_t = std::map<key_t, value_t>;

    // a color table is a map from a color name to a control string
    using colorname_t = string_t;
    using colorrep_t = string_t;
    using colortable_t = std::map<colorname_t, colorrep_t>;

    // a palette is a map from a metadata key to a color name; it is used by the renderers to
    // colorize the message notes
    using palette_t = std::map<key_t, colorrep_t>;
} // namespace pyre::journal


#endif

// end of file
