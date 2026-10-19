<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# coercions

The suites in `tests/pyre.pkg/coercions` verify what a trait holds after a configuration event
reaches it, for every kind of schema and every source of configuration events. The schemata
themselves are exercised directly in `tests/pyre.pkg/schemata`; the suites here go through a
source.

## Layout

```
coercions/<family>/<schema>/<source>/
```

| family | schemata |
|---|---|
| `text` | `str` `enum` |
| `numbers` | `bool` `int` `float` `complex` `decimal` `fraction` |
| `quantities` | `dimensional` `date` `time` `timestamp` |
| `resources` | `path` `uri` `inet` `istream` `ostream` `envvar` `envpath` |
| `sequences` | `list` `set` `tuple` `array` |
| `mappings` | `dict` `kv` `catalog` |
| `components` | `facility` |
| `composites` | containers of containers, and of components |

| source | what it covers |
|---|---|
| `yaml` | settings in yaml files |
| `pfg` | settings in pfg files |
| `cfg` | settings in cfg files |
| `cli` | settings on the command line |
| `code` | assignments made by code: to the store before the component exists, and to the trait of a live component |
| `recipe` | a component saved as a recipe and read back, with the schema of its traits to guide the writer, and settings that no trait has claimed, without one |

Each case is a driver and the file it loads, with the same name: `flow_map.py` loads
`flow_map.yaml`. The file configures the instance `probe`, and the driver declares the component
under study and checks the case in stages, each one blaming the code that owns it:

1. what the reader of the source makes of the file, compared with the events the case calls for;
2. what the trait holds once the component is built, or how it refuses the setting.

A case that misbehaves fires a `journal.firewall` on `pyre.coercions`, whose report names what
was expected, what happened, and where to look; an error raised where none, or another, was
expected is reported with the innermost frames inside pyre that raised it.

## Cases

Not every schema has every case, and a source may have cases of its own, such as the flow and
block forms of yaml, or operators on the command line.

| group | case | yaml spelling |
|---|---|---|
| presence | `absent` | nothing configures the instance |
| | `null` | `trait:` |
| empty | `empty_text` | `trait: ''` |
| | `empty_map` | `trait: {}` |
| text | `quoted_braces` | `trait: "{}"` |
| macros | `unresolved` | `trait: "{x}"`, a macro that refers to a name nobody defines |
| structure | `flow_map` | `trait: {k: v}` |
| | `block_map` | `trait:` with `k: v` indented under it |
| | `block_existing_key` | the block form, naming a key the default already has |
| entries | `entry_empty_map` | `trait: {k: {}}` |
| | `entry_unresolved` | `trait: {k: "{x}"}` |


<!-- end of file -->
