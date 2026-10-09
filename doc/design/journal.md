<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# journal: the diagnostics framework

`journal` is the pyre diagnostics framework. It works identically from Python and
C++, and predates and is preferred over Python's `logging` module. The basic
entity is a named **channel**; all state is keyed by the name and shared across
every call site that opens a channel with the same name, so channels never need to
be passed around.

## Channel types

| Channel    | Active | Fatal | Purpose |
|------------|--------|-------|---------|
| `debug`    | no     | no    | development diagnostics; a no-op in release builds |
| `info`     | yes    | no    | ordinary progress reporting to the user |
| `warning`  | yes    | no    | something is off but the run can proceed |
| `error`    | yes    | yes   | a user mistake; report and abort |
| `firewall` | yes    | yes   | an assertion: a bug, an impossible state, a broken invariant |

**`error` vs `firewall`.** `error` is for the user's mistakes (bad input, missing
environment). `firewall` is for the developer's: if it fires, the code must change,
either because a real inconsistency was caught or the firewall itself is wrong.
Never mix them.

## Naming

Channel names are dotted strings rooted at the project name: `qed.archives.location`.
Names reflect the *activity or concern* being logged, not the class or component
doing the work, so a workflow spread across several components can write to one
shared channel and be followed as a unit. The hierarchy is respected: deactivating
`qed.archives` also silences `qed.archives.location` unless the latter has been
explicitly reactivated — so a user can silence a whole subsystem with one call.

Choose names deliberately; do not derive them mechanically from `__name__` or a
component's `family` string.

## Python API

Factories (each takes the channel name):

```python
journal.debug, journal.info, journal.warning, journal.error, journal.firewall
```

Channel methods — all return the channel, so they **chain**:

| Method | Effect |
|--------|--------|
| `line(message="")` | append one line to the entry; does **not** flush |
| `log(message="", **kw)` | append the optional message, then record/flush the entry |
| `report(iterable)` | append several lines at once |
| `indent(levels=1)` | increase the indentation of subsequent lines |
| `outdent(levels=1)` | decrease it; pair around a block |
| `activate()` / `deactivate()` | toggle output (hierarchy-aware, see *Naming*) |

Channel attributes: `active`, `fatal` (booleans); `name`, `severity` (identity);
`detail` (verbosity level); `notes` (a key/value mapping carried with the entry).

The notes are the one place for metadata, the journal's own included: every entry
carries `channel`, `severity` and `application`, one flushed with a location carries
`filename`, `line` and `function`, and one shipped to another process by a courier
carries `pid`, `seq`, `time` and `host` (see `courier.md`). Those ten names are reserved;
a note of the same name from a call site is overwritten. Anything else is the call
site's to use.

Two idioms:

```python
# one-shot
journal.info("qed.archives.location").log(f"locating {product}")

# accumulate, then flush with log()
channel = journal.info("mm.pkgdb")
channel.line("building the package database")
channel.indent()
channel.line(f"prefix: {prefix}")
channel.outdent()
channel.log()

# abort on a user mistake (error is fatal by default)
error = journal.error("mm.pkgdb")
error.line("no active conda environment found")
error.log()
```

Open a fresh channel at the call site every time; never cache one as a class or
instance attribute. `journal` is part of pyre and is guaranteed available once the
framework has bootstrapped, so its import never needs guarding.

## C++ API

The same model. Channel types follow the `pyre::journal::{severity}_t`
convention: `info_t`, `warning_t`, `error_t`, `firewall_t`, `debug_t`. Entries are
built with the streaming operator and closed with a manipulator:

```cpp
auto channel = pyre::journal::firewall_t("qed.a.b.c");
channel
    << pyre::journal::at()
    << "something went wrong"
    << pyre::journal::endl;
```

Manipulators:

| Manipulator | Effect |
|-------------|--------|
| `endl` | flush and close the entry; always last |
| `at()` | record the source location of the entry, as the compiler reports it; entries start with it |
| `newline` | a line break within an entry, without flushing |
| `indent` / `outdent` | adjust the indentation level of structured output |

