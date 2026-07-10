// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the machinery this file needs, and nobody else does
namespace pyre::postgres::py {
    // turn a python mapping into a connection specification
    static auto specification(const py::dict & spec) -> parameters_t
    {
        // room for the parameters
        parameters_t parameters;
        parameters.reserve(spec.size());
        // walk the mapping
        for (const auto & item : spec) {
            // a parameter whose value is {None} is one the caller did not supply; libpq has its
            // own defaults for every one of them, and they are better than anything we could
            // invent, so leave it out entirely rather than sending it an empty string
            if (item.second.is_none()) {
                continue;
            }
            // everything else goes as a name and a value, kept apart. a password with a space
            // in it, spliced into a conninfo string, silently becomes a password and a garbage
            // keyword; the bindings this package replaces built the string that way
            parameters.emplace_back(
                item.first.cast<string_t>(), py::str(item.second).cast<string_t>());
        }
        // hand them off
        return parameters;
    }
} // namespace pyre::postgres::py


// add the bindings for a session with the back end
//
// every call below that waits on the server lets go of the interpreter lock while it waits. the
// bindings this package replaces held it throughout, so a single slow query stopped every thread
// in the process
void
pyre::postgres::py::connection(py::module & m)
{
    // the class
    auto cls = py::class_<Connection>(
        // in scope
        m,
        // the name
        "Connection",
        // the docstring
        "a session with the postgres back end");

    // build one out of a mapping of parameters
    cls.def(
        // the implementation
        py::init([](const py::dict & spec) {
            // read the mapping while we still hold the lock
            const auto parameters = specification(spec);
            // and let go of it while libpq talks to the server, which may take a while
            py::gil_scoped_release release;
            // open the session
            return Connection(parameters);
        }),
        // the signature
        "parameters"_a,
        // the docstring
        "open a session described by the given {parameters}");

    // or out of a conninfo string, for a caller that has one already
    cls.def(
        // the implementation
        py::init([](view_t conninfo) {
            // let go of the lock while libpq talks to the server
            py::gil_scoped_release release;
            // open the session
            return Connection(conninfo);
        }),
        // the signature
        "conninfo"_a,
        // the docstring
        "open a session described by a conninfo string or a postgres uri");

    // structure
    cls.def_property_readonly(
        // the name
        "status",
        // the implementation
        &Connection::status,
        // the docstring
        "whether the session is up");

    cls.def_property_readonly(
        // the name
        "ok",
        // the implementation
        &Connection::ok,
        // the docstring
        "whether the session is up and has not been closed");

    cls.def_property_readonly(
        // the name
        "message",
        // the implementation
        [](const Connection & self) -> string_t { return string_t(self.message()); },
        // the docstring
        "whatever libpq has to say about the last thing that went wrong");

    // what the session is
    cls.def_property_readonly(
        // the name
        "database",
        // the implementation
        [](const Connection & self) -> string_t { return string_t(self.database()); },
        // the docstring
        "the database this session is talking to");

    cls.def_property_readonly(
        // the name
        "user",
        // the implementation
        [](const Connection & self) -> string_t { return string_t(self.user()); },
        // the docstring
        "the role this session is talking as");

    cls.def_property_readonly(
        // the name
        "host",
        // the implementation
        [](const Connection & self) -> string_t { return string_t(self.host()); },
        // the docstring
        "where the server is");

    cls.def_property_readonly(
        // the name
        "port",
        // the implementation
        [](const Connection & self) -> string_t { return string_t(self.port()); },
        // the docstring
        "the port the server is listening on");

    cls.def_property_readonly(
        // the name
        "backend",
        // the implementation
        &Connection::backend,
        // the docstring
        "the process id of the back end serving this session");

    cls.def_property_readonly(
        // the name
        "socket",
        // the implementation
        &Connection::socket,
        // the docstring
        "the descriptor underneath the session, for a caller that wants to wait on it");

    cls.def_property_readonly(
        // the name
        "protocol",
        // the implementation
        &Connection::protocol,
        // the docstring
        "the version of the wire protocol in use");

    cls.def_property_readonly(
        // the name
        "server",
        // the implementation
        &Connection::server,
        // the docstring
        "the version of the server, as a number: 16.2 is 160002");

    cls.def_property_readonly(
        // the name
        "transaction",
        // the implementation
        &Connection::transaction,
        // the docstring
        "where the session stands with respect to its transaction");

    cls.def(
        // the name
        "setting",
        // the implementation
        [](const Connection & self, view_t name) -> string_t { return string_t(self.setting(name)); },
        // the signature
        "name"_a,
        // the docstring
        "the current value of the server setting {name}");

    // synchronous execution
    cls.def(
        // the name
        "exec",
        // the implementation
        &Connection::exec,
        // the signature
        "statement"_a,
        // let go of the lock while the server works
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "run {statement}, which may hold several commands, and hand back what the server said");

    cls.def(
        // the name
        "execute",
        // the implementation
        [](const Connection & self, view_t statement, const py::args & args) -> Result {
            // render the arguments while we still hold the lock
            const auto rendered = arguments(args);
            // and let go of it while the server works
            py::gil_scoped_release release;
            // the values travel beside the statement rather than inside it, so nothing a caller
            // passes here can change what the statement does
            return self.execParams(statement, rendered);
        },
        // the signature
        "statement"_a,
        // the docstring
        "run {statement}, with its $1, $2, ... placeholders filled in from the {arguments}");

    cls.def(
        // the name
        "prepare",
        // the implementation
        &Connection::prepare,
        // the signature
        "name"_a, "statement"_a,
        // let go of the lock while the server works
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "teach the server {statement} under the given {name}, so it need only plan it once");

    cls.def(
        // the name
        "execPrepared",
        // the implementation
        [](const Connection & self, view_t name, const py::args & args) -> Result {
            // render the arguments while we still hold the lock
            const auto rendered = arguments(args);
            // and let go of it while the server works
            py::gil_scoped_release release;
            // run what it was taught
            return self.execPrepared(name, rendered);
        },
        // the signature
        "name"_a,
        // the docstring
        "run the statement the server was taught under {name}");

    // asynchronous execution
    cls.def(
        // the name
        "send",
        // the implementation
        &Connection::send,
        // the signature
        "statement"_a,
        // let go of the lock while the socket drains
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "send {statement} off, and do not wait for it");

    cls.def(
        // the name
        "sendParams",
        // the implementation
        [](const Connection & self, view_t statement, const py::args & args) -> void {
            // render the arguments while we still hold the lock
            const auto rendered = arguments(args);
            // and let go of it while the socket drains
            py::gil_scoped_release release;
            // send it off
            self.sendParams(statement, rendered);
        },
        // the signature
        "statement"_a,
        // the docstring
        "send {statement} off with its placeholders filled in, and do not wait for it");

    cls.def(
        // the name
        "consume",
        // the implementation
        &Connection::consume,
        // let go of the lock while we read the socket
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "read whatever the server has sent so far; a loop over {busy} that omits this never ends");

    cls.def_property_readonly(
        // the name
        "busy",
        // the implementation
        &Connection::busy,
        // the docstring
        "whether the answer to the statement in flight is still incomplete");

    cls.def(
        // the name
        "result",
        // the implementation
        &Connection::result,
        // let go of the lock, since this blocks until the next result is complete
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "the next result the server produced, or {None} when it has produced them all; this does "
        "not raise on a failed statement, so that the collection may be drained. ask the result "
        "to {check} itself once it has");

    cls.def(
        // the name
        "cancel",
        // the implementation
        &Connection::cancel,
        // let go of the lock while the request travels
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "ask the server to give up on the statement in flight");

    cls.def(
        // the name
        "nonblocking",
        // the implementation
        &Connection::nonblocking,
        // the signature
        "state"_a,
        // the docstring
        "whether the calls that send do so without waiting for the socket to drain");

    cls.def(
        // the name
        "flush",
        // the implementation
        &Connection::flush,
        // let go of the lock while the socket drains
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "push whatever is queued out to the server; zero when it all went, one when it did not");

    // messages from other sessions
    cls.def(
        // the name
        "notification",
        // the implementation
        &Connection::notification,
        // the docstring
        "the next message this session has collected, or {None}; call {consume} first");

    // quoting
    cls.def(
        // the name
        "escapeLiteral",
        // the implementation
        &Connection::escapeLiteral,
        // the signature
        "text"_a,
        // the docstring
        "quote {text} so that it may stand where a literal may stand");

    cls.def(
        // the name
        "escapeIdentifier",
        // the implementation
        &Connection::escapeIdentifier,
        // the signature
        "name"_a,
        // the docstring
        "quote {name} so that it may stand where an identifier may stand");

    // lifecycle
    cls.def(
        // the name
        "reset",
        // the implementation
        &Connection::reset,
        // let go of the lock while libpq reconnects
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "close the session and open a new one with the same parameters");

    cls.def(
        // the name
        "close",
        // the implementation
        &Connection::close,
        // let go of the lock while the socket closes
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "hand the session back now; every copy of me observes this and refuses to be used after");

    // contextual conversion to {bool}, true when the session is up
    cls.def(
        // the name
        "__bool__",
        // the implementation
        &Connection::ok,
        // the docstring
        "whether the session is up and has not been closed");

    // the interactive representation
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Connection & self) -> string_t {
            // a session that has been closed cannot be asked anything about itself
            if (!self.ok()) {
                return "<postgres.Connection: closed>";
            }
            // and one that is up knows where it is
            return "<postgres.Connection to '" + string_t(self.database()) + "' as '"
                 + string_t(self.user()) + "'>";
        },
        // the docstring
        "a human readable summary of this session");

    // all done
    return;
}


// end of file
