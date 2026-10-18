# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# the parameters below are named {signal}, after what they carry, so the module goes by another
# name
import signal as signal_module
import socket
import threading
import weakref

# support
from . import exceptions
from .SocketPair import SocketPair


# declaration
class Signals:
    """
    The process-wide relay that delivers signals to event loops as ordinary read events

    The interpreter runs the handler of a signal on its main thread, between two bytecodes, at
    whatever point the program happens to be. That is the wrong place to do real work: the
    handler interrupts the event loop halfway through a pass, or one of its handlers halfway
    through its job. It is also not enough to stop a loop asleep in {select}: since python 3.5
    (PEP 475), {select} runs the handler and goes back to sleep, so a handler that merely asks
    the loop to stop is not heard until something else wakes the loop up.

    The relay uses the mechanism the standard library provides for this: it gives the
    interpreter one end of a socket pair through {signal.set_wakeup_fd}, and the interpreter
    writes the number of every signal it catches there, from its lowest level handler, before
    any python code runs. Event loops watch the other end like any other channel, so a loop
    asleep in {select} wakes the moment a signal arrives, and the relay invokes the handlers
    registered for it from the loop, between two events, like every other handler.

    The interpreter keeps one such descriptor per process, and only its main thread may set it
    or install signal handlers, so there is exactly one relay per process, shared by every
    event loop in it. A forked child starts without one: it gets back the signal dispositions
    the process had before the relay took charge, so a signal sent to the child can neither
    wake its parent through the inherited socket pair, nor run handlers that belong to the
    parent's event loops
    """

    # interface
    @classmethod
    def relay(cls):
        """
        Retrieve the relay of this process, building it on first use
        """
        # if this process does not have one yet
        if cls._relay is None:
            # build it
            cls._relay = cls()
        # and hand it off
        return cls._relay

    def watch(self, dispatcher, signal, call):
        """
        Arrange for {call} to be invoked from the event loop of {dispatcher} whenever the process
        receives {signal}

        The handler is invoked with the signal number as {signal}, and stays registered for as
        long as it returns a true value, just like the handlers of channel events
        """
        # take charge of the wakeup descriptor, if i haven't already
        self._claim(signal=signal)
        # if this is the first interest in {signal}
        if signal not in self._handlers:
            # carefully
            try:
                # take it over from whoever had it
                self._capture(signal=signal)
            # if that is not possible
            except exceptions.SignalRelayError:
                # and i am in charge of nothing else
                if not self._handlers:
                    # let go of the wakeup descriptor i just took
                    self._disown()
                # and let the caller know
                raise
        # add {call} to the pile of handlers of {signal}
        self._handlers.setdefault(signal, []).append(call)
        # if {dispatcher} is not watching my end of the socket pair yet
        if dispatcher not in self._loops:
            # ask it to
            dispatcher.whenReadReady(channel=self._reader, call=self._drain)
            # and remember that it does
            self._loops.add(dispatcher)
        # all done
        return

    def forget(self, signal, call=None):
        """
        Stop relaying {signal} to {call}, or to every one of its handlers when {call} is not
        given; a signal with no handlers left is handed back to whoever had it before
        """
        # get the handlers of {signal}
        pile = self._handlers.get(signal)
        # if there aren't any
        if pile is None:
            # there is nothing to do
            return
        # remove {call}, or all of them; by equality, since a bound method is a fresh object
        # every time it is looked up
        pile[:] = [] if call is None else [handler for handler in pile if handler != call]
        # if there are handlers left
        if pile:
            # i'm still in charge of {signal}
            return
        # otherwise, hand {signal} back
        self._release(signal=signal)
        # all done
        return

    def channel(self):
        """
        The channel the event loops watch, if the relay is in charge of any signals
        """
        # easy enough
        return self._reader

    def signals(self):
        """
        Generate the signals the relay is in charge of
        """
        # easy enough
        yield from self._handlers
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the handlers of each signal: signal -> list of callables
        self._handlers = {}
        # what each signal had before i took it over: signal -> handler
        self._previous = {}
        # the event loops watching my end of the socket pair, held weakly so i don't keep them
        # alive
        self._loops = weakref.WeakSet()
        # the two ends of the socket pair, while i own the wakeup descriptor
        self._reader = None
        self._writer = None
        # all done
        return

    # implementation details
    def _claim(self, signal):
        """
        Install my socket pair as the wakeup descriptor of the interpreter, unless it already is
        """
        # if i already own the wakeup descriptor
        if self._reader is not None:
            # nothing to do
            return
        # the interpreter lets only its main thread do this
        if threading.current_thread() is not threading.main_thread():
            # so complain
            raise exceptions.SignalRelayError(
                signal=signal, reason="signals can be relayed only from the main thread"
            )
        # make a socket pair; neither end is inherited by programs this process executes
        reader, writer = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        # the interpreter writes from its signal handler, which must never block
        writer.setblocking(False)
        # and i drain my end until it is empty, which must not block either
        reader.setblocking(False)
        # install the writer; a full buffer means a burst of signals the loop has not caught
        # up with, and dropping the extra bytes loses nothing, since the loop treats repeats
        # of a signal as one
        previous = signal_module.set_wakeup_fd(writer.fileno(), warn_on_full_buffer=False)
        # if somebody else owned the wakeup descriptor
        if previous != -1:
            # give it back
            signal_module.set_wakeup_fd(previous)
            # release my socket pair
            reader.close()
            writer.close()
            # and complain
            raise exceptions.SignalRelayError(
                signal=signal,
                reason=f"the wakeup descriptor of the interpreter is in use by fd {previous}",
            )
        # wrap my end so the event loops can watch it like any other channel
        self._reader = SocketPair(socket.AF_UNIX, socket.SOCK_STREAM, 0, fileno=reader.detach())
        # and hold on to the interpreter's end, so it stays open
        self._writer = writer
        # all done
        return

    def _capture(self, signal):
        """
        Take {signal} over from whoever had it
        """
        # carefully
        try:
            # install the handler that lets the interpreter know {signal} is of interest; the
            # interpreter writes to the wakeup descriptor only for signals that have one
            previous = signal_module.signal(signal, self._noted)
        # if {signal} cannot be caught, or does not exist
        except (OSError, ValueError) as error:
            # complain
            raise exceptions.SignalRelayError(signal=signal, reason=str(error)) from error
        # remember what {signal} had, so it can be handed back
        self._previous[signal] = previous
        # all done
        return

    def _release(self, signal):
        """
        Hand {signal} back to whoever had it before me, and let go of the wakeup descriptor if
        it was the last signal i was in charge of
        """
        # forget its handlers
        self._handlers.pop(signal, None)
        # and restore what it had
        signal_module.signal(signal, self._previous.pop(signal))
        # if i am still in charge of other signals
        if self._handlers:
            # keep the wakeup descriptor
            return
        # otherwise, let go of it
        self._disown()
        # all done
        return

    def _disown(self):
        """
        Give the wakeup descriptor back, and release my socket pair
        """
        # get my end of the socket pair
        reader = self._reader
        # if i don't own the wakeup descriptor
        if reader is None:
            # nothing to do
            return
        # go through the event loops that watch it
        for loop in list(self._loops):
            # and ask each one to stop, so nothing is left behind under a descriptor number
            # that is about to be recycled
            loop.forget(channel=reader)
        # i am no longer watched
        self._loops = weakref.WeakSet()
        # give the wakeup descriptor back; nobody owned it before me, or i would not own it
        signal_module.set_wakeup_fd(-1)
        # close both ends
        reader.close()
        self._writer.close()
        # and forget them
        self._reader = None
        self._writer = None
        # all done
        return

    def _drain(self, channel, **kwds):
        """
        Read the signals the interpreter caught, and invoke their handlers
        """
        # the signals, in the order they first arrived
        caught = []
        # keep reading
        while True:
            # carefully
            try:
                # whatever is there
                data = channel.recv(256)
            # until there is nothing left
            except BlockingIOError:
                # move on
                break
            # if the other end went away
            if not data:
                # stop reading
                break
            # go through the signal numbers
            for number in data:
                # a signal that arrived more than once since the last pass is handled once,
                # the way the kernel itself merges repeats of a pending signal
                if number not in caught:
                    # add it to the pile
                    caught.append(number)
        # go through the signals
        for number in caught:
            # get their handlers; a signal i have let go of since it arrived has none
            pile = self._handlers.get(number, [])
            # invoke each one, in a snapshot of the pile, since handlers may register more
            for handler in list(pile):
                # and if it is not interested in the next one
                if not handler(signal=number):
                    # stop relaying {number} to it
                    self.forget(signal=number, call=handler)
        # keep watching, for as long as i am in charge of any signals
        return self._reader is not None

    def _reset(self):
        """
        In a forked child, undo everything the relay of the parent did
        """
        # if i don't own the wakeup descriptor
        if self._reader is None:
            # there is nothing to undo
            return
        # hand every signal back to what it had before i took it over
        for signal, previous in self._previous.items():
            # one by one
            signal_module.signal(signal, previous)
        # give the wakeup descriptor back
        signal_module.set_wakeup_fd(-1)
        # close my copies of the socket pair; the parent still holds its own
        self._reader.close()
        self._writer.close()
        # and forget everything
        self._reader = None
        self._writer = None
        self._handlers = {}
        self._previous = {}
        self._loops = weakref.WeakSet()
        # all done
        return

    @staticmethod
    def _noted(signal, frame):
        """
        The handler the interpreter runs when a relayed signal arrives; the relay does the work
        from the event loop, so there is nothing to do here
        """
        # all done
        return

    @classmethod
    def _forked(cls):
        """
        Invoked in every child forked by this process
        """
        # if there is a relay
        if cls._relay is not None:
            # it belongs to the parent, so undo it
            cls._relay._reset()
        # all done
        return

    # private data
    _relay = None  # the relay of this process


# every child forked by this process undoes the relay of its parent
os.register_at_fork(after_in_child=Signals._forked)


# end of file
