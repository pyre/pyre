<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# components and the configuration store in pyre 2.0

A proposal for the second version of the component system: two configuration stores in
place of one, a configuration syntax that says which store a setting is meant for, a
lifecycle for component instances that admits creation, renaming, rebinding, and release,
and a framework executive that is itself a component. The document is written to be
discussed one numbered item at a time. Every section, list item, and open question carries
a number that can be cited on its own, e.g. "4.2.3" or "Q4".

Status: draft for discussion, 2026-09-23. Nothing in it is implemented. Where the proposal
departs from what the code does today, section 3 records what the code does, so that the
departure is deliberate.

## 1. Purpose

1.1. The first version of the component system was built for programs that assemble their
configuration from a fixed set of sources, build their components once, and run. It has
been asked to serve programs that create components before naming them, connect and
disconnect them repeatedly, discard them, and save the result as a document: the flow
experiment, its graphical editor, the merlin builder, and the qed pipeline. This proposal
restates the design so that both kinds of program are served by the same rules.

1.2. The proposal is free to break the first version. Configuration files written for the
first version are long lived, so the parts of the breakage that are mechanical are handled
by a migration tool (section 9.3), and the parts that are not are reported by that tool
rather than silently accepted.

1.3. The proposal covers the Python packages `pyre.components`, `pyre.framework`,
`pyre.config`, and the parts of `pyre.traits` and `pyre.calc` that hold configuration
values. It does not cover the C++ libraries, the schema and database packages, or the
contents of `pyre.flow` beyond what it asks of the base framework (section 8).

## 2. Vocabulary

Many of the words in this area are used for several different things in the current code.
This section fixes one meaning per word for the rest of the document. Where the code uses
a word differently, the difference is noted.

2.1. **Package.** A Python package that has registered with the framework, e.g. `pyre`,
`gauss`, `qed`. A package has a name, a home directory, and a set of configuration files
of its own.

2.2. **Family.** The dotted name under which a component class or a protocol is declared,
e.g. `gauss.functors.exp`. Its first segment is the name of a package. The family is the
address of the class in the class store (section 4.1). A class without a family is
private to the process and has no address.

2.3. **Class record.** The Python class object of a component or protocol, as decorated by
its metaclass. The current code also calls this a "class" or a "component class". The
term "component" alone is avoided in this document, because the code uses it for the
class, for the instance, and for the base class `pyre.component`.

2.4. **Trait.** A declared attribute of a class record whose value is subject to
configuration: a property, which holds a plain value, or a facility, which holds an
instance of some class that implements a protocol. A behavior is a trait too but is not
configurable and plays no part here.

2.5. **Instance.** An object built from a class record. An instance has an identity
(section 6.1), may have a name, and holds one value per trait.

2.6. **Name.** A string that a client, a configuration file, or the framework assigns to an
instance. Names are optional, can be assigned after construction, and can be changed. A
name is the address of the instance in the instance store (section 4.2). Today the name
is a construction argument that cannot change; that is the departure.

2.7. **Part.** An instance held as the value of a facility of another instance. The
instance that holds it is the part's **host**. A part that was built by the framework to
satisfy a facility, rather than supplied by a client, is an **owned part**, and its name
is the name of its host followed by the name of the facility, e.g. `station.sensor`.

2.8. **Ownership path.** A name of the form `host.facility.facility...`, i.e. the name of
an owned part of an owned part. The instance store is organized along these paths.

2.9. **Binding.** The association of a facility of a host with the part that is its value.
To **bind** is to establish it, to **unbind** is to dissolve it, to **rebind** is to
replace one part by another. Today the word "bind" is also used for the moment a trait
value is first evaluated; that meaning is not used here.

2.10. **Setting.** A value that a source has supplied for a path, together with the
source's priority and the location it came from. The current code calls the value holder
a "slot"; that word is not used in this document, because the flow editor uses it for
something else.

