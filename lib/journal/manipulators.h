// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_journal_manipulators_h)
#define pyre_journal_manipulators_h


// manipulators
// end of transaction
template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::endl(Channel<severityT, proxyT> & channel) -> Channel<severityT, proxyT> &
{
    // ask the channel to record the accumulated message
    return channel.log();
}


template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::newline(Channel<severityT, proxyT> & channel) -> Channel<severityT, proxyT> &
{
    // ask the channel entry to mark the end of a line of output
    return channel.line();
}


template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::indent(Channel<severityT, proxyT> & channel) -> Channel<severityT, proxyT> &
{
    // ask the channel entry to mark the end of a line of output
    return channel.indent();
}


template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::outdent(Channel<severityT, proxyT> & channel) -> Channel<severityT, proxyT> &
{
    // ask the channel entry to mark the end of a line of output
    return channel.outdent();
}


// the injection operators
// detail level
template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::operator<<(Channel<severityT, proxyT> & channel, const Detail & detail)
    -> Channel<severityT, proxyT> &
{
    // adjust the detail of the channel
    channel.detail(detail.detail());
    // all done
    return channel;
}


// location info
template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::operator<<(Channel<severityT, proxyT> & channel, const Locator & locator)
    -> Channel<severityT, proxyT> &
{
    // use the locator information to set channel entry metadata
    channel.entry().note("filename", locator.file());
    channel.entry().note("line", locator.line());
    channel.entry().note("function", locator.func());

    // all done
    return channel;
}


// metadata
template <typename severityT, template <class> typename proxyT>
auto
pyre::journal::operator<<(Channel<severityT, proxyT> & channel, const Note & note)
    -> Channel<severityT, proxyT> &
{
    // transfer the note to the current entry
    channel.entry().note(note.key(), note.value());
    // all done
    return channel;
}


// injection of manipulator functions
// this template takes care of {endl}, {newline}, and the stateless manipulators from <iomanip>
template <typename severityT, template <class> typename proxyT>
inline auto
pyre::journal::operator<<(
    Channel<severityT, proxyT> & channel,
    Channel<severityT, proxyT> & (*manipulator)(Channel<severityT, proxyT> &) )
    -> Channel<severityT, proxyT> &
{
    // invoke the manipulator function with the {channel} as an argument
    return manipulator(channel);
}


// injection of everything else
template <typename itemT, typename severityT, template <class> typename proxyT>
auto
pyre::journal::operator<<(Channel<severityT, proxyT> & channel, const itemT & item)
    -> Channel<severityT, proxyT> &
{
    // inject the item in the channel and return the channel
    channel.entry().inject(item);
    // enable chaining
    return channel;
}


// flush with a decorator
template <typename severityT, template <class> typename proxyT, typename decoratorT>
auto
pyre::journal::operator<<(Channel<severityT, proxyT> & channel, const Flush<decoratorT> & flush)
    -> Channel<severityT, proxyT> &
{
    // inject the decorator
    channel << flush.decorator();
    // all done
    return channel.log();
}


// make a decorator flushable
template <typename decoratorT>
auto
pyre::journal::endl(decoratorT decorator) -> Flush<decoratorT>
{
    // easy enough
    return Flush(decorator);
}


// recognize the locator special signature and convert it into a flushable
auto pyre::journal::endl(__HERE_DECL__) -> Flush<Locator>
{
    return Flush(Locator(__HERE_ARGS__));
}


#endif

// end of file
