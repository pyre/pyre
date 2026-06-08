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
    << "something went wrong"
    << pyre::journal::endl(__HERE__);
```

Manipulators:

| Manipulator | Effect |
|-------------|--------|
| `endl` | flush and close the entry; always last |
| `here()` | inject the source location, inline or as the argument to `endl` |
| `newline` | a line break within an entry, without flushing |
| `indent` / `outdent` | adjust the indentation level of structured output |

After a `firewall_t` or `error_t` fires, always `break` or `return`; do not fall
through as if the logging were optional.