2.11. **Source.** Where settings come from: a class declaration, a package configuration
file, a user configuration file, the command line, a constructor argument, an assignment
to an instance attribute, or the framework itself. Each source has a **priority**, and a
setting of higher priority replaces one of lower priority for the same path.

2.12. **Path.** A dotted string that addresses a setting in one of the stores, e.g.
`gauss.functors.exp.a` in the class store, `two.a` in the instance store.

2.13. **Store.** A table from paths to settings. This proposal has two: the **class store**
(section 4.1) and the **instance store** (section 4.2). The current code has one, the
name server.

2.14. **Guard.** A condition attached to a setting in the instance store that says the
setting applies only if the instance at its path is of a given family (section 4.4).

2.15. **Claim.** The moment a class record or an instance takes possession of a path in a
store and the settings under it. A setting whose path has never been claimed is
**unclaimed**.

2.16. **Kernel.** The plain objects that the framework needs before any class record can
be declared: the two stores, the registrar, and the configurator (section 7.1).

2.17. **Executive.** The object that owns the kernel and the runtime information: the
host, the user, the terminal, the environment. In this proposal it is an instance named
`pyre` (section 7.2).

2.18. **Session state.** Data attached to an instance that is not the value of any trait,
e.g. the position of a node in a diagram (section 6.7).

## 3. What the current implementation does

These are measured facts, not interpretations. The scripts that produce them are in the
lifecycle sandbox, `~/tmp/pyre/sandbox/{reuse,probe,classes}.py`, and were run against
the build of 2026-09-23.

3.1. **One store holds everything.** Packages, class records, instances, trait values, and
framework settings such as the configuration path all live in one hierarchy keyed by
dotted names. There is no operation that removes an entry. A lookup of a missing name
leaves a permanent marker under that name.

3.2. **A setting may precede what it configures.** A setting that arrives before its class
or instance exists is held untyped and is re-typed in place when the class or instance
claims the path. This is what makes configuration files, the command line, and deferred
assignments work, and it must survive the redesign.

3.3. **A class record is a source of defaults.** Declaring a class with a family places
the class record under the family and one setting per trait under `family.trait`. An
instance copies the values of these settings when it is built. An instance built before a
class default changed keeps the old value; one built after gets the new one. A subclass
with its own family refers to its ancestor's settings rather than copying them.

3.4. **The store holds every named instance strongly.** Registering an instance stores the
instance object itself as the value under its name. A named instance is therefore never
released for the life of the process.

3.5. **Building under a name that is in use returns the existing instance.** The
construction call looks the name up in the registrar first and returns any hit before
depositing constructor arguments or running any hook. Constructor trait values are
discarded without any report. The priority scheme would have let them take: a later
deposit at construction priority outranks an earlier one.

3.6. **Two different classes built under one name share their settings.** The registrar
enforces uniqueness per class; the store is global. The second instance replaces the first
as the value under the name, and both read and write the same trait settings.

3.7. **A name keeps the settings of its previous occupant.** Rebinding a facility to a class
of a different family builds a new part under the same name; the new part inherits every
setting of the old one whose trait name it shares, including settings that were only the
old part's defaults. Binding back later builds a third part that inherits the settings
of the first. Settings for traits the current occupant does not have stay under the name
indefinitely.

3.8. **An instance named like its family displaces the class record.** The instance becomes
the value under the family and shares the trait settings with the class, so assignments
to the instance change the defaults of every instance built afterwards. Nothing reports
this.

3.9. **Unclaimed settings are never reported.** A misspelled trait under a real family, or a
section for a name that is never used, stays in the store at its source's priority for
the life of the process, with no diagnostic.

3.10. **Named and unnamed instances take different paths.** A named instance keeps its
settings in the store and receives deferred assignments; an unnamed instance keeps them
in a private table with no record of priority or location, so the introspection that
reports where a value came from returns nothing for it.

3.11. **Some hooks are not what they say.** The hook documented as running before any
configuration event runs last. The hook meant to release resources has no caller. The
class-level initialization hook fires for protocols only.