After a `firewall_t` or `error_t` fires, always `break` or `return`; do not fall
through as if the logging were optional.

`endl` hands back the outcome of the entry. For `error_t` and `firewall_t` that is
the exception that states the condition, whether or not the channel is fatal or
active, so an entry can be raised directly:

```cpp
throw channel << pyre::journal::at() << "the grid has no cells" << pyre::journal::endl;
```

### The developer channels in release builds

`debug_t` and `firewall_t` are the developer channels. In release builds they are
`null_t`, which accepts the same expressions and compiles to nothing, so they cost
nothing where they are off. Which one a translation unit gets is settled when
`pyre/journal.h` is included:

| Build settings | Developer channels |
|----------------|--------------------|
| `PYRE_CORE` (pyre itself) | live |
| `JOURNAL_DEBUG` set to 1 | live |
| `JOURNAL_DEBUG` set to 0 | null |
| otherwise, `NDEBUG` | null |
| otherwise, `DEBUG` | live |
| none of the above | null |

The rows are checked in order and the first match decides, so `JOURNAL_DEBUG` wins
over `DEBUG` and `NDEBUG`, and `NDEBUG` wins over `DEBUG`. `-DJOURNAL_DEBUG` on the
command line sets it to 1; a definition with no value is an error. pyre itself is
always built with the developer channels live, and setting `JOURNAL_DEBUG` to 0
there is an error.

After the include, `JOURNAL_DEBUG` is always defined: 1 when the developer channels
are live and 0 when they are null. Code that only compiles against the live
channels goes behind it. Raising a firewall entry is such code, since `null_t`
hands back nothing that can be thrown:

```cpp
#if JOURNAL_DEBUG
    throw firewall << pyre::journal::at() << "nasty bug" << pyre::journal::endl;
#endif
```

`error_t` is never null, so raising an error entry needs no guard.

The `JOURNAL_DEBUG` environment variable is unrelated: it names the debug channels
to activate when the application starts.

## Devices

A device is where entries end up. There are three places to install one, and a channel
uses the first it finds: its own device, then the default of its severity, then the
global default kept by the chronicler.

```python
# the global default
journal.chronicler.device = journal.file(path="run.log")
# the default of a severity
journal.warning.setDefaultDevice(journal.cerr())
# the device of one channel
journal.info("qed.archives").device = journal.trash()
```

The stock devices are the console (`cout`), the error console (`cerr`), files (`file`),
the trash can (`trash`), and the devices that forward entries to others: a splitter
hands every entry to each of the devices attached to it, a tee is a splitter over the
console and a set of files, and a courier ships entries to another process and can also
hand them to a mirror (see `courier.md`). Forwarding devices nest: a splitter can feed
another splitter, or be the mirror of a courier.

```python
log = journal.file(path="run.log")
splitter = journal.splitter(outputs=[journal.cout()])
splitter.attach(device=log)
splitter.detach(device=log)
courier.mirror = None
```

`attach` adds a device to a splitter, `detach` removes every attachment of a device,
and the mirror of a courier can be replaced, or removed by setting it to `None`. A
splitter skips empty attachments.

### Devices implemented in python

A device can be written in python by deriving from `journal.device` and implementing
`alert`, `help` and `memo`. With the C++ journal, such a device is held by C++ state
that outlives the interpreter, so the journal has to let go of it while the interpreter
can still release it:

- Every device says whether it is **foreign**, implemented outside C++; devices written
  in python are, the stock ones are not.
- `journal.chronicler.detachForeign()` walks every device the journal holds, including
  the outputs of splitters and the mirrors of couriers at any depth, and lets go of the
  foreign ones. A foreign global default is replaced by a console; a foreign device
  anywhere else is forgotten, so the channels fall back on the devices above them.
- The C++ journal calls `detachForeign` from an `atexit` hook registered when it is
  imported. Hooks registered later, by pyre or by the application, run first, so they
  can still log to python devices.

What the journal cannot reach, it cannot release: C++ code of a client that keeps its
own reference to a python device, or to a forwarding device that holds one, must let go
of it before the interpreter shuts down.


<!-- end of file -->