3.12. **Configuration files cannot say which store they mean.** A bare section, `[sample]`
or `sample:`, produces plain assignments that could be class defaults or instance
settings; whichever claims the path first gets them. Only sections of the form
`family # name` are unambiguous, and those are deferred until an instance of that name
and family is configured, by an exact match on the class.

3.13. **Consumers work around the framework.** The flow experiment names every node with a
generated identifier so that its nodes can be observed. The flow editor never builds
instances at all, because it has no name to give them. The merlin builder keeps its own
dictionary from names to assets because the store cannot answer "the instance called
this". All three keep their products in container traits that the flow engine does not
recognize as bindings.

## 4. Two stores

4.1. **The class store.**

4.1.1. The class store holds packages and class records. Its paths follow the package and
family structure: `gauss` is a package, `gauss.functors.exp` is a class record,
`gauss.functors.exp.a` is the default of trait `a` of that class.

4.1.2. Entries in the class store are permanent. A class record cannot be undeclared, so
nothing in this store is ever released. This is the one place where the current store's
"no removal" rule is correct.

4.1.3. A setting under a family is validated when the family is claimed. Once
`gauss.functors.exp` is declared, a setting at `gauss.functors.exp.b` where `b` names no
trait of the class is an error in the source that supplied it, and is reported as such
(section 4.5).

4.1.4. The class store is also the vocabulary of facility bindings. A short binding such as
`integrand = line` under a facility whose protocol has family `quad.functors` is resolved
by looking up `quad.functors.line` in the class store. This is how the current code
resolves such bindings and it does not change.

4.1.5. The class store is where the catalog of what can be built comes from: a request for
the classes that implement a protocol is answered from this store and the registrar.

4.2. **The instance store.**

4.2.1. The instance store holds instances and their settings. Its paths follow instance
names and ownership paths: `two` is an instance, `two.a` its trait `a`,
`station.sensor` the part bound to facility `sensor` of `station`,
`station.sensor.gain` a trait of that part.

4.2.2. An entry in the instance store lives as long as something holds the instance
(section 6.5). The store does not hold instances strongly.

4.2.3. The settings under a name outlive the instance that carried them, subject to the
rules of section 6.5.3, so that the next instance built under the name is configured the
same way. This preserves the behavior of section 3.2 for instances.

4.2.4. A trait setting of an instance that has never been assigned refers to the
corresponding default in the class store, in the same way that a subclass refers to its
ancestor's default today (section 3.3). An assignment replaces the reference with a
value. This is the one change of observable behavior in this section: an instance that
was never assigned a value for a trait follows a later change of the class default. See
Q1.

4.3. **What each store answers.**

4.3.1. "What is the default for this trait of this class" is a class store question.

4.3.2. "What is the value of this trait of this instance" is an instance store question,
which falls through to the class store per 4.2.4.

4.3.3. "Which instance is called this" is an instance store question. It replaces the
registrar's linear search by name (section 3.5).

4.3.4. "Which class is called this" and "which classes implement this protocol" are class
store questions.

4.4. **Guarded settings.**

4.4.1. A setting written as `name@family.trait = value` (section 5) is stored in the
instance store at `name.trait` with the guard `family`. It applies only when the instance
at `name` is of that family.

4.4.2. Several guarded settings for the same path with different guards may coexist. When
an instance claims the path, the settings whose guards it satisfies apply, in priority
order; the rest stay dormant and apply if a later occupant satisfies them.

4.4.3. A guard is satisfied by pedigree: the instance's class is the guard's family, or
derives from it, or, when the guard names a protocol, implements it. Today the match is by
identity of the class, so a subclass silently fails the guard (section 3.12).

4.4.4. Guarded settings live in the store, not in a side table. They are visible to the
tools that list and dump the store, and they are written out by persistence (section 6.8).
Today they are held in a list inside the configurator, keyed by the instance's address,
and are invisible to everything else.

4.5. **Unclaimed settings and reporting.**

4.5.1. A setting in the class store whose family is declared but whose trait does not
exist is reported at the moment the family is declared.

4.5.2. A setting in the class store whose family is never declared, and a setting in the
instance store whose name is never claimed, are reported on request and at the end of the
process. They are never errors by default.

4.5.3. A guarded setting in the instance store can be validated against the traits of its
guard's family as soon as that family is declared, whether or not an instance ever claims
the path. A setting without a guard cannot be validated until an instance claims it. This
is the incentive to write guards.

4.5.4. Applications choose the reporting policy: silent, a report at exit, or an error.
The framework default is a report at exit on a warning channel.

## 5. Configuration syntax

5.1. **The section grammar.**

5.1.1. A section header, and a fully qualified path on the command line, has the form
`[name][@[family]]`, where both halves are optional but not both empty:

| spelling | meaning | store |
|---|---|---|
| `two` | the instance named `two` | instance |
| `two@gauss.functors.exp` | the instance named `two`, provided it is of that family | instance, guarded |
| `@gauss.functors.exp` | the class record of that family | class |
| `#two` | the instance named `two`, spelled with an explicit marker | instance |

5.1.2. A leading `@` routes the section to the class store; anything else routes it to the
instance store. The routing is decided by the parser, not by which store claims the path
first (section 3.12).

5.1.3. `name` may be an ownership path, `station.sensor`, or a name a file declares on its
own, `two`. Both are instance store paths.

5.1.4. The `#name` spelling exists for authors who want an explicit reminder. It must be
quoted in yaml and toml, where `#` begins a comment, and it is not the recommended
spelling.

5.1.5. Sections nest. A section inside a section prefixes its path with the enclosing
path, and its guards accumulate, exactly as the current `family # name` sections do.

5.2. **Values that name instances.** The value of a facility follows the same grammar: `two`
is the instance named `two`, made from the protocol's default class if it does not exist;
`@quad.functors.const` is a fresh owned part of that class; `two@quad.functors.const` is
the instance named `two`, of that class, built if absent and checked if present. Shelf
addresses keep the `#symbol` fragment, `import:gauss.shapes#box`, because that fragment
locates a symbol in a module or file, which is a different operation from naming an
instance.

5.3. **The formats.**

5.3.1. `cfg` and `pfg` are pyre's own formats. Their section headers admit the grammar of
5.1 without quoting, and their values are bare strings. Both are kept, both change their
header syntax from `family # name` to `name@family`.

5.3.2. `yaml` is kept for reading and writing. A key beginning with `@` or `#` must be
quoted; a key of the form `two@family` need not be. The editor that writes yaml quotes
such keys.

5.3.3. `toml` is added for reading, through the standard library. Every key that contains
a marker is quoted, because bare toml keys admit only letters, digits, underscore, and
hyphen, and every string value is quoted. The standard library parser reports no line
numbers, so settings read from toml carry the file as their location but not the line.

5.3.4. `pml` is removed.

5.3.5. The command line uses the same grammar: `--two.a=5` and `--@gauss.functors.exp.a=5`.

5.4. **Migration of first-version files.** A tool rewrites `family # name` headers to
`name@family` and `family#name` values to `name@family`. For a bare section it consults
the registrar, after importing the package the section's first segment names: a section
that is a declared family becomes `@family`; one that is not stays bare; one that is both
a declared family and, by the rest of the file, an instance name is reported for the
author to resolve (section 3.8).

## 6. The lifecycle of an instance

6.1. **Identity and naming.**

6.1.1. Every instance receives an identifier at construction that is unique for the life
of the process. The identifier is not a name and does not appear in configuration files.

6.1.2. A name is optional at construction. An unnamed instance is fully functional: it has
settings with priority and location, it can be observed, it can be bound as a part.

6.1.3. An instance can be given a name after construction, and its name can be changed.
Naming an instance claims the path in the instance store and applies the settings found
there, in priority order, as if the instance had been built under that name. Renaming
releases the old path per section 6.5 and claims the new one.

6.1.4. A framework naming service supplies names on request: readable, stable within a
process, and distinct from any path a file is likely to declare. The registrar's existing
hook for name generators is the attachment point; nothing registers with it today.

6.1.5. An owned part is named by its ownership path when it is built (section 2.7). A part
supplied by a client keeps the client's name for it.

6.1.6. Naming or renaming an instance after its construction applies the settings under the
new name after `__init__` has already run (6.2.5). The framework applies them as one
batch, fires the trait-modified hook for each trait whose value changed, and then fires
the batch hook of Q8, so that a class can recompute whatever it derived from its traits
in `__init__`. A class that derives such state and does not implement the batch hook
keeps stale derived state, as it does today after any assignment made after construction.

6.2. **Construction.**

6.2.1. Named and unnamed instances are built by the same sequence. They differ only in
whether their settings are addressed in the instance store from the start.

6.2.2. The sequence is: allocate the instance and its identifier; attach its settings,
referring to class defaults per 4.2.4; apply constructor trait arguments at construction
priority; if a name was given, claim it and apply the settings under it; run the
configuration hook; run the class's own constructor; run the initialization hook and
collect its errors; register the instance; run the registration hook; mark the instance
complete.

6.2.3. Constructor arguments that name traits, under any alias, are applied through the
same operation as any other assignment, at construction priority. The separate channel
that the current code uses for unnamed instances goes away.

6.2.4. The hooks keep their names and are made to run in the order their documentation
states. The finalization hook is wired to release (section 6.5.4).

6.2.5. The sequence of 6.2.2 preserves a guarantee the current framework makes and that
its consumers rely on: when `__init__` runs, every setting that addresses the instance at
that moment has been applied and typed, and no hook has been skipped, so that `self.trait`
inside `__init__` yields the configured value and `self.part` yields a finished part.
The guarantee is about the moment of construction. It has never meant that the
configuration is final: a setting that addresses the instance later, by assignment, by a
configuration file loaded afterwards, by naming (6.1.6), by reconfiguration (6.3.1), or
by a change of a class default that the instance never overrode (4.2.4), is applied
through the notifications of 6.1.6, not by running `__init__` again.

6.3. **Construction under a name that is in use.**

6.3.1. If the instance store holds a live instance under the name and it is of the same
class, the call returns that instance after applying the constructor trait arguments at
construction priority, which outranks the earlier ones, firing the trait-modified hook
for each changed trait, and then the batch hook of Q8. The call is a reconfiguration, not
a silent lookup. Its `__init__` ran with the earlier arguments (6.2.5), so a class that
derives state in `__init__` and does not implement the batch hook returns an instance
whose derived state disagrees with its traits; this is the weight behind Q2.

6.3.2. If the live instance is of a different class, the call raises an exception that
names both classes. Two instances never share settings (section 3.6).

6.3.3. If the name is known to the store but no instance is alive under it, a new instance
is built and claims the path (section 4.2.3).

6.3.4. A plain lookup, "the instance called this if there is one", is a separate operation
on the instance store that never builds anything.

6.4. **Bindings.**

6.4.1. When a facility of a host is bound to a part, the framework calls `pyre_bound` on
the part with the host and the trait; when the binding is dissolved, `pyre_unbound`. A
rebinding is an unbind followed by a bind.

6.4.2. These calls are the graph. The flow engine's input and output edges, the recipe's
traversal of what an instance references, and the question "who holds this instance" are
all reconstructions of them today (section 3.13).

6.4.3. A container of parts, i.e. a list, set, or dictionary trait whose schema is a
protocol, is a facility for these purposes: each member is bound and unbound with the same
calls, and the container is classified as a facility by every consumer that classifies
traits. Today such traits are properties and are invisible to the flow engine and to
persistence.

6.5. **Release.**

6.5.1. The instance store refers to instances weakly. An instance is alive while a client
holds it or while it is bound as a part of a live instance.

6.5.2. When an instance dies, or is renamed away from a path, the path is released. The
instance's entry is cleared; the settings under the path are treated per 6.5.3; the
finalization hook has run per 6.5.4.

6.5.3. Settings addressed to the path by a source outside the instance, i.e. package,
user, persistent, and command line sources, stay, so that a later instance under the path
is configured the same way. Settings made through the instance, i.e. constructor
arguments and attribute assignments, go with it. A default that the departed instance
contributed never outranks the default of the next occupant, whatever the order of
events.

6.5.4. The finalization hook runs when the instance is about to be released: on renaming
away from a path, on unbinding from the last host, and on garbage collection. Today the
hook exists and nothing calls it (section 3.11).

6.6. **Observation.**

6.6.1. Every instance carries a revision number that increases when any of its traits
changes and when the revision of any of its parts increases. A consumer that needs to know
whether an instance changed since it last looked compares revisions.

6.6.2. A full history of values, as the tracker keeps today, remains available and remains
opt-in. It is not the mechanism that stale detection or change notification is built on,
because it grows without bound.

6.7. **Session state.** An instance may carry data that is not the value of any trait, e.g.
the position of a node in a diagram, and that a document should preserve. The framework
provides one attachment point for it, keyed by the name of the consumer that owns it, and
persistence writes it out and reads it back beside the settings. Without such a place,
consumers either put it in unclaimed settings, which section 4.5 now reports, or keep
parallel data structures.

6.8. **Persistence.** The recipe of a component, as merged in #254, becomes a description
of a subtree of the instance store: trait settings that were assigned, bindings by family
and name, guards, session state. Bindings refer into the class store by family. Because
release clears what the instance contributed (6.5.3), a saved file no longer accumulates
the settings of departed occupants.

6.9. **Attribute access.** Trait lookup follows the rules of ordinary Python attribute
lookup, and the component system adds as little as possible to them.

6.9.1. A read, `instance.trait` or `Class.trait`, is the descriptor's `__get__`: it finds
the entry for that instance or class and evaluates it. An unassigned instance entry refers
to the class entry (4.2.4); an unassigned entry of a class that inherited the trait refers
to the entry of the ancestor that declared it, as today. The chain of references is the
method resolution order, expressed as entries. The `__getattr__` trap of the current code
goes away.

6.9.2. Aliases are installed by the metaclass as additional class attributes that hold the
same descriptor object, so that `instance.alias` resolves by ordinary lookup. The harvester
that collects traits deduplicates descriptors by identity.

6.9.3. A write on an instance, `instance.trait = value`, is the descriptor's `__set__`,
which records the assignment site as the location. The programmatic assignment operation
passes its location explicitly. The `__setattr__` trap on instances goes away.

6.9.4. A write on a class, `Class.trait = value`, must be intercepted by the metaclass,
because assignment on a class replaces a descriptor rather than invoking it. This is the
one interception the design keeps.

6.9.5. A facility default at class level is a class record or a foundry, while an instance
holds a part. An instance's reference entry therefore carries the instance-side value
processing, the step that builds the part, in the same way that inherited-trait references
carry their processing today. Each instance's entry memoizes its own part; a change of the
class default rebuilds the part of every instance that never assigned the facility, with
the binding events of 6.4.

## 7. The executive

7.1. **The kernel.** The two stores, the registrar, and the configurator are plain objects,
built first, before any class record is declared. They have no traits and are not
components. Their construction is phase one of the boot.

7.2. **The `pyre` instance.** The executive is a component with family `pyre.executive`,
instantiated once, in phase two of the boot, under the name `pyre`. The host, the user,
the terminal, and the environment are its facilities; the configuration path and the host
map are its traits. Its parts are addressed by ownership path: `pyre.host`,
`pyre.host.nickname`. What are framework settings today become the configuration of one
instance.

7.3. **Access.** Every class record and every instance carries one attribute,
`pyre_executive`, a weak reference to the executive, placed on the base classes of
configurables and of value holders when the kernel is built. The module attribute
`pyre.executive` refers to the same object and is set at the end of phase one rather than
at the end of the boot, so that it is usable while the framework's own classes are being
declared. The nine attributes of the dashboard, and the dashboard itself, are removed.

7.4. **The journal cycle.** The journal protocol is a pyre protocol and journal must be
importable during the boot. The kernel of 7.1 gives it what it needs; the remaining
coupling is recorded in the project memory and is resolved as part of this phase.

## 8. What consumers get

8.1. `pyre.flow` keeps the input and output markers, the product and factory protocols,
and the make, tasklist, and targets logic. It stops generating names, because unnamed
instances can be observed (6.1.2); it stops keeping its own edges, because bindings are
reported (6.4); it recognizes container traits of products (6.4.3); and it derives
staleness from revisions (6.6.1).

8.2. The flow editor holds instances directly instead of class records and a parallel
model, names them when the user does (6.1.3), releases them when the user deletes them
(6.5), keeps positions as session state (6.7), and saves and reloads the diagram through
the recipe (6.8).

8.3. The merlin builder addresses its assets by name in the instance store and drops its
private index (4.3.3).

8.4. The three programs are the acceptance tests: a merlin build assembling its graph, the
editor creating, connecting, renaming, deleting, saving, and reloading, and the qed
pipeline rendering while it is rewired.

## 9. Compatibility

9.1. **What breaks.** Building under a live name with a different class raises where it
used to return the first instance (6.3.2). Constructor trait arguments apply where they
used to be discarded (6.3.1). Settings assigned through an instance do not survive it
(6.5.3). An instance that was never assigned a value follows a later change of the class
default (4.2.4, Q1). `family # name` sections and `family#name` values are rejected;
`pml` files are not read. Code that reads the dashboard attributes other than
`pyre_executive` fails.

9.2. **What does not break.** Bare instance sections, class default sections written
without a marker after migration, facility bindings by short name, the priority order of
sources, the hooks by name, `pyre_where` and `pyre_how`, and the persistence API of #254.

9.3. **The migration tool.** As in 5.4. It is a `pyre` application, so that it boots the
framework and can consult the registrar.

## 10. Open questions

Q1. Should an unassigned instance trait refer to the class default (4.2.4), or copy it at
construction as today (3.3)? The proposal says refer: it is how ordinary Python attribute
lookup behaves, it is how subclasses already behave, and it makes the two stores genuinely
layered (6.9). The cost is the change of behavior in 9.1 for long running processes.

Q2. When a live instance of the same class is built again under its name with constructor
arguments (6.3.1), should the arguments apply, or should the call raise? The proposal
says apply, treating the call as a reconfiguration. The alternative treats any arguments
on a repeat construction as an error. The alternative has gained weight from 6.2.5: a
caller who asks for an archive at a new location and receives an instance whose
constructor ran with the old one is worse off than a caller who receives an exception,
unless the class implements the batch hook of Q8.

Q3. Should guards match by pedigree, including protocols (4.4.3), or by exact class as
today? The proposal says pedigree.

Q4. Where does the naming service's output appear in files? Generated names are meant to
be stable within a process, not across processes; a saved document that contains one
will not find the instance when reloaded. The proposal is that persistence names unnamed
instances by ownership path where one exists and refuses to describe an unnamed instance
that is not a part of anything, as the recipe does today.

Q5. What is the default reporting policy for unclaimed settings (4.5.4)? The proposal
says a report at exit on a warning channel.

Q6. Should renaming be allowed while an instance is bound as an owned part, given that
the ownership path is its name? The proposal says no: an owned part's name is derived,
and changes only when the binding changes.

Q7. Should the priority category for constructor arguments stay below the persistent,
user, and command line categories? Under 6.3.1 a repeated construction reconfigures at
that priority, which a user setting still overrides. The proposal keeps the order.

Q8. What is the notification that a batch of settings has been applied to an instance
after its construction (6.1.6, 6.3.1)? One option is a second invocation of
`pyre_configured`, which today runs before `__init__` and therefore cannot assume that
the instance's own attributes exist; a class would have to write it to cope with both
moments. The other is a new hook that runs only after `__init__`, on naming, renaming,
and reconfiguration, leaving `pyre_configured` with one meaning. The proposal leans to
the new hook; its name is open.

## 11. Sequencing

P1. The stores: split the name server into the class store and the instance store, with
weak instance entries, release, guarded settings held in the store, the fall-through of
4.2.4, and the reporting of 4.5. The construction path is adjusted only as far as the
stores require.

P2. The syntax: the parser change for `cfg`, `pfg`, and `yaml`, the `toml` reader, the
removal of `pml`, the command line, and the migration tool. Existing configuration files
in the repository and in the sibling projects are migrated with the tool as its first
test.

P3. The lifecycle: one construction path, identity, naming and renaming, the rules of
6.3, binding events, containers as facilities, revisions, session state, the finalization
hook, and the recipe over the instance store.

P4. The executive: the two-phase boot, the `pyre` instance, the accessor, the removal of
the dashboard, and the journal cycle.

P5. The consumers: `pyre.flow` on the new services, then the editor, the merlin builder,
and the qed pipeline as acceptance tests.

Each phase lands on its own branch with its own tests, and each is usable without the
ones after it.

## 12. Earlier attempts, and where the work is seeded

12.1. The repository `aivazis/p2`, active from December 2019 to January 2021, was an
incubator for a second version. The subsystems that could be exercised on their own
graduated from it into pyre: journal, grid, memory, and timers. The component core stopped
in January 2020, before it had a store, because it could not be exercised without the
configurator, the codecs, the file server, the shells, and the programs that use them.

12.2. Its component core anticipated three parts of this proposal, and they are taken up
here by rewriting rather than by transplanting: traits as data descriptors that learn
their names through `__set_name__` (6.9); class defaults found by walking the method
resolution order, with the instance falling through to its class (4.2.4, Q1); and the
framework managers reached through a module attribute rather than a mixin (7.3).

12.3. The branch `p2` in this repository, twelve commits from January 2021, imported part
of that work into the tracking, constraints, and algebraic packages. Main has since
acquired the one piece that mattered, the name lookup locator, on its own. The branch no
longer merges; what is worth keeping from it is listed in [p2.md](p2.md), and the name is
reused for the integration branch.

12.4. The second version is built in this repository, and the package keeps the name
`pyre`. The branches are arranged so that main remains a releasable first version for the
whole duration: one long-lived integration branch, `p2`, is created from the release tag
`v1.13.1`; each phase of section 11 is developed on a short-lived branch created from `p2`
and merged back into `p2` when its tests pass, the five phases in sequence since each
builds on the previous one; and main receives `p2` once, when the work is complete. The
phase branches never merge into main, because each phase on its own breaks first-version
behavior (9.1) while the downstream projects are pinned to main. Downstream projects move
to the second version by tag, each when it migrates. The branch names and the ledger of
workstreams are in [p2.md](p2.md). The acceptance programs of 8.4 are the reason for staying in this
repository: a separate repository could not run them, and the history of 12.1 shows what
happens to a component core that cannot be exercised end to end.

12.5. The same arrangement serves every other part of the second version. Each further
effort that breaks first-version behavior has its own design document with its own
numbered phases, develops each phase on a short-lived branch created from `p2`, and
merges it back into `p2`. Phases of one effort are sequential because each builds on the
previous one; phases of independent efforts may proceed side by side on `p2`; an effort
that depends on another waits for the phase it needs to land on `p2`. Main still receives
`p2` once.
